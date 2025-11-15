#!/bin/bash
# Installation script for Lofi Hip Hop Generator

set -e  # Exit on error

echo "=================================="
echo "Lofi Hip Hop Generator Installer"
echo "=================================="
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    echo "Unsupported OS: $OSTYPE"
    exit 1
fi

echo "Detected OS: $OS"
echo ""

# Install system dependencies
echo "[1/4] Installing system dependencies..."

if [ "$OS" == "linux" ]; then
    echo "Using apt-get (Ubuntu/Debian)..."
    sudo apt-get update
    sudo apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        fluidsynth \
        fluid-soundfont-gm \
        timidity \
        ffmpeg \
        libsndfile1
    echo "✓ System dependencies installed"

elif [ "$OS" == "macos" ]; then
    if ! command -v brew &> /dev/null; then
        echo "Error: Homebrew not found. Please install from https://brew.sh"
        exit 1
    fi

    echo "Using Homebrew..."
    brew install python3 fluidsynth timidity ffmpeg libsndfile
    echo "✓ System dependencies installed"
fi

echo ""

# Create virtual environment
echo "[2/4] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""

# Activate virtual environment and install Python packages
echo "[3/4] Installing Python packages..."
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "✓ Python packages installed"
echo ""

# Create necessary directories
echo "[4/4] Setting up directories..."
mkdir -p output
mkdir -p data
mkdir -p midi_songs

echo "✓ Directories created"
echo ""

# Check if MIDI files exist
MIDI_COUNT=$(find midi_songs -name "*.mid" 2>/dev/null | wc -l)
if [ $MIDI_COUNT -eq 0 ]; then
    echo "⚠️  Warning: No MIDI files found in midi_songs/"
    echo "   Please add MIDI files before training the model."
else
    echo "✓ Found $MIDI_COUNT MIDI files in midi_songs/"
fi

echo ""
echo "=================================="
echo "Installation Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Add MIDI files to midi_songs/ (if not already present)"
echo "3. Train the model: python main.py train"
echo "4. Generate music: python main.py generate"
echo ""
echo "For more information, see README_NEW.md"
echo ""
