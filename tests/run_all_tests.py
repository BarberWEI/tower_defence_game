#!/usr/bin/env python3
"""
Tower Defense Game Test Runner

This script runs all test suites for the tower defense game and provides
a comprehensive test report.

Usage:
    python tests/run_all_tests.py
    python tests/run_all_tests.py --verbose
    python tests/run_all_tests.py --specific test_towers
"""

import unittest
import sys
import os
import argparse
from io import StringIO

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all test modules
from tests.test_towers import TestTowersFixed
from tests.test_enemies import TestEnemies
from tests.test_projectiles import TestProjectiles
from tests.test_game_systems import TestGameSystemsFixed
from tests.test_integration import TestIntegration


class ColoredTextTestResult(unittest.TextTestResult):
    """Custom test result class with colored output"""
    
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.success_count = 0
        self.verbosity = verbosity  # Store verbosity for later use
        
    def addSuccess(self, test):
        super().addSuccess(test)
        self.success_count += 1
        if self.verbosity > 1:
            self.stream.write("✓ ")
            self.stream.writeln(self.getDescription(test))
        elif self.verbosity == 1:
            self.stream.write("✓")
        self.stream.flush()
    
    def addError(self, test, err):
        super().addError(test, err)
        if self.verbosity > 1:
            self.stream.write("✗ ERROR: ")
            self.stream.writeln(self.getDescription(test))
        elif self.verbosity == 1:
            self.stream.write("E")
        self.stream.flush()
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        if self.verbosity > 1:
            self.stream.write("✗ FAIL: ")
            self.stream.writeln(self.getDescription(test))
        elif self.verbosity == 1:
            self.stream.write("F")
        self.stream.flush()
    
    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        if self.verbosity > 1:
            self.stream.write("- SKIP: ")
            self.stream.writeln(f"{self.getDescription(test)} ({reason})")
        elif self.verbosity == 1:
            self.stream.write("S")
        self.stream.flush()


