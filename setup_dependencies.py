#!/usr/bin/env python3
"""
Auto-installer for Lofi Hip Hop Generator dependencies
Downloads and configures FFmpeg and FluidSynth automatically
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil
import platform
from pathlib import Path

def is_admin():
    """Check if running with admin privileges"""
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def download_file(url, dest):
    """Download file with progress"""
    print(f"Downloading from {url}...")

    def reporthook(count, block_size, total_size):
        percent = int(count * block_size * 100 / total_size)
        sys.stdout.write(f"\rProgress: {percent}%")
        sys.stdout.flush()

    urllib.request.urlretrieve(url, dest, reporthook)
    print("\nDownload complete!")

def install_ffmpeg_windows():
    """Install FFmpeg on Windows"""
    print("\n" + "="*50)
    print("Installing FFmpeg...")
    print("="*50)

    # Try winget first
    try:
        print("Attempting installation via winget...")
        result = subprocess.run(
            ['winget', 'install', 'ffmpeg', '--silent'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✓ FFmpeg installed successfully via winget!")
            return True
    except FileNotFoundError:
        print("Winget not available, using manual installation...")

    # Manual installation
    ffmpeg_dir = Path("C:/ffmpeg")
    if ffmpeg_dir.exists():
        print("FFmpeg directory already exists")
        choice = input("Reinstall? (y/n): ").lower()
        if choice != 'y':
            return True

    # Download FFmpeg
    ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    temp_zip = Path("ffmpeg_temp.zip")

    try:
        download_file(ffmpeg_url, temp_zip)

        print("Extracting FFmpeg...")
        with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
            zip_ref.extractall("C:/")

        # Find extracted folder
        for item in Path("C:/").glob("ffmpeg-*-essentials_build"):
            # Move bin folder
            bin_src = item / "bin"
            ffmpeg_dir.mkdir(exist_ok=True)
            bin_dest = ffmpeg_dir / "bin"

            if bin_dest.exists():
                shutil.rmtree(bin_dest)

            shutil.copytree(bin_src, bin_dest)
            shutil.rmtree(item)
            break

        temp_zip.unlink()

        # Add to PATH
        add_to_path("C:/ffmpeg/bin")

        print("✓ FFmpeg installed successfully!")
        return True

    except Exception as e:
        print(f"✗ Error installing FFmpeg: {e}")
        return False

def add_to_path(directory):
    """Add directory to system PATH"""
    if platform.system() == "Windows":
        try:
            # Try to add to user PATH
            result = subprocess.run(
                ['setx', 'PATH', f"%PATH%;{directory}"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"✓ Added {directory} to PATH")
                print("  Please restart your terminal for changes to take effect")
            else:
                print(f"⚠ Could not add to PATH automatically")
                print(f"  Please add manually: {directory}")
        except Exception as e:
            print(f"⚠ Error adding to PATH: {e}")

def check_python_packages():
    """Check and install Python packages"""
    print("\n" + "="*50)
    print("Checking Python packages...")
    print("="*50)

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✓ Python packages installed!")
            return True
        else:
            print("✗ Error installing Python packages")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False

def create_directories():
    """Create necessary directories"""
    print("\n" + "="*50)
    print("Creating directories...")
    print("="*50)

    dirs = ['output', 'data', 'midi_songs']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✓ Created: {dir_name}/")

def main():
    """Main installation function"""
    print("\n" + "="*60)
    print("  LOFI HIP HOP GENERATOR - DEPENDENCY INSTALLER")
    print("="*60)
    print()

    if platform.system() != "Windows":
        print("This auto-installer is for Windows only.")
        print("Please see the documentation for your platform.")
        return

    # Check Python
    print(f"Python version: {sys.version}")

    # Create directories
    create_directories()

    # Install Python packages
    if not check_python_packages():
        print("\n⚠ Warning: Some packages failed to install")
        print("You may need to install them manually")

    # Check/Install FFmpeg
    print()
    if check_ffmpeg():
        print("✓ FFmpeg is already installed")
    else:
        print("FFmpeg not found. Installing...")

        if not is_admin():
            print("\n⚠ WARNING: Not running as administrator")
            print("FFmpeg installation may fail without admin privileges")
            print()
            choice = input("Continue anyway? (y/n): ").lower()
            if choice != 'y':
                print("Installation cancelled")
                return

        install_ffmpeg_windows()

    # Final summary
    print("\n" + "="*60)
    print("  INSTALLATION SUMMARY")
    print("="*60)

    checks = {
        "Python": sys.version_info >= (3, 8),
        "FFmpeg": check_ffmpeg(),
        "Directories": Path("output").exists(),
    }

    for name, status in checks.items():
        symbol = "✓" if status else "✗"
        print(f"{symbol} {name}: {'OK' if status else 'MISSING'}")

    print("\n" + "="*60)

    if all(checks.values()):
        print("✓ Installation complete!")
        print("\nNext steps:")
        print("1. Restart your terminal/command prompt")
        print("2. Run: python gui.py")
        print("3. Enjoy creating lofi music!")
    else:
        print("⚠ Some components are missing")
        print("\nPlease check:")
        print("- WINDOWS_INSTALL.md for manual installation")
        print("- INSTALL_FFMPEG_WINDOWS.md for FFmpeg help")

    print("\n" + "="*60)
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
