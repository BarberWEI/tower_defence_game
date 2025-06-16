import pygame
import sys
from game import Game

def main():
    pygame.init()
    game = Game()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_event(event)
        
        game.update()
        game.draw()
        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main() 