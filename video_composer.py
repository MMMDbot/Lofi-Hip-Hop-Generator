"""Video composition and audio-video synchronization"""
import subprocess
from pathlib import Path
from typing import Optional
import logging

from config import get_config

logger = logging.getLogger(__name__)


class VideoComposer:
    """Compose video with audio and create final output"""

    def __init__(self, config_path: str = 'config.yaml'):
        self.config = get_config(config_path)

    def combine_audio_video(
        self,
        video_file: str,
        audio_file: str,
        output_file: Optional[str] = None,
        video_codec: str = 'libx264',
        audio_codec: str = 'aac',
        video_bitrate: Optional[str] = None,
        audio_bitrate: Optional[str] = None
    ) -> str:
        """
        Combine video and audio files

        Args:
            video_file: Path to video file
            audio_file: Path to audio file
            output_file: Path to output file. Auto-generated if None.
            video_codec: Video codec to use
            audio_codec: Audio codec to use
            video_bitrate: Video bitrate (e.g., '4500k')
            audio_bitrate: Audio bitrate (e.g., '128k')

        Returns:
            Path to combined video file
        """
        video_path = Path(video_file)
        audio_path = Path(audio_file)

        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_file}")
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_file}")

        if output_file is None:
            output_dir = Path(self.config.get('data.output_directory', 'output'))
            output_file = output_dir / 'lofi_aurora_final.mp4'

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if video_bitrate is None:
            video_bitrate = self.config.get('streaming.bitrate_video', '4500k')
        if audio_bitrate is None:
            audio_bitrate = self.config.get('streaming.bitrate_audio', '128k')

        logger.info(f"Combining video and audio:")
        logger.info(f"  Video: {video_file}")
        logger.info(f"  Audio: {audio_file}")
        logger.info(f"  Output: {output_path}")

        # Build ffmpeg command
        cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-i', str(audio_path),
            '-c:v', video_codec,
            '-b:v', video_bitrate,
            '-c:a', audio_codec,
            '-b:a', audio_bitrate,
            '-shortest',  # Match shortest duration (video or audio)
            '-y',  # Overwrite output
            str(output_path)
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"Combined video created: {output_path}")
            return str(output_path)

        except subprocess.CalledProcessError as e:
            logger.error(f"Video combination failed: {e.stderr}")
            raise RuntimeError(f"Video combination failed: {e.stderr}")

    def add_text_overlay(
        self,
        video_file: str,
        text: str,
        output_file: Optional[str] = None,
        position: str = 'bottom',
        font_size: int = 48,
        font_color: str = 'white'
    ) -> str:
        """
        Add text overlay to video

        Args:
            video_file: Path to input video file
            text: Text to overlay
            output_file: Path to output file
            position: Text position ('top', 'bottom', 'center')
            font_size: Font size in pixels
            font_color: Font color

        Returns:
            Path to output video with text overlay
        """
        if output_file is None:
            video_path = Path(video_file)
            output_file = video_path.parent / f"{video_path.stem}_text{video_path.suffix}"

        # Determine text position
        if position == 'bottom':
            y_pos = 'h-th-50'
        elif position == 'top':
            y_pos = '50'
        else:  # center
            y_pos = '(h-th)/2'

        # Build filter string
        filter_str = (
            f"drawtext=text='{text}':"
            f"fontsize={font_size}:"
            f"fontcolor={font_color}:"
            f"x=(w-tw)/2:"
            f"y={y_pos}:"
            f"shadowcolor=black:"
            f"shadowx=2:shadowy=2"
        )

        logger.info(f"Adding text overlay: '{text}'")

        cmd = [
            'ffmpeg',
            '-i', video_file,
            '-vf', filter_str,
            '-codec:a', 'copy',
            '-y',
            output_file
        ]

        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.info(f"Text overlay added: {output_file}")
            return output_file

        except subprocess.CalledProcessError as e:
            logger.error(f"Text overlay failed: {e.stderr}")
            raise RuntimeError(f"Text overlay failed: {e.stderr}")

    def create_looping_video(
        self,
        video_file: str,
        output_file: Optional[str] = None,
        duration: float = 3600
    ) -> str:
        """
        Create a looping video of specified duration

        Args:
            video_file: Path to input video file
            output_file: Path to output file
            duration: Total duration in seconds

        Returns:
            Path to looping video
        """
        if output_file is None:
            video_path = Path(video_file)
            output_file = video_path.parent / f"{video_path.stem}_loop{video_path.suffix}"

        logger.info(f"Creating {duration}s looping video from {video_file}")

        cmd = [
            'ffmpeg',
            '-stream_loop', '-1',  # Loop indefinitely
            '-i', video_file,
            '-t', str(duration),  # Duration
            '-c', 'copy',
            '-y',
            output_file
        ]

        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.info(f"Looping video created: {output_file}")
            return output_file

        except subprocess.CalledProcessError as e:
            logger.error(f"Looping video creation failed: {e.stderr}")
            raise RuntimeError(f"Looping video creation failed: {e.stderr}")

    def optimize_for_streaming(
        self,
        video_file: str,
        output_file: Optional[str] = None
    ) -> str:
        """
        Optimize video for streaming (fast start, proper encoding)

        Args:
            video_file: Path to input video file
            output_file: Path to output file

        Returns:
            Path to optimized video
        """
        if output_file is None:
            video_path = Path(video_file)
            output_file = video_path.parent / f"{video_path.stem}_optimized{video_path.suffix}"

        logger.info(f"Optimizing video for streaming: {video_file}")

        cmd = [
            'ffmpeg',
            '-i', video_file,
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-movflags', '+faststart',  # Enable fast start for web playback
            '-pix_fmt', 'yuv420p',  # Ensure compatibility
            '-y',
            output_file
        ]

        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.info(f"Optimized video created: {output_file}")
            return output_file

        except subprocess.CalledProcessError as e:
            logger.error(f"Video optimization failed: {e.stderr}")
            raise RuntimeError(f"Video optimization failed: {e.stderr}")


def combine_lofi_video(video_file: str, audio_file: str, output_file: str = None) -> str:
    """
    Convenience function to combine video and audio

    Args:
        video_file: Path to video file
        audio_file: Path to audio file
        output_file: Path to output file

    Returns:
        Path to combined video
    """
    composer = VideoComposer()
    return composer.combine_audio_video(video_file, audio_file, output_file)
