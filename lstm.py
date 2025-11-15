"""
This module prepares midi file data and feeds it to the neural network for training

UPDATED: Now uses modern TensorFlow/Keras and modular architecture
For new code, use the modules in model.py, data_processor.py, etc.
This file is kept for backward compatibility.
"""
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    # Use new modular architecture
    from data_processor import MidiDataProcessor
    from model import LofiMusicModel
    from config import get_config

    def train_network(config_path='config.yaml'):
        """
        Train a Neural Network to generate music

        This function now uses the new modular architecture.
        See model.py and data_processor.py for implementation details.
        """
        logger.info("Starting training with new modular architecture...")

        config = get_config(config_path)

        # Process MIDI files
        logger.info("Processing MIDI files...")
        processor = MidiDataProcessor(config_path)
        notes = processor.get_notes_from_midi()
        processor.save_notes()

        # Prepare sequences
        logger.info("Preparing training sequences...")
        network_input, network_output = processor.prepare_sequences(notes)

        # Create and train model
        logger.info("Creating and training model...")
        model = LofiMusicModel(config_path)
        model.create_model(network_input, processor.get_vocabulary_size())

        # Try to load existing weights if available
        try:
            model.load_weights()
            logger.info("Loaded existing weights for continued training")
        except FileNotFoundError:
            logger.info("No existing weights found, training from scratch")

        model.train(network_input, network_output)

        logger.info("Training complete!")

        return model

except ImportError as e:
    logger.error(f"Failed to import new modules: {e}")
    logger.error("Falling back to legacy implementation...")

    # Legacy fallback implementation
    import glob
    import pickle
    import numpy
    from music21 import converter, instrument, note, chord
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Dropout, LSTM, Activation, BatchNormalization as BatchNorm
    from tensorflow.keras.utils import to_categorical
    from tensorflow.keras.callbacks import ModelCheckpoint

    def train_network():
        """Legacy training function"""
        notes = get_notes()
        n_vocab = len(set(notes))

        if n_vocab == 0:
            raise ValueError("No notes found!")

        network_input, network_output = prepare_sequences(notes, n_vocab)
        model = create_network(network_input, n_vocab)
        train(model, network_input, network_output)

    def get_notes():
        """Get all notes and chords from MIDI files"""
        notes = []

        for file in glob.glob("midi_songs/*.mid"):
            try:
                midi = converter.parse(file)
                print("Parsing %s" % file)

                notes_to_parse = None

                try:
                    s2 = instrument.partitionByInstrument(midi)
                    if s2 and len(s2.parts) > 0:
                        notes_to_parse = s2.parts[0].recurse()
                    else:
                        notes_to_parse = midi.flat.notes
                except (AttributeError, IndexError):
                    notes_to_parse = midi.flat.notes

                for element in notes_to_parse:
                    if isinstance(element, note.Note):
                        notes.append(str(element.pitch))
                    elif isinstance(element, chord.Chord):
                        notes.append('.'.join(str(n) for n in element.normalOrder))

            except Exception as e:
                print(f"Error parsing {file}: {e}")
                continue

        with open('data/notes', 'wb') as filepath:
            pickle.dump(notes, filepath)

        return notes

    def prepare_sequences(notes, n_vocab):
        """Prepare the sequences used by the Neural Network"""
        sequence_length = 32
        pitchnames = sorted(set(item for item in notes))
        note_to_int = dict((note, number) for number, note in enumerate(pitchnames))

        network_input = []
        network_output = []

        for i in range(0, len(notes) - sequence_length, 1):
            sequence_in = notes[i:i + sequence_length]
            sequence_out = notes[i + sequence_length]
            network_input.append([note_to_int[char] for char in sequence_in])
            network_output.append(note_to_int[sequence_out])

        n_patterns = len(network_input)
        network_input = numpy.reshape(network_input, (n_patterns, sequence_length, 1))
        network_input = network_input / float(n_vocab)
        network_output = to_categorical(network_output)

        return (network_input, network_output)

    def create_network(network_input, n_vocab):
        """Create the structure of the neural network"""
        model = Sequential()
        model.add(LSTM(512, input_shape=(network_input.shape[1], network_input.shape[2]),
                      recurrent_dropout=0.3, return_sequences=True))
        model.add(LSTM(512, return_sequences=True, recurrent_dropout=0.3))
        model.add(LSTM(512))
        model.add(BatchNorm())
        model.add(Dropout(0.3))
        model.add(Dense(256))
        model.add(Activation('relu'))
        model.add(BatchNorm())
        model.add(Dropout(0.3))
        model.add(Dense(n_vocab))
        model.add(Activation('softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam')

        try:
            model.load_weights('lofi-hip-hop-weights-improvement-100-0.6290.hdf5')
            print("Loaded existing weights")
        except:
            print("No existing weights found, training from scratch")

        return model

    def train(model, network_input, network_output):
        """Train the neural network"""
        filepath = "output/weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
        checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1,
                                    save_best_only=True, mode='min')
        callbacks_list = [checkpoint]

        model.fit(network_input, network_output, epochs=100, batch_size=64,
                 callbacks=callbacks_list)

if __name__ == '__main__':
    train_network()
