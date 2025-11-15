#!/usr/bin/env python3
"""
Lofi Hip Hop Generator - Graphical User Interface
Simple GUI for configuration and execution
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
import sys
import logging
from pathlib import Path
import yaml
import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class TextHandler(logging.Handler):
    """Logging handler that writes to a text widget"""

    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)

        def append():
            self.text_widget.configure(state='normal')
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.configure(state='disabled')
            self.text_widget.yview(tk.END)

        self.text_widget.after(0, append)


class LofiGeneratorGUI:
    """Main GUI application"""

    def __init__(self, root):
        self.root = root
        self.root.title("Lofi Hip Hop Generator 🎵")
        self.root.geometry("900x700")

        # Load configuration
        self.config_file = Path("config.yaml")
        self.load_config()

        # Setup UI
        self.setup_ui()

        # Setup logging to GUI
        self.setup_logging()

        # Current process
        self.current_process = None

    def load_config(self):
        """Load configuration from YAML file"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            # Default config
            self.config = {
                'model': {
                    'sequence_length': 32,
                    'lstm_units': 512,
                    'dropout_rate': 0.3,
                    'epochs': 100,
                    'batch_size': 64
                },
                'generation': {
                    'num_notes': 500,
                    'temperature': 1.0,
                    'tempo': 80
                },
                'video': {
                    'resolution': [1920, 1080],
                    'fps': 30,
                    'duration': 300,
                    'aurora': {
                        'colors': [[0, 255, 159], [0, 191, 255], [138, 43, 226]],
                        'wave_speed': 0.02,
                        'stars_enabled': True,
                        'stars_count': 200
                    }
                },
                'streaming': {
                    'enabled': False,
                    'platform': 'youtube',
                    'rtmp_url': '',
                    'stream_key': ''
                }
            }

    def save_config(self):
        """Save configuration to YAML file"""
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
        logging.info("Configuration saved")

    def setup_ui(self):
        """Setup the user interface"""

        # Create notebook (tabs)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # Tab 1: Generation
        self.tab_generate = ttk.Frame(notebook)
        notebook.add(self.tab_generate, text="🎵 Generate")
        self.setup_generate_tab()

        # Tab 2: Training
        self.tab_train = ttk.Frame(notebook)
        notebook.add(self.tab_train, text="🎓 Train Model")
        self.setup_train_tab()

        # Tab 3: Streaming
        self.tab_stream = ttk.Frame(notebook)
        notebook.add(self.tab_stream, text="📺 Streaming")
        self.setup_stream_tab()

        # Tab 4: Configuration
        self.tab_config = ttk.Frame(notebook)
        notebook.add(self.tab_config, text="⚙️ Settings")
        self.setup_config_tab()

        # Tab 5: Logs
        self.tab_logs = ttk.Frame(notebook)
        notebook.add(self.tab_logs, text="📋 Logs")
        self.setup_logs_tab()

        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_generate_tab(self):
        """Setup generation tab"""
        frame = ttk.Frame(self.tab_generate, padding="10")
        frame.pack(fill='both', expand=True)

        # Title
        title = ttk.Label(frame, text="Generate Lofi Music & Aurora Video", font=('Arial', 14, 'bold'))
        title.pack(pady=10)

        # Parameters
        params_frame = ttk.LabelFrame(frame, text="Parameters", padding="10")
        params_frame.pack(fill='x', pady=10)

        # Number of notes
        ttk.Label(params_frame, text="Number of Notes:").grid(row=0, column=0, sticky='w', pady=5)
        self.notes_var = tk.IntVar(value=self.config['generation'].get('num_notes', 500))
        ttk.Scale(params_frame, from_=100, to=1000, variable=self.notes_var, orient='horizontal', length=200).grid(row=0, column=1, padx=10)
        ttk.Label(params_frame, textvariable=self.notes_var).grid(row=0, column=2)

        # Temperature
        ttk.Label(params_frame, text="Creativity (Temperature):").grid(row=1, column=0, sticky='w', pady=5)
        self.temp_var = tk.DoubleVar(value=self.config['generation'].get('temperature', 1.0))
        ttk.Scale(params_frame, from_=0.5, to=2.0, variable=self.temp_var, orient='horizontal', length=200).grid(row=1, column=1, padx=10)
        ttk.Label(params_frame, textvariable=self.temp_var).grid(row=1, column=2)

        # BPM
        ttk.Label(params_frame, text="Tempo (BPM):").grid(row=2, column=0, sticky='w', pady=5)
        self.bpm_var = tk.IntVar(value=self.config['generation'].get('tempo', 80))
        ttk.Scale(params_frame, from_=60, to=140, variable=self.bpm_var, orient='horizontal', length=200).grid(row=2, column=1, padx=10)
        ttk.Label(params_frame, textvariable=self.bpm_var).grid(row=2, column=2)

        # Duration
        ttk.Label(params_frame, text="Video Duration (seconds):").grid(row=3, column=0, sticky='w', pady=5)
        self.duration_var = tk.IntVar(value=self.config['video'].get('duration', 300))
        ttk.Entry(params_frame, textvariable=self.duration_var, width=10).grid(row=3, column=1, sticky='w', padx=10)

        # Output filename
        ttk.Label(params_frame, text="Output Filename:").grid(row=4, column=0, sticky='w', pady=5)
        self.output_var = tk.StringVar(value="lofi_aurora_output.mp4")
        ttk.Entry(params_frame, textvariable=self.output_var, width=30).grid(row=4, column=1, sticky='w', padx=10)

        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="🎵 Generate Music Only", command=self.generate_music_only, width=25).pack(side='left', padx=5)
        ttk.Button(button_frame, text="🌌 Generate Aurora Only", command=self.generate_aurora_only, width=25).pack(side='left', padx=5)
        ttk.Button(button_frame, text="🎬 Generate Complete Video", command=self.generate_complete, width=25).pack(side='left', padx=5)

        # Info
        info = ttk.Label(frame, text="💡 Tip: Lower temperature = more predictable, Higher temperature = more creative",
                        foreground='gray')
        info.pack(pady=10)

    def setup_train_tab(self):
        """Setup training tab"""
        frame = ttk.Frame(self.tab_train, padding="10")
        frame.pack(fill='both', expand=True)

        # Title
        title = ttk.Label(frame, text="Train Neural Network Model", font=('Arial', 14, 'bold'))
        title.pack(pady=10)

        # MIDI files info
        info_frame = ttk.LabelFrame(frame, text="Training Data", padding="10")
        info_frame.pack(fill='x', pady=10)

        midi_count = len(list(Path("midi_songs").glob("*.mid"))) if Path("midi_songs").exists() else 0
        ttk.Label(info_frame, text=f"MIDI files found: {midi_count}").pack(anchor='w')

        if midi_count == 0:
            ttk.Label(info_frame, text="⚠️ No MIDI files found. Add .mid files to midi_songs/ folder",
                     foreground='red').pack(anchor='w', pady=5)

        ttk.Button(info_frame, text="📁 Open MIDI Folder", command=self.open_midi_folder).pack(pady=5)

        # Training parameters
        params_frame = ttk.LabelFrame(frame, text="Training Parameters", padding="10")
        params_frame.pack(fill='x', pady=10)

        ttk.Label(params_frame, text="Epochs:").grid(row=0, column=0, sticky='w', pady=5)
        self.epochs_var = tk.IntVar(value=self.config['model'].get('epochs', 100))
        ttk.Entry(params_frame, textvariable=self.epochs_var, width=10).grid(row=0, column=1, sticky='w', padx=10)

        ttk.Label(params_frame, text="Batch Size:").grid(row=1, column=0, sticky='w', pady=5)
        self.batch_var = tk.IntVar(value=self.config['model'].get('batch_size', 64))
        ttk.Entry(params_frame, textvariable=self.batch_var, width=10).grid(row=1, column=1, sticky='w', padx=10)

        # Train button
        ttk.Button(frame, text="🎓 Start Training", command=self.train_model, width=30).pack(pady=20)

        # Warning
        warning = ttk.Label(frame, text="⚠️ Training can take several hours depending on your hardware",
                           foreground='orange')
        warning.pack(pady=10)

    def setup_stream_tab(self):
        """Setup streaming tab"""
        frame = ttk.Frame(self.tab_stream, padding="10")
        frame.pack(fill='both', expand=True)

        # Title
        title = ttk.Label(frame, text="Live Streaming Setup", font=('Arial', 14, 'bold'))
        title.pack(pady=10)

        # Platform selection
        platform_frame = ttk.LabelFrame(frame, text="Platform", padding="10")
        platform_frame.pack(fill='x', pady=10)

        self.platform_var = tk.StringVar(value=self.config['streaming'].get('platform', 'youtube'))
        ttk.Radiobutton(platform_frame, text="📺 YouTube Live", variable=self.platform_var,
                       value='youtube').pack(anchor='w')
        ttk.Radiobutton(platform_frame, text="🎮 Twitch", variable=self.platform_var,
                       value='twitch').pack(anchor='w')
        ttk.Radiobutton(platform_frame, text="🔧 Custom RTMP", variable=self.platform_var,
                       value='custom').pack(anchor='w')

        # Stream configuration
        config_frame = ttk.LabelFrame(frame, text="Stream Configuration", padding="10")
        config_frame.pack(fill='x', pady=10)

        ttk.Label(config_frame, text="Stream Key:").grid(row=0, column=0, sticky='w', pady=5)
        self.stream_key_var = tk.StringVar(value=self.config['streaming'].get('stream_key', ''))
        ttk.Entry(config_frame, textvariable=self.stream_key_var, width=40, show='*').grid(row=0, column=1, padx=10)

        ttk.Label(config_frame, text="RTMP URL (for custom):").grid(row=1, column=0, sticky='w', pady=5)
        self.rtmp_url_var = tk.StringVar(value=self.config['streaming'].get('rtmp_url', ''))
        ttk.Entry(config_frame, textvariable=self.rtmp_url_var, width=40).grid(row=1, column=1, padx=10)

        # Video file selection
        video_frame = ttk.LabelFrame(frame, text="Video to Stream", padding="10")
        video_frame.pack(fill='x', pady=10)

        self.stream_video_var = tk.StringVar(value="")
        ttk.Entry(video_frame, textvariable=self.stream_video_var, width=50).pack(side='left', padx=5)
        ttk.Button(video_frame, text="Browse", command=self.browse_video).pack(side='left')

        # Stream buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="▶️ Start Stream", command=self.start_stream, width=20).pack(side='left', padx=5)
        ttk.Button(button_frame, text="⏹️ Stop Stream", command=self.stop_stream, width=20).pack(side='left', padx=5)

        # Instructions
        instructions = ttk.Label(frame, text="📝 Get your stream key from YouTube Studio > Go Live > Stream Key",
                                foreground='gray', wraplength=600)
        instructions.pack(pady=10)

    def setup_config_tab(self):
        """Setup configuration tab"""
        frame = ttk.Frame(self.tab_config, padding="10")
        frame.pack(fill='both', expand=True)

        # Title
        title = ttk.Label(frame, text="Advanced Configuration", font=('Arial', 14, 'bold'))
        title.pack(pady=10)

        # Video settings
        video_frame = ttk.LabelFrame(frame, text="Video Settings", padding="10")
        video_frame.pack(fill='x', pady=10)

        ttk.Label(video_frame, text="Resolution:").grid(row=0, column=0, sticky='w', pady=5)
        self.resolution_var = tk.StringVar(value="1920x1080")
        resolution_combo = ttk.Combobox(video_frame, textvariable=self.resolution_var,
                                       values=["1280x720", "1920x1080", "2560x1440", "3840x2160"], width=15)
        resolution_combo.grid(row=0, column=1, sticky='w', padx=10)

        ttk.Label(video_frame, text="FPS:").grid(row=1, column=0, sticky='w', pady=5)
        self.fps_var = tk.IntVar(value=self.config['video'].get('fps', 30))
        fps_combo = ttk.Combobox(video_frame, textvariable=self.fps_var,
                                values=[24, 30, 60], width=15)
        fps_combo.grid(row=1, column=1, sticky='w', padx=10)

        # Aurora settings
        aurora_frame = ttk.LabelFrame(frame, text="Aurora Settings", padding="10")
        aurora_frame.pack(fill='x', pady=10)

        self.stars_var = tk.BooleanVar(value=self.config['video']['aurora'].get('stars_enabled', True))
        ttk.Checkbutton(aurora_frame, text="Enable Stars", variable=self.stars_var).pack(anchor='w')

        ttk.Label(aurora_frame, text="Number of Stars:").pack(anchor='w')
        self.stars_count_var = tk.IntVar(value=self.config['video']['aurora'].get('stars_count', 200))
        ttk.Scale(aurora_frame, from_=50, to=500, variable=self.stars_count_var,
                 orient='horizontal', length=300).pack(fill='x', padx=10)

        ttk.Label(aurora_frame, text="Wave Speed:").pack(anchor='w', pady=(10, 0))
        self.wave_speed_var = tk.DoubleVar(value=self.config['video']['aurora'].get('wave_speed', 0.02))
        ttk.Scale(aurora_frame, from_=0.01, to=0.05, variable=self.wave_speed_var,
                 orient='horizontal', length=300).pack(fill='x', padx=10)

        # Save button
        ttk.Button(frame, text="💾 Save Configuration", command=self.save_configuration, width=30).pack(pady=20)

    def setup_logs_tab(self):
        """Setup logs tab"""
        frame = ttk.Frame(self.tab_logs, padding="10")
        frame.pack(fill='both', expand=True)

        # Title
        title = ttk.Label(frame, text="Application Logs", font=('Arial', 14, 'bold'))
        title.pack(pady=10)

        # Log text widget
        self.log_text = scrolledtext.ScrolledText(frame, height=25, state='disabled',
                                                   bg='black', fg='lightgreen',
                                                   font=('Consolas', 9))
        self.log_text.pack(fill='both', expand=True, pady=10)

        # Clear button
        ttk.Button(frame, text="🗑️ Clear Logs", command=self.clear_logs).pack()

    def setup_logging(self):
        """Setup logging to GUI"""
        text_handler = TextHandler(self.log_text)
        text_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(text_handler)

        logging.info("Lofi Hip Hop Generator GUI started")
        logging.info(f"Configuration loaded from {self.config_file}")

    # Actions
    def generate_music_only(self):
        """Generate music only"""
        self.run_in_thread(self._generate_music_only)

    def _generate_music_only(self):
        try:
            from music_generator import generate_lofi_music

            self.status_bar.config(text="Generating music...")
            logging.info("Starting music generation...")

            midi_file = generate_lofi_music(
                num_notes=self.notes_var.get(),
                temperature=self.temp_var.get(),
                bpm=self.bpm_var.get()
            )

            self.status_bar.config(text=f"Music generated: {midi_file}")
            logging.info(f"✓ Music generation complete: {midi_file}")
            messagebox.showinfo("Success", f"Music generated:\n{midi_file}")

        except Exception as e:
            logging.error(f"Music generation failed: {e}", exc_info=True)
            messagebox.showerror("Error", f"Music generation failed:\n{str(e)}")
            self.status_bar.config(text="Error")

    def generate_aurora_only(self):
        """Generate aurora video only"""
        self.run_in_thread(self._generate_aurora_only)

    def _generate_aurora_only(self):
        try:
            from aurora_visualizer import create_aurora_video

            self.status_bar.config(text="Generating aurora video...")
            logging.info("Starting aurora generation...")

            video_file = create_aurora_video(
                duration=self.duration_var.get()
            )

            self.status_bar.config(text=f"Aurora generated: {video_file}")
            logging.info(f"✓ Aurora generation complete: {video_file}")
            messagebox.showinfo("Success", f"Aurora video generated:\n{video_file}")

        except Exception as e:
            logging.error(f"Aurora generation failed: {e}", exc_info=True)
            messagebox.showerror("Error", f"Aurora generation failed:\n{str(e)}")
            self.status_bar.config(text="Error")

    def generate_complete(self):
        """Generate complete video"""
        self.run_in_thread(self._generate_complete)

    def _generate_complete(self):
        try:
            from main import LofiStreamGenerator

            self.status_bar.config(text="Generating complete video...")
            logging.info("Starting complete video generation...")

            generator = LofiStreamGenerator()
            results = generator.generate_complete_video(
                num_notes=self.notes_var.get(),
                temperature=self.temp_var.get(),
                duration=self.duration_var.get(),
                output_name=self.output_var.get()
            )

            final_video = results.get('optimized_video') or results.get('final_video')
            self.status_bar.config(text=f"Complete! Video: {final_video}")
            logging.info(f"✓ Complete video generation finished")
            messagebox.showinfo("Success", f"Complete video generated!\n\nFinal video: {final_video}")

        except Exception as e:
            logging.error(f"Complete generation failed: {e}", exc_info=True)
            messagebox.showerror("Error", f"Complete generation failed:\n{str(e)}")
            self.status_bar.config(text="Error")

    def train_model(self):
        """Train the model"""
        if messagebox.askyesno("Confirm", "Training can take several hours. Continue?"):
            self.run_in_thread(self._train_model)

    def _train_model(self):
        try:
            from main import train_model

            self.status_bar.config(text="Training model...")
            logging.info("Starting model training...")

            # Update config with current values
            self.config['model']['epochs'] = self.epochs_var.get()
            self.config['model']['batch_size'] = self.batch_var.get()
            self.save_config()

            train_model()

            self.status_bar.config(text="Training complete!")
            logging.info("✓ Model training complete")
            messagebox.showinfo("Success", "Model training completed!")

        except Exception as e:
            logging.error(f"Training failed: {e}", exc_info=True)
            messagebox.showerror("Error", f"Training failed:\n{str(e)}")
            self.status_bar.config(text="Error")

    def browse_video(self):
        """Browse for video file"""
        filename = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[("Video files", "*.mp4 *.avi *.mkv"), ("All files", "*.*")]
        )
        if filename:
            self.stream_video_var.set(filename)

    def start_stream(self):
        """Start streaming"""
        video_file = self.stream_video_var.get()
        if not video_file:
            messagebox.showwarning("Warning", "Please select a video file to stream")
            return

        if not Path(video_file).exists():
            messagebox.showerror("Error", f"Video file not found: {video_file}")
            return

        stream_key = self.stream_key_var.get()
        if not stream_key:
            messagebox.showwarning("Warning", "Please enter your stream key")
            return

        if messagebox.askyesno("Confirm", f"Start streaming to {self.platform_var.get()}?"):
            self.run_in_thread(lambda: self._start_stream(video_file, stream_key))

    def _start_stream(self, video_file, stream_key):
        try:
            from streamer import stream_video

            self.status_bar.config(text="Streaming...")
            logging.info(f"Starting stream to {self.platform_var.get()}...")

            process = stream_video(
                video_file,
                platform=self.platform_var.get(),
                stream_key=stream_key,
                loop=True
            )

            self.current_process = process
            logging.info("✓ Stream started successfully")
            logging.info("Stream will continue until you click 'Stop Stream'")

        except Exception as e:
            logging.error(f"Streaming failed: {e}", exc_info=True)
            messagebox.showerror("Error", f"Streaming failed:\n{str(e)}")
            self.status_bar.config(text="Error")

    def stop_stream(self):
        """Stop streaming"""
        if self.current_process:
            try:
                self.current_process.terminate()
                self.current_process = None
                self.status_bar.config(text="Stream stopped")
                logging.info("Stream stopped")
                messagebox.showinfo("Info", "Stream stopped")
            except Exception as e:
                logging.error(f"Error stopping stream: {e}")
        else:
            messagebox.showinfo("Info", "No active stream")

    def save_configuration(self):
        """Save current configuration"""
        try:
            # Update config with current values
            self.config['generation']['num_notes'] = self.notes_var.get()
            self.config['generation']['temperature'] = self.temp_var.get()
            self.config['generation']['tempo'] = self.bpm_var.get()
            self.config['video']['duration'] = self.duration_var.get()
            self.config['video']['fps'] = self.fps_var.get()

            # Parse resolution
            res = self.resolution_var.get().split('x')
            self.config['video']['resolution'] = [int(res[0]), int(res[1])]

            # Aurora settings
            self.config['video']['aurora']['stars_enabled'] = self.stars_var.get()
            self.config['video']['aurora']['stars_count'] = self.stars_count_var.get()
            self.config['video']['aurora']['wave_speed'] = self.wave_speed_var.get()

            # Streaming settings
            self.config['streaming']['platform'] = self.platform_var.get()
            self.config['streaming']['stream_key'] = self.stream_key_var.get()
            self.config['streaming']['rtmp_url'] = self.rtmp_url_var.get()

            self.save_config()
            messagebox.showinfo("Success", "Configuration saved successfully!")

        except Exception as e:
            logging.error(f"Failed to save configuration: {e}")
            messagebox.showerror("Error", f"Failed to save configuration:\n{str(e)}")

    def open_midi_folder(self):
        """Open MIDI songs folder"""
        midi_path = Path("midi_songs")
        midi_path.mkdir(exist_ok=True)

        import platform
        import subprocess

        try:
            if platform.system() == "Windows":
                subprocess.Popen(f'explorer "{midi_path.absolute()}"')
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", str(midi_path.absolute())])
            else:  # Linux
                subprocess.Popen(["xdg-open", str(midi_path.absolute())])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder:\n{str(e)}")

    def clear_logs(self):
        """Clear log text"""
        self.log_text.configure(state='normal')
        self.log_text.delete('1.0', tk.END)
        self.log_text.configure(state='disabled')

    def run_in_thread(self, func):
        """Run function in separate thread"""
        thread = threading.Thread(target=func, daemon=True)
        thread.start()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = LofiGeneratorGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
