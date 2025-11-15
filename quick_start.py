#!/usr/bin/env python3
"""
Quick Start Example - Lofi Hip Hop Generator
Demonstrates basic usage of the system
"""

import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def quick_demo():
    """
    Quick demonstration of the Lofi Hip Hop Generator

    This will:
    1. Generate lofi music (MIDI)
    2. Convert to audio
    3. Create aurora visualization
    4. Combine into final video
    """
    logger.info("=" * 60)
    logger.info("LOFI HIP HOP GENERATOR - QUICK START")
    logger.info("=" * 60)

    try:
        # Import modules
        from main import LofiStreamGenerator
        from config import get_config

        # Check if model weights exist
        config = get_config()
        weights_file = config.get('model.weights_file')

        if not Path(weights_file).exists():
            logger.error(f"Model weights not found: {weights_file}")
            logger.error("Please run training first:")
            logger.error("  python main.py train")
            return

        # Check if notes data exists
        notes_file = config.get('data.notes_file', 'data/notes')
        if not Path(notes_file).exists():
            logger.error(f"Notes file not found: {notes_file}")
            logger.error("Please run training first to process MIDI files:")
            logger.error("  python main.py train")
            return

        # Create generator
        logger.info("\nInitializing generator...")
        generator = LofiStreamGenerator()

        # Generate complete video with default settings
        logger.info("\nGenerating lofi music and aurora video...")
        logger.info("This may take several minutes depending on your hardware.")
        logger.info("")

        results = generator.generate_complete_video(
            num_notes=200,      # Generate 200 notes (shorter for demo)
            temperature=1.0,    # Standard creativity
            duration=None,      # Match audio duration
            output_name='quick_demo.mp4'
        )

        # Show results
        logger.info("\n" + "=" * 60)
        logger.info("GENERATION COMPLETE!")
        logger.info("=" * 60)
        logger.info("\nGenerated files:")

        for key, path in results.items():
            if path and Path(path).exists():
                size = Path(path).stat().st_size / (1024 * 1024)  # MB
                logger.info(f"  {key:20s}: {path} ({size:.2f} MB)")

        logger.info("\n" + "=" * 60)
        logger.info("You can now:")
        logger.info(f"  - Play the video: {results.get('final_video', 'N/A')}")
        logger.info(f"  - Listen to audio: {results.get('audio', 'N/A')}")
        logger.info(f"  - Use MIDI: {results.get('midi', 'N/A')}")
        logger.info("\nTo stream to YouTube/Twitch:")
        logger.info(f"  python main.py stream {results.get('optimized_video')} --platform youtube --key YOUR_KEY")
        logger.info("=" * 60)

    except ImportError as e:
        logger.error(f"Import error: {e}")
        logger.error("Please install requirements: pip install -r requirements.txt")

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        logger.error("Make sure you have:")
        logger.error("  1. Trained the model (python main.py train)")
        logger.error("  2. MIDI files in midi_songs/")

    except Exception as e:
        logger.error(f"Error during generation: {e}", exc_info=True)


def simple_music_generation():
    """
    Simple example: Just generate music (no video)
    """
    logger.info("Generating music only (no video)...")

    try:
        from music_generator import generate_lofi_music

        midi_file = generate_lofi_music(
            num_notes=300,
            temperature=1.0,
            bpm=80
        )

        logger.info(f"Music generated: {midi_file}")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)


def simple_aurora_generation():
    """
    Simple example: Just generate aurora video (no music)
    """
    logger.info("Generating aurora visualization only...")

    try:
        from aurora_visualizer import create_aurora_video

        video_file = create_aurora_video(
            duration=60,  # 1 minute
            output_file='output/aurora_demo.mp4'
        )

        logger.info(f"Aurora video generated: {video_file}")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)


def main():
    """Main entry point"""
    import sys

    if len(sys.argv) > 1:
        mode = sys.argv[1]

        if mode == 'music':
            simple_music_generation()
        elif mode == 'aurora':
            simple_aurora_generation()
        elif mode == 'full':
            quick_demo()
        else:
            print("Usage:")
            print("  python quick_start.py full    # Complete demo")
            print("  python quick_start.py music   # Music only")
            print("  python quick_start.py aurora  # Aurora only")
    else:
        # Default: full demo
        quick_demo()


if __name__ == '__main__':
    main()
