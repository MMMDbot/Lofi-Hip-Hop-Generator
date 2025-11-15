"""Music generation module"""
import numpy as np
from pathlib import Path
from music21 import instrument, note, stream, chord, tempo
from typing import List, Optional
import logging

from config import get_config
from model import LofiMusicModel
from data_processor import MidiDataProcessor

logger = logging.getLogger(__name__)


class MusicGenerator:
    """Generate music using trained LSTM model"""

    def __init__(self, config_path: str = 'config.yaml'):
        self.config = get_config(config_path)
        self.model = LofiMusicModel(config_path)
        self.data_processor = MidiDataProcessor(config_path)

    def generate_notes(
        self,
        num_notes: Optional[int] = None,
        temperature: Optional[float] = None,
        start_index: Optional[int] = None
    ) -> List[str]:
        """
        Generate notes using the trained model

        Args:
            num_notes: Number of notes to generate. Uses config default if None.
            temperature: Sampling temperature. Uses config default if None.
            start_index: Starting index in the training data. Random if None.

        Returns:
            List of generated note/chord representations
        """
        # Load notes
        try:
            self.data_processor.load_notes()
        except FileNotFoundError as e:
            logger.error(str(e))
            raise

        notes = self.data_processor.notes

        # Prepare sequences
        network_input, normalized_input = self.data_processor.prepare_prediction_sequences()

        # Get vocabulary info
        n_vocab = self.data_processor.get_vocabulary_size()
        sequence_length = self.config.get('model.sequence_length', 32)

        # Create and load model
        self.model.create_model(normalized_input, n_vocab)
        try:
            self.model.load_weights()
        except FileNotFoundError as e:
            logger.error(str(e))
            raise

        # Get generation parameters
        if num_notes is None:
            num_notes = self.config.get('generation.num_notes', 500)

        if temperature is None:
            temperature = self.config.get('generation.temperature', 1.0)

        # Pick random starting sequence
        if start_index is None:
            start_index = np.random.randint(0, len(network_input) - 1)

        logger.info(f"Generating {num_notes} notes with temperature {temperature}")
        logger.info(f"Starting from index {start_index}")

        pattern = network_input[start_index]
        prediction_output = []

        # Generate notes
        for i in range(num_notes):
            # Prepare input for prediction
            prediction_input = np.reshape(pattern, (1, len(pattern), 1))
            prediction_input = prediction_input / float(n_vocab)

            # Get prediction
            prediction = self.model.predict(prediction_input, temperature)

            # Sample from the distribution
            if temperature > 0:
                # Probabilistic sampling
                index = np.random.choice(len(prediction[0]), p=prediction[0])
            else:
                # Greedy sampling
                index = np.argmax(prediction)

            # Convert to note
            result = self.data_processor.number_to_note(index)
            prediction_output.append(result)

            # Update pattern for next iteration
            pattern.append(index)
            pattern = pattern[1:]

            # Log progress
            if (i + 1) % 50 == 0:
                logger.info(f"Generated {i + 1}/{num_notes} notes")

        logger.info("Note generation completed")
        return prediction_output

    def create_midi(
        self,
        prediction_output: List[str],
        output_filename: Optional[str] = None,
        bpm: Optional[int] = None
    ) -> str:
        """
        Convert generated notes to a MIDI file

        Args:
            prediction_output: List of note/chord representations
            output_filename: Output MIDI filename. Auto-generated if None.
            bpm: Tempo in beats per minute. Uses config default if None.

        Returns:
            Path to created MIDI file
        """
        if bpm is None:
            bpm = self.config.get('generation.tempo', 80)

        if output_filename is None:
            output_dir = Path(self.config.get('data.output_directory', 'output'))
            output_filename = output_dir / self.config.get_output_filename('midi')

        output_path = Path(output_filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Creating MIDI file: {output_path}")

        offset = 0
        output_notes = []

        # Create note and chord objects
        for pattern in prediction_output:
            # Check if pattern is a chord (contains dots or is all digits)
            if ('.' in pattern) or pattern.isdigit():
                # It's a chord
                notes_in_chord = pattern.split('.')
                notes = []
                for current_note in notes_in_chord:
                    try:
                        new_note = note.Note(int(current_note))
                        new_note.storedInstrument = instrument.Piano()
                        notes.append(new_note)
                    except (ValueError, TypeError) as e:
                        logger.warning(f"Skipping invalid chord note: {current_note} - {e}")
                        continue

                if notes:  # Only create chord if we have valid notes
                    new_chord = chord.Chord(notes)
                    new_chord.offset = offset
                    output_notes.append(new_chord)
            else:
                # It's a single note
                try:
                    new_note = note.Note(pattern)
                    new_note.offset = offset
                    new_note.storedInstrument = instrument.Piano()
                    output_notes.append(new_note)
                except Exception as e:
                    logger.warning(f"Skipping invalid note: {pattern} - {e}")
                    continue

            # Increment offset (0.5 = eighth note spacing)
            offset += 0.5

        # Create stream and add tempo
        midi_stream = stream.Stream(output_notes)
        midi_stream.insert(0, tempo.MetronomeMark(number=bpm))

        # Write to MIDI file
        midi_stream.write('midi', fp=str(output_path))

        logger.info(f"MIDI file created: {output_path}")
        logger.info(f"Total notes/chords: {len(output_notes)}")

        return str(output_path)

    def generate_music(
        self,
        num_notes: Optional[int] = None,
        temperature: Optional[float] = None,
        output_filename: Optional[str] = None,
        bpm: Optional[int] = None
    ) -> str:
        """
        Complete music generation pipeline

        Args:
            num_notes: Number of notes to generate
            temperature: Sampling temperature
            output_filename: Output MIDI filename
            bpm: Tempo in beats per minute

        Returns:
            Path to created MIDI file
        """
        logger.info("=== Starting Music Generation ===")

        # Generate notes
        notes = self.generate_notes(num_notes, temperature)

        # Create MIDI file
        midi_path = self.create_midi(notes, output_filename, bpm)

        logger.info("=== Music Generation Complete ===")

        return midi_path


def generate_lofi_music(
    num_notes: int = 500,
    temperature: float = 1.0,
    output_file: str = None,
    bpm: int = 80
) -> str:
    """
    Convenience function to generate lofi music

    Args:
        num_notes: Number of notes to generate
        temperature: Sampling temperature (0.5-2.0)
        output_file: Output MIDI file path
        bpm: Tempo in beats per minute

    Returns:
        Path to generated MIDI file
    """
    generator = MusicGenerator()
    return generator.generate_music(num_notes, temperature, output_file, bpm)
