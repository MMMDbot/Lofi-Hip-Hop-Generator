#!/usr/bin/env python3
"""
Lofi Hip Hop Generator with Aurora Visualization
Main orchestration script
"""
import argparse
import logging
import sys
from pathlib import Path

from config import get_config
from music_generator import MusicGenerator
from audio_processor import AudioProcessor
from aurora_visualizer import AuroraVisualizer
from video_composer import VideoComposer
from streamer import LiveStreamer
from data_processor import MidiDataProcessor
from model import LofiMusicModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LofiStreamGenerator:
    """Main class for generating lofi music streams with aurora visuals"""

    def __init__(self, config_path: str = 'config.yaml'):
        self.config = get_config(config_path)
        self.music_generator = MusicGenerator(config_path)
        self.audio_processor = AudioProcessor(config_path)
        self.aurora_visualizer = AuroraVisualizer(config_path)
        self.video_composer = VideoComposer(config_path)
        self.streamer = LiveStreamer(config_path)

    def generate_complete_video(
        self,
        num_notes: int = None,
        temperature: float = None,
        duration: float = None,
        output_name: str = None
    ) -> dict:
        """
        Generate complete video with music and aurora visualization

        Args:
            num_notes: Number of musical notes to generate
            temperature: Sampling temperature for music generation
            duration: Video duration in seconds
            output_name: Base name for output files

        Returns:
            Dictionary with paths to generated files
        """
        logger.info("=" * 60)
        logger.info("LOFI HIP HOP AURORA STREAM GENERATOR")
        logger.info("=" * 60)

        output_dir = Path(self.config.get('data.output_directory', 'output'))
        output_dir.mkdir(parents=True, exist_ok=True)

        results = {}

        # Step 1: Generate Music (MIDI)
        logger.info("\n[1/5] Generating lofi music...")
        midi_file = self.music_generator.generate_music(
            num_notes=num_notes,
            temperature=temperature
        )
        results['midi'] = midi_file
        logger.info(f"✓ MIDI file created: {midi_file}")

        # Step 2: Convert MIDI to Audio
        logger.info("\n[2/5] Converting MIDI to audio...")
        try:
            audio_file = self.audio_processor.midi_to_audio(midi_file)
            results['audio'] = audio_file
            logger.info(f"✓ Audio file created: {audio_file}")

            # Get audio duration for video
            audio_duration = self.audio_processor.get_audio_duration(audio_file)
            logger.info(f"  Audio duration: {audio_duration:.2f} seconds")

        except Exception as e:
            logger.error(f"Failed to convert MIDI to audio: {e}")
            logger.info("Continuing with video generation...")
            audio_file = None
            audio_duration = duration or 300

        # Step 3: Generate Aurora Visualization
        logger.info("\n[3/5] Generating aurora borealis visualization...")
        video_file = self.aurora_visualizer.generate_video(
            duration=audio_duration if audio_file else duration,
            audio_file=audio_file
        )
        results['video_silent'] = video_file
        logger.info(f"✓ Aurora video created: {video_file}")

        # Step 4: Combine Audio and Video
        if audio_file:
            logger.info("\n[4/5] Combining audio and video...")
            final_video = self.video_composer.combine_audio_video(
                video_file,
                audio_file,
                str(output_dir / (output_name or 'lofi_aurora_final.mp4'))
            )
            results['final_video'] = final_video
            logger.info(f"✓ Final video created: {final_video}")

            # Step 5: Optimize for streaming
            logger.info("\n[5/5] Optimizing for streaming...")
            optimized_video = self.video_composer.optimize_for_streaming(final_video)
            results['optimized_video'] = optimized_video
            logger.info(f"✓ Optimized video created: {optimized_video}")

        else:
            results['final_video'] = video_file
            results['optimized_video'] = video_file
            logger.warning("Skipped audio-video combination (no audio)")

        logger.info("\n" + "=" * 60)
        logger.info("GENERATION COMPLETE!")
        logger.info("=" * 60)

        for key, path in results.items():
            logger.info(f"{key}: {path}")

        return results

    def start_stream(
        self,
        video_file: str,
        platform: str = 'youtube',
        stream_key: str = None
    ):
        """
        Start streaming video

        Args:
            video_file: Path to video file to stream
            platform: Platform to stream to
            stream_key: Stream key for the platform
        """
        logger.info(f"Starting stream to {platform}...")

        if not Path(video_file).exists():
            raise FileNotFoundError(f"Video file not found: {video_file}")

        try:
            if platform == 'youtube':
                process = self.streamer.stream_youtube(video_file, stream_key)
            elif platform == 'twitch':
                process = self.streamer.stream_twitch(video_file, stream_key)
            else:
                raise ValueError(f"Unknown platform: {platform}")

            logger.info("Stream started! Press Ctrl+C to stop.")

            # Monitor stream
            try:
                process.wait()
            except KeyboardInterrupt:
                logger.info("\nStopping stream...")
                self.streamer.stop_stream()

        except Exception as e:
            logger.error(f"Streaming failed: {e}")
            raise


