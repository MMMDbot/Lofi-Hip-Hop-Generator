"""Live streaming functionality"""
import subprocess
import threading
import time
from pathlib import Path
from typing import Optional
import logging

from config import get_config

logger = logging.getLogger(__name__)


class LiveStreamer:
    """Stream video to various platforms"""

    def __init__(self, config_path: str = 'config.yaml'):
        self.config = get_config(config_path)
        self.streaming_process = None
        self.is_streaming = False

    def stream_to_rtmp(
        self,
        video_file: str,
        rtmp_url: Optional[str] = None,
        stream_key: Optional[str] = None,
        loop: bool = True
    ) -> subprocess.Popen:
        """
        Stream video to RTMP server (YouTube, Twitch, etc.)

        Args:
            video_file: Path to video file to stream
            rtmp_url: RTMP server URL. Uses config if None.
            stream_key: Stream key. Uses config if None.
            loop: Whether to loop the video

        Returns:
            Subprocess handle for the streaming process

        Raises:
            ValueError: If RTMP URL or stream key not provided
            FileNotFoundError: If video file doesn't exist
        """
        video_path = Path(video_file)
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_file}")

        # Get streaming configuration
        if rtmp_url is None:
            rtmp_url = self.config.get('streaming.rtmp_url')
        if stream_key is None:
            stream_key = self.config.get('streaming.stream_key')

        if not rtmp_url or not stream_key:
            raise ValueError(
                "RTMP URL and stream key must be provided. "
                "Set them in config.yaml or pass as arguments."
            )

        full_rtmp_url = f"{rtmp_url}/{stream_key}"

        logger.info(f"Starting stream to: {rtmp_url}")
        logger.info(f"Video source: {video_file}")

        # Build ffmpeg command for streaming
        cmd = [
            'ffmpeg',
            '-re',  # Read input at native frame rate
        ]

        if loop:
            cmd.extend(['-stream_loop', '-1'])  # Loop indefinitely

        cmd.extend([
            '-i', str(video_path),
            '-c:v', 'libx264',
            '-preset', 'veryfast',
            '-b:v', self.config.get('streaming.bitrate_video', '4500k'),
            '-maxrate', self.config.get('streaming.bitrate_video', '4500k'),
            '-bufsize', '9000k',
            '-pix_fmt', 'yuv420p',
            '-g', '60',  # Keyframe interval
            '-c:a', 'aac',
            '-b:a', self.config.get('streaming.bitrate_audio', '128k'),
            '-ar', '44100',
            '-f', 'flv',  # FLV format for RTMP
            full_rtmp_url
        ])

        try:
            # Start streaming process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            self.streaming_process = process
            self.is_streaming = True

            logger.info("Streaming started successfully")
            logger.info("Press Ctrl+C or call stop_stream() to stop")

            return process

        except Exception as e:
            logger.error(f"Failed to start stream: {e}")
            raise RuntimeError(f"Streaming failed: {e}")

    def stream_youtube(
        self,
        video_file: str,
        stream_key: Optional[str] = None,
        loop: bool = True
    ) -> subprocess.Popen:
        """
        Stream to YouTube Live

        Args:
            video_file: Path to video file
            stream_key: YouTube stream key
            loop: Whether to loop the video

        Returns:
            Subprocess handle for the streaming process
        """
        rtmp_url = "rtmp://a.rtmp.youtube.com/live2"
        return self.stream_to_rtmp(video_file, rtmp_url, stream_key, loop)

    def stream_twitch(
        self,
        video_file: str,
        stream_key: Optional[str] = None,
        loop: bool = True
    ) -> subprocess.Popen:
        """
        Stream to Twitch

        Args:
            video_file: Path to video file
            stream_key: Twitch stream key
            loop: Whether to loop the video

        Returns:
            Subprocess handle for the streaming process
        """
        rtmp_url = "rtmp://live.twitch.tv/app"
        return self.stream_to_rtmp(video_file, rtmp_url, stream_key, loop)

    def stop_stream(self):
        """Stop the current streaming process"""
        if self.streaming_process and self.is_streaming:
            logger.info("Stopping stream...")
            self.streaming_process.terminate()

            # Wait for graceful shutdown
            try:
                self.streaming_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                logger.warning("Stream did not stop gracefully, forcing...")
                self.streaming_process.kill()

            self.is_streaming = False
            logger.info("Stream stopped")
        else:
            logger.info("No active stream to stop")

    def monitor_stream(self, interval: int = 5):
        """
        Monitor streaming process and log status

        Args:
            interval: Check interval in seconds
        """
        if not self.streaming_process or not self.is_streaming:
            logger.warning("No active stream to monitor")
            return

        logger.info(f"Monitoring stream (checking every {interval}s)...")

        while self.is_streaming:
            # Check if process is still running
            if self.streaming_process.poll() is not None:
                logger.error("Streaming process terminated unexpectedly")
                self.is_streaming = False

                # Get error output
                _, stderr = self.streaming_process.communicate()
                if stderr:
                    logger.error(f"Stream error: {stderr}")
                break

            time.sleep(interval)

    def get_stream_status(self) -> dict:
        """
        Get current streaming status

        Returns:
            Dictionary with streaming status information
        """
        return {
            'is_streaming': self.is_streaming,
            'process_id': self.streaming_process.pid if self.streaming_process else None,
            'process_running': (
                self.streaming_process.poll() is None
                if self.streaming_process else False
            )
        }


