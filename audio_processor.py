"""Audio processing and MIDI to audio conversion"""
import subprocess
from pathlib import Path
from typing import Optional
import logging
import numpy as np

from config import get_config

logger = logging.getLogger(__name__)


class AudioProcessor:
    """Process and convert audio files"""

    def __init__(self, config_path: str = 'config.yaml'):
        self.config = get_config(config_path)

    def midi_to_audio(
        self,
        midi_file: str,
        output_file: Optional[str] = None,
        soundfont: Optional[str] = None
    ) -> str:
        """
        Convert MIDI file to audio using FluidSynth

        Args:
            midi_file: Path to input MIDI file
            output_file: Path to output audio file. Auto-generated if None.
            soundfont: Path to soundfont file. Uses default if None.

        Returns:
            Path to created audio file

        Raises:
            FileNotFoundError: If MIDI file or soundfont doesn't exist
            RuntimeError: If conversion fails
        """
        midi_path = Path(midi_file)
        if not midi_path.exists():
            raise FileNotFoundError(f"MIDI file not found: {midi_file}")

        if output_file is None:
            output_dir = Path(self.config.get('data.output_directory', 'output'))
            output_file = output_dir / self.config.get_output_filename('audio')

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Get soundfont
        if soundfont is None:
            soundfont = self.config.get('audio.soundfont')

        # Check if FluidSynth is available
        try:
            subprocess.run(['fluidsynth', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("FluidSynth not found. Attempting to use timidity instead.")
            return self._midi_to_audio_timidity(midi_file, output_file)

        logger.info(f"Converting MIDI to audio: {midi_path} -> {output_path}")

        # Build FluidSynth command
        cmd = [
            'fluidsynth',
            '-ni',  # No interactive shell
            '-g', '1.0',  # Gain
            '-F', str(output_path),  # Output file
        ]

        if soundfont and Path(soundfont).exists():
            cmd.append(soundfont)
        else:
            # Use default soundfont (usually /usr/share/soundfonts/default.sf2)
            logger.info("Using default soundfont")

        cmd.append(str(midi_path))

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"Audio file created: {output_path}")
            return str(output_path)

        except subprocess.CalledProcessError as e:
            logger.error(f"FluidSynth conversion failed: {e.stderr}")
            raise RuntimeError(f"MIDI to audio conversion failed: {e.stderr}")

    def _midi_to_audio_timidity(self, midi_file: str, output_file: str) -> str:
        """
        Fallback: Convert MIDI to audio using TiMidity++

        Args:
            midi_file: Path to input MIDI file
            output_file: Path to output audio file

        Returns:
            Path to created audio file
        """
        logger.info("Using TiMidity++ for MIDI conversion")

        cmd = [
            'timidity',
            midi_file,
            '-Ow',  # Output WAV format
            '-o', output_file
        ]

        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.info(f"Audio file created: {output_file}")
            return output_file

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logger.error(f"TiMidity conversion failed: {e}")

            # Provide helpful Windows-specific instructions
            import platform
            if platform.system() == "Windows":
                error_msg = (
                    "MIDI to audio conversion failed.\n\n"
                    "For Windows, please install FluidSynth:\n"
                    "1. Download from: https://github.com/FluidSynth/fluidsynth/releases\n"
                    "2. Or install via MSYS2: pacman -S mingw-w64-x86_64-fluidsynth\n"
                    "3. Add FluidSynth to your PATH\n\n"
                    "See WINDOWS_INSTALL.md for detailed instructions.\n\n"
                    "Note: The MIDI file was created successfully. "
                    "You can continue without audio or install FluidSynth for audio conversion."
                )
            else:
                error_msg = (
                    "MIDI to audio conversion failed. "
                    "Please install FluidSynth or TiMidity++.\n"
                    "Ubuntu/Debian: sudo apt-get install fluidsynth\n"
                    "macOS: brew install fluidsynth"
                )

            raise RuntimeError(error_msg)

    def add_background_audio(
        self,
        main_audio: str,
        background_audio: str,
        output_file: str,
        background_volume: float = 0.3
    ) -> str:
        """
        Mix main audio with background audio (e.g., ambient sounds)

        Args:
            main_audio: Path to main audio file
            background_audio: Path to background audio file
            output_file: Path to output mixed audio file
            background_volume: Volume level for background (0.0-1.0)

        Returns:
            Path to mixed audio file
        """
        logger.info(f"Mixing audio: {main_audio} + {background_audio}")

        # Use ffmpeg for mixing
        cmd = [
            'ffmpeg',
            '-i', main_audio,
            '-i', background_audio,
            '-filter_complex',
            f'[1:a]volume={background_volume}[bg];[0:a][bg]amix=inputs=2:duration=first',
            '-y',  # Overwrite output file
            output_file
        ]

        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.info(f"Mixed audio created: {output_file}")
            return output_file

        except subprocess.CalledProcessError as e:
            logger.error(f"Audio mixing failed: {e.stderr}")
            raise RuntimeError(f"Audio mixing failed: {e.stderr}")

    def normalize_audio(self, audio_file: str, output_file: Optional[str] = None) -> str:
        """
        Normalize audio levels

        Args:
            audio_file: Path to input audio file
            output_file: Path to output file. Overwrites input if None.

        Returns:
            Path to normalized audio file
        """
        if output_file is None:
            output_file = audio_file

        logger.info(f"Normalizing audio: {audio_file}")

        cmd = [
            'ffmpeg',
            '-i', audio_file,
            '-af', 'loudnorm',
            '-y',
            output_file
        ]

        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.info(f"Normalized audio: {output_file}")
            return output_file

        except subprocess.CalledProcessError as e:
            logger.error(f"Audio normalization failed: {e.stderr}")
            raise RuntimeError(f"Audio normalization failed: {e.stderr}")

    def get_audio_duration(self, audio_file: str) -> float:
        """
        Get duration of audio file in seconds

        Args:
            audio_file: Path to audio file

        Returns:
            Duration in seconds
        """
        try:
            import soundfile as sf
            audio_data, sample_rate = sf.read(audio_file)
            duration = len(audio_data) / sample_rate
            return duration

        except Exception as e:
            logger.warning(f"Could not read audio with soundfile: {e}")

            # Fallback to ffprobe
            cmd = [
                'ffprobe',
                '-i', audio_file,
                '-show_entries', 'format=duration',
                '-v', 'quiet',
                '-of', 'csv=p=0'
            ]

            try:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                return float(result.stdout.strip())

            except Exception as e:
                logger.error(f"Could not get audio duration: {e}")
                return 0.0


def convert_midi_to_audio(midi_file: str, output_file: str = None) -> str:
    """
    Convenience function to convert MIDI to audio

    Args:
        midi_file: Path to MIDI file
        output_file: Path to output audio file

    Returns:
        Path to created audio file
    """
    processor = AudioProcessor()
    return processor.midi_to_audio(midi_file, output_file)