def train_model(config_path: str = 'config.yaml'):
    """Train the music generation model"""
    logger.info("=" * 60)
    logger.info("TRAINING LOFI MUSIC MODEL")
    logger.info("=" * 60)

    config = get_config(config_path)

    # Process data
    logger.info("\n[1/3] Processing MIDI files...")
    processor = MidiDataProcessor(config_path)
    notes = processor.get_notes_from_midi()
    processor.save_notes()

    # Prepare sequences
    logger.info("\n[2/3] Preparing training sequences...")
    network_input, network_output = processor.prepare_sequences(notes)

    # Create and train model
    logger.info("\n[3/3] Training model...")
    model = LofiMusicModel(config_path)
    model.create_model(network_input, processor.get_vocabulary_size())
    model.train(network_input, network_output)

    logger.info("\n" + "=" * 60)
    logger.info("TRAINING COMPLETE!")
    logger.info("=" * 60)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Lofi Hip Hop Generator with Aurora Visualization'
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Train command
    train_parser = subparsers.add_parser('train', help='Train the music model')
    train_parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to configuration file'
    )

    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate music and video')
    gen_parser.add_argument(
        '--notes',
        type=int,
        help='Number of notes to generate'
    )
    gen_parser.add_argument(
        '--temperature',
        type=float,
        help='Sampling temperature (0.5-2.0)'
    )
    gen_parser.add_argument(
        '--duration',
        type=float,
        help='Video duration in seconds'
    )
    gen_parser.add_argument(
        '--output',
        help='Output filename'
    )
    gen_parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to configuration file'
    )

    # Stream command
    stream_parser = subparsers.add_parser('stream', help='Stream video')
    stream_parser.add_argument(
        'video_file',
        help='Path to video file to stream'
    )
    stream_parser.add_argument(
        '--platform',
        choices=['youtube', 'twitch'],
        default='youtube',
        help='Streaming platform'
    )
    stream_parser.add_argument(
        '--key',
        help='Stream key'
    )
    stream_parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to configuration file'
    )

    # Full pipeline command
    full_parser = subparsers.add_parser(
        'full',
        help='Generate and stream (full pipeline)'
    )
    full_parser.add_argument(
        '--notes',
        type=int,
        help='Number of notes to generate'
    )
    full_parser.add_argument(
        '--temperature',
        type=float,
        help='Sampling temperature'
    )
    full_parser.add_argument(
        '--platform',
        choices=['youtube', 'twitch'],
        help='Streaming platform'
    )
    full_parser.add_argument(
        '--key',
        help='Stream key'
    )
    full_parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to configuration file'
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == 'train':
            train_model(args.config)

        elif args.command == 'generate':
            generator = LofiStreamGenerator(args.config)
            generator.generate_complete_video(
                num_notes=args.notes,
                temperature=args.temperature,
                duration=args.duration,
                output_name=args.output
            )

        elif args.command == 'stream':
            generator = LofiStreamGenerator(args.config)
            generator.start_stream(
                args.video_file,
                args.platform,
                args.key
            )

        elif args.command == 'full':
            generator = LofiStreamGenerator(args.config)

            # Generate
            results = generator.generate_complete_video(
                num_notes=args.notes,
                temperature=args.temperature
            )

            # Stream if requested
            if args.platform and args.key:
                generator.start_stream(
                    results['optimized_video'],
                    args.platform,
                    args.key
                )

    except KeyboardInterrupt:
        logger.info("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