class StreamScheduler:
    """Schedule and manage continuous streaming"""

    def __init__(self, config_path: str = 'config.yaml'):
        self.config = get_config(config_path)
        self.streamer = LiveStreamer(config_path)
        self.scheduler_thread = None
        self.running = False

    def start_continuous_stream(
        self,
        video_file: str,
        platform: str = 'youtube',
        stream_key: Optional[str] = None
    ):
        """
        Start continuous streaming with automatic restart on failure

        Args:
            video_file: Path to video file
            platform: Streaming platform ('youtube', 'twitch', or 'rtmp')
            stream_key: Stream key for the platform
        """
        self.running = True

        def stream_loop():
            while self.running:
                try:
                    logger.info(f"Starting stream to {platform}...")

                    if platform == 'youtube':
                        process = self.streamer.stream_youtube(video_file, stream_key)
                    elif platform == 'twitch':
                        process = self.streamer.stream_twitch(video_file, stream_key)
                    else:  # rtmp
                        rtmp_url = self.config.get('streaming.rtmp_url')
                        process = self.streamer.stream_to_rtmp(
                            video_file, rtmp_url, stream_key
                        )

                    # Wait for process to complete
                    process.wait()

                    if self.running:
                        logger.warning("Stream ended unexpectedly, restarting in 10s...")
                        time.sleep(10)

                except Exception as e:
                    logger.error(f"Streaming error: {e}")
                    if self.running:
                        logger.info("Retrying in 30 seconds...")
                        time.sleep(30)

        # Start streaming in a separate thread
        self.scheduler_thread = threading.Thread(target=stream_loop, daemon=True)
        self.scheduler_thread.start()

        logger.info("Continuous streaming started")

    def stop_continuous_stream(self):
        """Stop continuous streaming"""
        self.running = False
        self.streamer.stop_stream()

        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=10)

        logger.info("Continuous streaming stopped")


def stream_video(
    video_file: str,
    platform: str = 'youtube',
    stream_key: str = None,
    loop: bool = True
) -> subprocess.Popen:
    """
    Convenience function to stream video

    Args:
        video_file: Path to video file
        platform: Platform to stream to
        stream_key: Stream key
        loop: Whether to loop the video

    Returns:
        Streaming process handle
    """
    streamer = LiveStreamer()

    if platform == 'youtube':
        return streamer.stream_youtube(video_file, stream_key, loop)
    elif platform == 'twitch':
        return streamer.stream_twitch(video_file, stream_key, loop)
    else:
        raise ValueError(f"Unknown platform: {platform}")
