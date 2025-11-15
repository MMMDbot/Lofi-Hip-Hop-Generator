"""Data processing for MIDI files"""
import glob
import pickle
import numpy as np
from pathlib import Path
from music21 import converter, instrument, note, chord
from typing import List, Tuple, Dict
import logging

from config import get_config

logger = logging.getLogger(__name__)


class MidiDataProcessor:
    """Process MIDI files for neural network training"""

    def __init__(self, config_path: str = 'config.yaml'):
        self.config = get_config(config_path)
        self.notes = []
        self.pitchnames = []
        self.note_to_int = {}
        self.int_to_note = {}
        self.n_vocab = 0

    def get_notes_from_midi(self, midi_directory: str = None) -> List[str]:
        """
        Extract all notes and chords from MIDI files

        Args:
            midi_directory: Directory containing MIDI files. Uses config default if None.

        Returns:
            List of note/chord representations

        Raises:
            FileNotFoundError: If MIDI directory doesn't exist
            ValueError: If no MIDI files found
        """
        if midi_directory is None:
            midi_directory = self.config.get('data.midi_directory', 'midi_songs')

        midi_path = Path(midi_directory)
        if not midi_path.exists():
            raise FileNotFoundError(f"MIDI directory not found: {midi_directory}")

        midi_files = list(midi_path.glob("*.mid"))
        if not midi_files:
            raise ValueError(f"No MIDI files found in {midi_directory}")

        logger.info(f"Found {len(midi_files)} MIDI files in {midi_directory}")

        notes = []

        for file_path in midi_files:
            try:
                logger.info(f"Parsing: {file_path.name}")
                midi = converter.parse(str(file_path))

                notes_to_parse = None

                # Try to get instrument parts
                try:
                    parts = instrument.partitionByInstrument(midi)
                    if parts and len(parts.parts) > 0:
                        notes_to_parse = parts.parts[0].recurse()
                    else:
                        notes_to_parse = midi.flat.notes
                except (AttributeError, IndexError) as e:
                    # File has notes in a flat structure
                    logger.debug(f"Using flat structure for {file_path.name}: {e}")
                    notes_to_parse = midi.flat.notes

                # Extract notes and chords
                for element in notes_to_parse:
                    if isinstance(element, note.Note):
                        notes.append(str(element.pitch))
                    elif isinstance(element, chord.Chord):
                        # Represent chord as dot-separated note numbers
                        notes.append('.'.join(str(n) for n in element.normalOrder))

            except Exception as e:
                logger.error(f"Error parsing {file_path.name}: {e}")
                continue

        if not notes:
            raise ValueError("No notes extracted from MIDI files")

        logger.info(f"Extracted {len(notes)} notes/chords total")

        self.notes = notes
        return notes

    def save_notes(self, filepath: str = None):
        """
        Save extracted notes to a pickle file

        Args:
            filepath: Path to save notes. Uses config default if None.
        """
        if filepath is None:
            filepath = self.config.get('data.notes_file', 'data/notes')

        # Ensure directory exists
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Saving notes to: {filepath}")
        with open(filepath, 'wb') as f:
            pickle.dump(self.notes, f)

        logger.info(f"Saved {len(self.notes)} notes")

    def load_notes(self, filepath: str = None) -> List[str]:
        """
        Load notes from a pickle file

        Args:
            filepath: Path to notes file. Uses config default if None.

        Returns:
            List of note/chord representations

        Raises:
            FileNotFoundError: If notes file doesn't exist
        """
        if filepath is None:
            filepath = self.config.get('data.notes_file', 'data/notes')

        notes_path = Path(filepath)
        if not notes_path.exists():
            raise FileNotFoundError(
                f"Notes file not found: {filepath}. "
                "Run training first to generate notes."
            )

        logger.info(f"Loading notes from: {filepath}")
        with open(filepath, 'rb') as f:
            self.notes = pickle.load(f)

        logger.info(f"Loaded {len(self.notes)} notes")
        return self.notes

    def prepare_sequences(
        self,
        notes: List[str] = None,
        sequence_length: int = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare input and output sequences for the neural network

        Args:
            notes: List of notes. Uses self.notes if None.
            sequence_length: Length of input sequences. Uses config default if None.

        Returns:
            Tuple of (network_input, network_output)

        Raises:
            ValueError: If vocabulary size is 0 or not enough notes
        """
        if notes is None:
            if not self.notes:
                raise ValueError("No notes available. Load or extract notes first.")
            notes = self.notes

        if sequence_length is None:
            sequence_length = self.config.get('model.sequence_length', 32)

        # Get all unique pitch names
        self.pitchnames = sorted(set(notes))
        self.n_vocab = len(self.pitchnames)

        if self.n_vocab == 0:
            raise ValueError("Vocabulary size is 0. No valid notes found.")

        logger.info(f"Vocabulary size: {self.n_vocab}")
        logger.info(f"Sequence length: {sequence_length}")

        # Create mapping dictionaries
        self.note_to_int = {note: number for number, note in enumerate(self.pitchnames)}
        self.int_to_note = {number: note for number, note in enumerate(self.pitchnames)}

        # Create input sequences and corresponding outputs
        network_input = []
        network_output = []

        if len(notes) <= sequence_length:
            raise ValueError(
                f"Not enough notes ({len(notes)}) for sequence length ({sequence_length})"
            )

        for i in range(len(notes) - sequence_length):
            sequence_in = notes[i:i + sequence_length]
            sequence_out = notes[i + sequence_length]
            network_input.append([self.note_to_int[char] for char in sequence_in])
            network_output.append(self.note_to_int[sequence_out])

        n_patterns = len(network_input)
        logger.info(f"Created {n_patterns} training patterns")

        # Reshape and normalize input
        network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
        network_input = network_input / float(self.n_vocab)

        # One-hot encode output
        network_output = np.array(network_output)

        # Use keras utility for one-hot encoding
        from tensorflow.keras.utils import to_categorical
        network_output = to_categorical(network_output, num_classes=self.n_vocab)

        logger.info(f"Input shape: {network_input.shape}")
        logger.info(f"Output shape: {network_output.shape}")

        return network_input, network_output

    def prepare_prediction_sequences(
        self,
        notes: List[str] = None,
        sequence_length: int = None
    ) -> Tuple[List[List[int]], np.ndarray]:
        """
        Prepare sequences for prediction/generation

        Args:
            notes: List of notes. Uses self.notes if None.
            sequence_length: Length of input sequences. Uses config default if None.

        Returns:
            Tuple of (network_input, normalized_input)
        """
        if notes is None:
            if not self.notes:
                raise ValueError("No notes available. Load or extract notes first.")
            notes = self.notes

        if sequence_length is None:
            sequence_length = self.config.get('model.sequence_length', 32)

        # Get all unique pitch names
        self.pitchnames = sorted(set(notes))
        self.n_vocab = len(self.pitchnames)

        if self.n_vocab == 0:
            raise ValueError("Vocabulary size is 0. No valid notes found.")

        # Create mapping
        self.note_to_int = {note: number for number, note in enumerate(self.pitchnames)}
        self.int_to_note = {number: note for number, note in enumerate(self.pitchnames)}

        network_input = []
        for i in range(len(notes) - sequence_length):
            sequence_in = notes[i:i + sequence_length]
            network_input.append([self.note_to_int[char] for char in sequence_in])

        n_patterns = len(network_input)

        # Reshape and normalize
        normalized_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
        normalized_input = normalized_input / float(self.n_vocab)

        logger.info(f"Prepared {n_patterns} sequences for prediction")

        return network_input, normalized_input

    def get_vocabulary_size(self) -> int:
        """Get the size of the note vocabulary"""
        return self.n_vocab

    def note_to_number(self, note: str) -> int:
        """Convert note to integer"""
        return self.note_to_int.get(note, 0)

    def number_to_note(self, number: int) -> str:
        """Convert integer to note"""
        return self.int_to_note.get(number, '')
