#!/usr/bin/env python
"""
AI City Simulation - Android/Termux Python Launcher
Optimized for mobile devices with automatic dependency checking
"""
import sys
import subprocess
import os

def check_package(package_name):
    """Check if a Python package is installed"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def install_package(package_name):
    """Install a package using pip"""
    print(f"Installing {package_name}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

def main():
    print("=" * 50)
    print("AI City Simulation - Android Edition")
    print("Crafted by Intellegix")
    print("=" * 50)
    print()

    # Check required packages
    required_packages = {
        'numpy': 'numpy',
        'pygame': 'pygame',
        'noise': 'noise',
        'networkx': 'networkx',
        'scipy': 'scipy',
        'dataclasses_json': 'dataclasses-json'
    }

    missing_packages = []
    for import_name, package_name in required_packages.items():
        if not check_package(import_name):
            missing_packages.append(package_name)
            print(f"✗ {package_name} not installed")
        else:
            print(f"✓ {package_name} installed")

    if missing_packages:
        print()
        print(f"Missing {len(missing_packages)} package(s). Install them with:")
        print(f"  pip install {' '.join(missing_packages)}")
        print()
        response = input("Install missing packages now? (y/n): ").lower()
        if response == 'y':
            for package in missing_packages:
                try:
                    install_package(package)
                except Exception as e:
                    print(f"Error installing {package}: {e}")
                    return 1
        else:
            print("Cannot run without required packages.")
            return 1

    print()
    print("All dependencies installed!")
    print()

    # Switch to Android config
    if os.path.exists('config.py') and not os.path.exists('config_original.py'):
        print("Backing up original config...")
        os.rename('config.py', 'config_original.py')

    if os.path.exists('config_android.py'):
        print("Using Android-optimized configuration...")
        import shutil
        shutil.copy('config_android.py', 'config.py')

    print()
    print("Starting AI City Simulation...")
    print("Controls:")
    print("  - Arrow keys or WASD to move camera")
    print("  - Q/E to zoom in/out")
    print("  - ESC to exit")
    print()

    # Import and run main
    try:
        from main import CitySimulation
        import argparse

        # Create simulation with Android-optimized settings
        sim = CitySimulation(seed=42, npc_count=5, grid_size=256)
        sim.run()

    except Exception as e:
        print(f"Error running simulation: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        # Restore original config
        if os.path.exists('config_original.py'):
            print()
            print("Restoring original config...")
            if os.path.exists('config.py'):
                os.remove('config.py')
            os.rename('config_original.py', 'config.py')

    print()
    print("Simulation ended. Thank you!")
    return 0

if __name__ == '__main__':
    sys.exit(main())
