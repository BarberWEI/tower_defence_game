import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class PathGeneratorModel(nn.Module):
    """
    PyTorch model for generating tower defense paths.
    
    Takes a map grid with terrain types, start and end positions,
    and outputs a probability map indicating where the path should go.
    """
    
    def __init__(self, 
                 map_width=40, 
                 map_height=26, 
                 terrain_channels=6,  # Different terrain types (grass, water, forest, etc.)
                 hidden_dim=64):
        """
        Initialize the path generator model.
        
        Args:
            map_width (int): Width of the map grid
            map_height (int): Height of the map grid  
            terrain_channels (int): Number of terrain type channels
            hidden_dim (int): Hidden dimension for conv layers
        """
        super(PathGeneratorModel, self).__init__()
        
        self.map_width = map_width
        self.map_height = map_height
        self.terrain_channels = terrain_channels
        self.hidden_dim = hidden_dim
        
        # Input channels: terrain types + start position + end position
        input_channels = terrain_channels + 2
        
        # Encoder layers - downsample to understand global structure
        self.encoder = nn.Sequential(
            # First conv block
            nn.Conv2d(input_channels, hidden_dim, kernel_size=3, padding=1),
            nn.BatchNorm2d(hidden_dim),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(hidden_dim, hidden_dim, kernel_size=3, padding=1),
            nn.BatchNorm2d(hidden_dim),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),  # Downsample by 2
            
            # Second conv block
            nn.Conv2d(hidden_dim, hidden_dim * 2, kernel_size=3, padding=1),
            nn.BatchNorm2d(hidden_dim * 2),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(hidden_dim * 2, hidden_dim * 2, kernel_size=3, padding=1),
            nn.BatchNorm2d(hidden_dim * 2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),  # Downsample by 2
            
            # Third conv block  
            nn.Conv2d(hidden_dim * 2, hidden_dim * 4, kernel_size=3, padding=1),
            nn.BatchNorm2d(hidden_dim * 4),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(hidden_dim * 4, hidden_dim * 4, kernel_size=3, padding=1),
            nn.BatchNorm2d(hidden_dim * 4),
            nn.ReLU(inplace=True),
        )
        
        # Decoder layers - upsample to generate path probabilities
        self.decoder = nn.Sequential(
            # First upsampling block
            nn.ConvTranspose2d(hidden_dim * 4, hidden_dim * 2, kernel_size=2, stride=2),
            nn.BatchNorm2d(hidden_dim * 2),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(hidden_dim * 2, hidden_dim * 2, kernel_size=3, padding=1),
            nn.BatchNorm2d(hidden_dim * 2),
            nn.ReLU(inplace=True),
            
            # Second upsampling block
            nn.ConvTranspose2d(hidden_dim * 2, hidden_dim, kernel_size=2, stride=2),
            nn.BatchNorm2d(hidden_dim),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(hidden_dim, hidden_dim, kernel_size=3, padding=1),
            nn.BatchNorm2d(hidden_dim),
            nn.ReLU(inplace=True),
        )
        
        # Final path probability layer
        self.path_head = nn.Sequential(
            nn.Conv2d(hidden_dim, hidden_dim // 2, kernel_size=3, padding=1),
            nn.BatchNorm2d(hidden_dim // 2),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(hidden_dim // 2, 1, kernel_size=1),  # Single channel output
            nn.Sigmoid()  # Probability between 0 and 1
        )
        
        # Path connectivity layers for ensuring connected paths
        self.connectivity_layers = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(16, 16, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(16, 1, kernel_size=1),
            nn.Sigmoid()
        )
        
    def forward(self, terrain_map, start_pos, end_pos):
        """
        Forward pass of the path generator.
        
        Args:
            terrain_map (torch.Tensor): [batch_size, terrain_channels, height, width]
                One-hot encoded terrain types
            start_pos (torch.Tensor): [batch_size, 2] - (x, y) coordinates of start
            end_pos (torch.Tensor): [batch_size, 2] - (x, y) coordinates of end
            
        Returns:
            torch.Tensor: [batch_size, 1, height, width] - Path probability map
        """
        batch_size = terrain_map.shape[0]
        
        # Create start and end position channels
        start_channel = torch.zeros(batch_size, 1, self.map_height, self.map_width, 
                                  device=terrain_map.device)
        end_channel = torch.zeros(batch_size, 1, self.map_height, self.map_width,
                                device=terrain_map.device)
        
        # Set start and end positions (convert to int for indexing)
        for i in range(batch_size):
            start_x, start_y = start_pos[i].int()
            end_x, end_y = end_pos[i].int()
            
            # Clamp coordinates to valid range
            start_x = torch.clamp(start_x, 0, self.map_width - 1)
            start_y = torch.clamp(start_y, 0, self.map_height - 1)
            end_x = torch.clamp(end_x, 0, self.map_width - 1)
            end_y = torch.clamp(end_y, 0, self.map_height - 1)
            
            start_channel[i, 0, start_y, start_x] = 1.0
            end_channel[i, 0, end_y, end_x] = 1.0
        
        # Concatenate all input channels
        input_tensor = torch.cat([terrain_map, start_channel, end_channel], dim=1)
        
        # Encode global structure
        encoded = self.encoder(input_tensor)
        
        # Decode to path probabilities
        decoded = self.decoder(encoded)
        
        # Generate initial path probabilities
        path_probs = self.path_head(decoded)
        
        # Refine connectivity
        refined_path = self.connectivity_layers(path_probs)
        
        return refined_path
    
    def generate_path_coordinates(self, path_probs, threshold=0.5):
        """
        Convert path probability map to actual path coordinates.
        
        Args:
            path_probs (torch.Tensor): [batch_size, 1, height, width] - Path probabilities
            threshold (float): Probability threshold for path inclusion
            
        Returns:
            list: List of path coordinates for each batch item
        """
        batch_size = path_probs.shape[0]
        paths = []
        
        for i in range(batch_size):
            prob_map = path_probs[i, 0].detach().cpu().numpy()
            
            # Find coordinates where probability exceeds threshold
            path_coords = np.where(prob_map > threshold)
            
            if len(path_coords[0]) > 0:
                # Convert to (x, y) coordinates
                path_points = list(zip(path_coords[1], path_coords[0]))  # (x, y)
                paths.append(path_points)
            else:
                paths.append([])
        
        return paths


class PathLoss(nn.Module):
    """
    Custom loss function for training the path generator.
    Combines path accuracy with connectivity and smoothness constraints.
    """
    
    def __init__(self, 
                 path_weight=1.0,
                 connectivity_weight=0.5, 
                 smoothness_weight=0.3,
                 distance_weight=0.2):
        """
        Initialize the path loss function.
        
        Args:
            path_weight (float): Weight for basic path prediction loss
            connectivity_weight (float): Weight for path connectivity loss
            smoothness_weight (float): Weight for path smoothness loss
            distance_weight (float): Weight for path length constraint
        """
        super(PathLoss, self).__init__()
        self.path_weight = path_weight
        self.connectivity_weight = connectivity_weight
        self.smoothness_weight = smoothness_weight
        self.distance_weight = distance_weight
        
    def forward(self, predicted_path, target_path, start_pos, end_pos):
        """
        Calculate the total loss for path generation.
        
        Args:
            predicted_path (torch.Tensor): [batch_size, 1, height, width]
            target_path (torch.Tensor): [batch_size, 1, height, width]
            start_pos (torch.Tensor): [batch_size, 2]
            end_pos (torch.Tensor): [batch_size, 2]
            
        Returns:
            torch.Tensor: Total loss value
        """
        # Basic path prediction loss (BCE)
        path_loss = F.binary_cross_entropy(predicted_path, target_path)
        
        # Connectivity loss - ensure path connects start to end
        connectivity_loss = self._connectivity_loss(predicted_path, start_pos, end_pos)
        
        # Smoothness loss - penalize jagged paths
        smoothness_loss = self._smoothness_loss(predicted_path)
        
        # Distance loss - prefer shorter paths
        distance_loss = self._distance_loss(predicted_path)
        
        total_loss = (self.path_weight * path_loss +
                     self.connectivity_weight * connectivity_loss +
                     self.smoothness_weight * smoothness_loss +
                     self.distance_weight * distance_loss)
        
        return total_loss
    
    def _connectivity_loss(self, path_probs, start_pos, end_pos):
        """Calculate connectivity loss to ensure path connects start and end."""
        batch_size = path_probs.shape[0]
        connectivity_loss = 0.0
        
        for i in range(batch_size):
            # Extract start and end coordinates
            start_x, start_y = start_pos[i].int()
            end_x, end_y = end_pos[i].int()
            
            # Check if start and end positions have high probability
            start_prob = path_probs[i, 0, start_y, start_x]
            end_prob = path_probs[i, 0, end_y, end_x]
            
            # Penalize if start/end don't have high path probability
            connectivity_loss += (1.0 - start_prob) + (1.0 - end_prob)
        
        return connectivity_loss / batch_size
    
    def _smoothness_loss(self, path_probs):
        """Calculate smoothness loss to penalize jagged paths."""
        # Compute gradients in x and y directions
        grad_x = torch.abs(path_probs[:, :, :, 1:] - path_probs[:, :, :, :-1])
        grad_y = torch.abs(path_probs[:, :, 1:, :] - path_probs[:, :, :-1, :])
        
        # Return mean gradient magnitude
        return torch.mean(grad_x) + torch.mean(grad_y)
    
    def _distance_loss(self, path_probs):
        """Calculate distance loss to prefer shorter paths."""
        # Sum of all path probabilities (higher = longer path)
        return torch.mean(torch.sum(path_probs, dim=(2, 3)))


def create_terrain_encoding(terrain_type, terrain_channels=6):
    """
    Helper function to create one-hot encoding for terrain types.
    
    Args:
        terrain_type (int): Terrain type index (0-5)
        terrain_channels (int): Total number of terrain types
        
    Returns:
        torch.Tensor: One-hot encoded terrain channel
    """
    encoding = torch.zeros(terrain_channels)
    if 0 <= terrain_type < terrain_channels:
        encoding[terrain_type] = 1.0
    return encoding 