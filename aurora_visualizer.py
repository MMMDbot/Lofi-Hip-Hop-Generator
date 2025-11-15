"""Aurora Borealis visualization generator"""
import numpy as np
import cv2
from pathlib import Path
from typing import List, Tuple, Optional
import logging

from config import get_config

logger = logging.getLogger(__name__)


class AuroraVisualizer:
    """Generate Aurora Borealis visualization videos"""

    def __init__(self, config_path: str = 'config.yaml'):
        self.config = get_config(config_path)
        self.width, self.height = self.config.get('video.resolution', [1920, 1080])
        self.fps = self.config.get('video.fps', 30)

    def generate_stars(self, num_stars: int) -> np.ndarray:
        """
        Generate random star positions

        Args:
            num_stars: Number of stars to generate

        Returns:
            Array of star positions (x, y, brightness)
        """
        stars = np.zeros((num_stars, 3))
        stars[:, 0] = np.random.randint(0, self.width, num_stars)  # x position
        stars[:, 1] = np.random.randint(0, self.height // 2, num_stars)  # y position (top half)
        stars[:, 2] = np.random.uniform(0.3, 1.0, num_stars)  # brightness

        return stars

    def draw_stars(self, frame: np.ndarray, stars: np.ndarray, twinkle: float = 0.0):
        """
        Draw stars on the frame

        Args:
            frame: Image frame to draw on
            stars: Array of star positions
            twinkle: Twinkle phase (0-2π)
        """
        for x, y, brightness in stars:
            # Add twinkle effect
            current_brightness = brightness * (0.7 + 0.3 * np.sin(twinkle + np.random.random() * 2 * np.pi))

            # Draw star
            color = int(255 * current_brightness)
            cv2.circle(frame, (int(x), int(y)), 1, (color, color, color), -1)

            # Occasionally draw a brighter star
            if np.random.random() < 0.1:
                cv2.circle(frame, (int(x), int(y)), 2, (color, color, color), -1)

    def create_aurora_wave(
        self,
        frame_num: int,
        wave_index: int,
        total_waves: int,
        colors: List[List[int]],
        speed: float,
        complexity: int
    ) -> np.ndarray:
        """
        Create a single aurora wave pattern

        Args:
            frame_num: Current frame number
            wave_index: Index of this wave
            total_waves: Total number of waves
            colors: List of RGB color values
            speed: Animation speed
            complexity: Number of frequency components

        Returns:
            RGBA image of the aurora wave
        """
        # Create empty RGBA image
        wave = np.zeros((self.height, self.width, 4), dtype=np.uint8)

        # Select color for this wave
        color = colors[wave_index % len(colors)]

        # Generate wave pattern
        x = np.linspace(0, 4 * np.pi, self.width)
        time_offset = frame_num * speed

        # Base wave position (vertical center varies by wave)
        base_y = self.height * (0.3 + 0.1 * wave_index / total_waves)

        # Complex wave pattern with multiple frequencies
        y_wave = base_y
        for freq in range(1, complexity + 1):
            amplitude = 50 / freq
            phase = time_offset + wave_index * np.pi / 2
            y_wave += amplitude * np.sin(freq * x + phase)

        # Draw the aurora wave with gradient
        for i in range(self.width):
            center_y = int(y_wave[i])

            # Create vertical gradient
            wave_height = int(100 + 50 * np.sin(x[i] + time_offset))

            for dy in range(-wave_height, wave_height):
                y = center_y + dy
                if 0 <= y < self.height:
                    # Calculate alpha based on distance from center
                    distance_factor = 1.0 - abs(dy) / wave_height
                    alpha = int(255 * distance_factor * 0.6)

                    # Add some horizontal variation
                    color_variation = 1.0 + 0.2 * np.sin(x[i] * 3 + time_offset)

                    # Set pixel color with alpha blending
                    wave[y, i] = [
                        int(color[0] * color_variation),
                        int(color[1] * color_variation),
                        int(color[2] * color_variation),
                        alpha
                    ]

        return wave

    def blend_aurora_waves(self, background: np.ndarray, waves: List[np.ndarray]) -> np.ndarray:
        """
        Blend multiple aurora waves onto background

        Args:
            background: Background image (RGB)
            waves: List of aurora wave images (RGBA)

        Returns:
            Blended image
        """
        result = background.copy()

        for wave in waves:
            # Extract alpha channel
            alpha = wave[:, :, 3] / 255.0
            alpha = np.stack([alpha] * 3, axis=2)

            # Blend wave onto result
            wave_rgb = wave[:, :, :3]
            result = (result * (1 - alpha) + wave_rgb * alpha).astype(np.uint8)

        return result

    def create_gradient_background(self, top_color: Tuple[int, int, int], bottom_color: Tuple[int, int, int]) -> np.ndarray:
        """
        Create a gradient background

        Args:
            top_color: RGB color for top of image
            bottom_color: RGB color for bottom of image

        Returns:
            Gradient background image
        """
        background = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        for y in range(self.height):
            factor = y / self.height
            color = [
                int(top_color[0] * (1 - factor) + bottom_color[0] * factor),
                int(top_color[1] * (1 - factor) + bottom_color[1] * factor),
                int(top_color[2] * (1 - factor) + bottom_color[2] * factor)
            ]
            background[y, :] = color

        return background

    def generate_frame(self, frame_num: int, stars: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Generate a single frame of aurora visualization

        Args:
            frame_num: Frame number
            stars: Star positions array (generated if None)

        Returns:
            RGB image frame
        """
        # Get aurora configuration
        aurora_config = self.config.get('video.aurora', {})
        colors = aurora_config.get('colors', [[0, 255, 159], [0, 191, 255], [138, 43, 226]])
        speed = aurora_config.get('wave_speed', 0.02)
        complexity = aurora_config.get('wave_complexity', 3)
        brightness = aurora_config.get('brightness', 0.8)
        stars_enabled = aurora_config.get('stars_enabled', True)
        stars_count = aurora_config.get('stars_count', 200)

        # Create gradient background (dark sky)
        top_color = (5, 5, 20)  # Dark blue-black
        bottom_color = (20, 10, 30)  # Slightly lighter purple-black
        frame = self.create_gradient_background(top_color, bottom_color)

        # Add stars
        if stars_enabled:
            if stars is None:
                stars = self.generate_stars(stars_count)
            twinkle = frame_num * 0.05
            self.draw_stars(frame, stars, twinkle)

        # Generate aurora waves
        num_waves = len(colors)
        waves = []
        for i in range(num_waves):
            wave = self.create_aurora_wave(frame_num, i, num_waves, colors, speed, complexity)
            waves.append(wave)

        # Blend waves onto background
        frame = self.blend_aurora_waves(frame, waves)

        # Apply brightness adjustment
        frame = (frame * brightness).astype(np.uint8)

        return frame

    def generate_video(
        self,
        output_filename: Optional[str] = None,
        duration: Optional[float] = None,
        audio_file: Optional[str] = None
    ) -> str:
        """
        Generate complete aurora visualization video

        Args:
            output_filename: Output video filename. Auto-generated if None.
            duration: Video duration in seconds. Uses config default if None.
            audio_file: Optional audio file to sync duration with

        Returns:
            Path to created video file
        """
        if duration is None:
            duration = self.config.get('video.duration', 300)

        if output_filename is None:
            output_dir = Path(self.config.get('data.output_directory', 'output'))
            output_filename = output_dir / self.config.get_output_filename('video')

        output_path = Path(output_filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # If audio file provided, match its duration
        if audio_file:
            import soundfile as sf
            try:
                audio_data, sample_rate = sf.read(audio_file)
                duration = len(audio_data) / sample_rate
                logger.info(f"Matching audio duration: {duration:.2f} seconds")
            except Exception as e:
                logger.warning(f"Could not read audio file duration: {e}")

        total_frames = int(duration * self.fps)
        logger.info(f"Generating aurora video: {output_path}")
        logger.info(f"Duration: {duration:.2f}s, FPS: {self.fps}, Total frames: {total_frames}")

        # Setup video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(
            str(output_path),
            fourcc,
            self.fps,
            (self.width, self.height)
        )

        # Generate stars once for consistency
        stars_enabled = self.config.get('video.aurora.stars_enabled', True)
        stars_count = self.config.get('video.aurora.stars_count', 200)
        stars = self.generate_stars(stars_count) if stars_enabled else None

        # Generate frames
        for frame_num in range(total_frames):
            frame = self.generate_frame(frame_num, stars)

            # Convert RGB to BGR for OpenCV
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            video_writer.write(frame_bgr)

            # Log progress
            if (frame_num + 1) % 30 == 0:
                progress = (frame_num + 1) / total_frames * 100
                logger.info(f"Progress: {progress:.1f}% ({frame_num + 1}/{total_frames} frames)")

        video_writer.release()
        logger.info(f"Aurora video created: {output_path}")

        return str(output_path)


def create_aurora_video(duration: float = 300, output_file: str = None) -> str:
    """
    Convenience function to create aurora video

    Args:
        duration: Video duration in seconds
        output_file: Output video file path

    Returns:
        Path to generated video
    """
    visualizer = AuroraVisualizer()
    return visualizer.generate_video(output_file, duration)