class TowerDefenseTestRunner:
    """Custom test runner for tower defense game tests"""
    
    def __init__(self, verbosity=1):
        self.verbosity = verbosity
        self.test_suites = {
        'towers': TestTowersFixed,
        'enemies': TestEnemies,
        'projectiles': TestProjectiles,
        'game_systems': TestGameSystemsFixed,
        'integration': TestIntegration
    }
    
    def run_specific_suite(self, suite_name):
        """Run a specific test suite"""
        if suite_name not in self.test_suites:
            print(f"Unknown test suite: {suite_name}")
            print(f"Available suites: {', '.join(self.test_suites.keys())}")
            return False
        
        print(f"\n{'='*60}")
        print(f"Running {suite_name.upper()} Tests")
        print(f"{'='*60}")
        
        suite = unittest.TestLoader().loadTestsFromTestCase(self.test_suites[suite_name])
        runner = unittest.TextTestRunner(
            verbosity=self.verbosity,
            resultclass=ColoredTextTestResult
        )
        result = runner.run(suite)
        
        return result.wasSuccessful()
    
    def run_all_tests(self):
        """Run all test suites"""
        print("Tower Defense Game - Comprehensive Test Suite")
        print("=" * 60)
        
        all_results = []
        total_tests = 0
        total_failures = 0
        total_errors = 0
        total_skipped = 0
        
        for suite_name in self.test_suites.keys():
            print(f"\n{'='*60}")
            print(f"Running {suite_name.upper()} Tests")
            print(f"{'='*60}")
            
            suite = unittest.TestLoader().loadTestsFromTestCase(self.test_suites[suite_name])
            
            # Capture output for summary
            stream = StringIO()
            runner = unittest.TextTestRunner(
                stream=stream,
                verbosity=self.verbosity,
                resultclass=ColoredTextTestResult
            )
            result = runner.run(suite)
            
            # Print the output
            output = stream.getvalue()
            print(output)
            
            # Collect statistics
            all_results.append((suite_name, result))
            total_tests += result.testsRun
            total_failures += len(result.failures)
            total_errors += len(result.errors)
            total_skipped += len(result.skipped)
        
        # Print comprehensive summary
        self.print_summary(all_results, total_tests, total_failures, total_errors, total_skipped)
        
        # Return overall success
        return total_failures == 0 and total_errors == 0
    
    def print_summary(self, results, total_tests, total_failures, total_errors, total_skipped):
        """Print comprehensive test summary"""
        print("\n" + "="*80)
        print("COMPREHENSIVE TEST SUMMARY")
        print("="*80)
        
        # Per-suite summary
        print("\nPer-Suite Results:")
        print("-" * 50)
        for suite_name, result in results:
            status = "✓ PASS" if result.wasSuccessful() else "✗ FAIL"
            success_count = getattr(result, 'success_count', result.testsRun - len(result.failures) - len(result.errors))
            print(f"{suite_name.ljust(15)} | {status} | "
                  f"{success_count}/{result.testsRun} tests passed")
            
            if result.failures:
                print(f"{''.ljust(15)} |      | {len(result.failures)} failures")
            if result.errors:
                print(f"{''.ljust(15)} |      | {len(result.errors)} errors")
            if result.skipped:
                print(f"{''.ljust(15)} |      | {len(result.skipped)} skipped")
        
        # Overall summary
        print("\nOverall Results:")
        print("-" * 50)
        total_passed = total_tests - total_failures - total_errors - total_skipped
        print(f"Total Tests:    {total_tests}")
        print(f"Passed:         {total_passed} ✓")
        print(f"Failed:         {total_failures} {'✗' if total_failures > 0 else ''}")
        print(f"Errors:         {total_errors} {'✗' if total_errors > 0 else ''}")
        print(f"Skipped:        {total_skipped} {'-' if total_skipped > 0 else ''}")
        
        # Success rate
        if total_tests > 0:
            success_rate = (total_passed / total_tests) * 100
            print(f"Success Rate:   {success_rate:.1f}%")
        
        # Final status
        print("\n" + "="*80)
        if total_failures == 0 and total_errors == 0:
            print("🎉 ALL TESTS PASSED! The tower defense game is working correctly.")
        else:
            print("❌ SOME TESTS FAILED! Please review the failures and errors above.")
        print("="*80)
    
    def run_test_discovery(self):
        """Discover and list all available tests"""
        print("Tower Defense Game - Test Discovery")
        print("=" * 60)
        
        total_test_count = 0
        for suite_name, test_class in self.test_suites.items():
            print(f"\n{suite_name.upper()} Tests:")
            print("-" * 30)
            
            # Get all test methods from the test class
            test_methods = [method for method in dir(test_class) if method.startswith('test_')]
            test_count = len(test_methods)
            
            for test_name in test_methods:
                # Extract docstring for description
                test_method = getattr(test_class, test_name)
                doc = test_method.__doc__ or "No description"
                print(f"  {test_name}: {doc.strip()}")
            
            print(f"  Total: {test_count} tests")
            total_test_count += test_count
        
        print(f"\nTotal test suites: {len(self.test_suites)}")
        print(f"Total tests: {total_test_count}")


def main():
    """Main function to run tests based on command line arguments"""
    parser = argparse.ArgumentParser(description='Run tower defense game tests')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    parser.add_argument('--specific', '-s', type=str,
                       help='Run specific test suite (towers, enemies, projectiles, game_systems, integration)')
    parser.add_argument('--discover', '-d', action='store_true',
                       help='Discover and list all available tests')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Minimal output')
    
    args = parser.parse_args()
    
    # Set verbosity
    if args.quiet:
        verbosity = 0
    elif args.verbose:
        verbosity = 2
    else:
        verbosity = 1
    
    runner = TowerDefenseTestRunner(verbosity=verbosity)
    
    # Handle different modes
    if args.discover:
        runner.run_test_discovery()
        return 0
    
    elif args.specific:
        success = runner.run_specific_suite(args.specific)
        return 0 if success else 1
    
    else:
        success = runner.run_all_tests()
        return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main()) 