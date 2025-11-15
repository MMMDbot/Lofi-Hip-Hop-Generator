"""Neural network model for music generation"""
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, Activation, BatchNormalization
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import ModelCheckpoint
import logging
from typing import Tuple, Optional
from pathlib import Path

from config import get_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LofiMusicModel:
    """LSTM-based model for generating lofi hip hop music"""

    def __init__(self, config_path: str = 'config.yaml'):
        self.config = get_config(config_path)
        self.model = None
        self.n_vocab = None

    def create_model(self, network_input: np.ndarray, n_vocab: int) -> Sequential:
        """
        Create the structure of the neural network

        Args:
            network_input: Input data for determining input shape
            n_vocab: Number of unique notes/chords in vocabulary

        Returns:
            Compiled Keras Sequential model
        """
        logger.info("Creating neural network model...")

        # Get configuration parameters
        lstm_units = self.config.get('model.lstm_units', 512)
        dropout_rate = self.config.get('model.dropout_rate', 0.3)
        dense_units = self.config.get('model.dense_units', 256)

        model = Sequential([
            # First LSTM layer
            LSTM(
                lstm_units,
                input_shape=(network_input.shape[1], network_input.shape[2]),
                recurrent_dropout=dropout_rate,
                return_sequences=True
            ),
            # Second LSTM layer
            LSTM(lstm_units, return_sequences=True, recurrent_dropout=dropout_rate),
            # Third LSTM layer
            LSTM(lstm_units),
            # Batch normalization
            BatchNormalization(),
            # Dropout for regularization
            Dropout(dropout_rate),
            # Dense layer
            Dense(dense_units),
            Activation('relu'),
            # Another batch normalization
            BatchNormalization(),
            Dropout(dropout_rate),
            # Output layer
            Dense(n_vocab),
            Activation('softmax')
        ])

        model.compile(loss='categorical_crossentropy', optimizer='adam')

        logger.info(f"Model created with vocabulary size: {n_vocab}")
        logger.info(f"Model parameters: LSTM units={lstm_units}, Dropout={dropout_rate}")

        self.model = model
        self.n_vocab = n_vocab

        return model

    def load_weights(self, weights_file: Optional[str] = None):
        """
        Load pre-trained weights into the model

        Args:
            weights_file: Path to weights file. If None, uses config default.

        Raises:
            FileNotFoundError: If weights file doesn't exist
            ValueError: If model hasn't been created yet
        """
        if self.model is None:
            raise ValueError("Model must be created before loading weights")

        if weights_file is None:
            weights_file = self.config.get('model.weights_file')

        weights_path = Path(weights_file)
        if not weights_path.exists():
            raise FileNotFoundError(f"Weights file not found: {weights_file}")

        logger.info(f"Loading weights from: {weights_file}")
        self.model.load_weights(str(weights_path))
        logger.info("Weights loaded successfully")

    def train(
        self,
        network_input: np.ndarray,
        network_output: np.ndarray,
        epochs: Optional[int] = None,
        batch_size: Optional[int] = None
    ):
        """
        Train the neural network

        Args:
            network_input: Training input data
            network_output: Training output labels
            epochs: Number of training epochs (uses config default if None)
            batch_size: Batch size for training (uses config default if None)
        """
        if self.model is None:
            raise ValueError("Model must be created before training")

        # Get training parameters from config or use provided values
        epochs = epochs or self.config.get('model.epochs', 100)
        batch_size = batch_size or self.config.get('model.batch_size', 64)

        # Setup model checkpoint callback
        output_dir = Path(self.config.get('data.output_directory', 'output'))
        output_dir.mkdir(parents=True, exist_ok=True)

        # Use .keras format for Keras 3.x compatibility
        filepath = str(output_dir / "weights-improvement-{epoch:02d}-{loss:.4f}.keras")
        checkpoint = ModelCheckpoint(
            filepath,
            monitor='loss',
            verbose=1,
            save_best_only=True,
            save_weights_only=False,  # Save full model in .keras format
            mode='min'
        )
        callbacks_list = [checkpoint]

        logger.info(f"Starting training: epochs={epochs}, batch_size={batch_size}")
        logger.info(f"Training data shape: input={network_input.shape}, output={network_output.shape}")

        self.model.fit(
            network_input,
            network_output,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks_list
        )

        logger.info("Training completed")

    def predict(self, input_sequence: np.ndarray, temperature: float = 1.0) -> np.ndarray:
        """
        Generate prediction from input sequence

        Args:
            input_sequence: Input sequence for prediction
            temperature: Sampling temperature (higher = more random)

        Returns:
            Predicted output probabilities
        """
        if self.model is None:
            raise ValueError("Model must be created and loaded before prediction")

        prediction = self.model.predict(input_sequence, verbose=0)

        # Apply temperature sampling
        if temperature != 1.0:
            prediction = np.log(prediction) / temperature
            exp_prediction = np.exp(prediction)
            prediction = exp_prediction / np.sum(exp_prediction)

        return prediction

    def save_model(self, filepath: str):
        """Save the entire model to a file"""
        if self.model is None:
            raise ValueError("Model must be created before saving")

        logger.info(f"Saving model to: {filepath}")
        self.model.save(filepath)
        logger.info("Model saved successfully")

    def load_model(self, filepath: str):
        """Load the entire model from a file"""
        logger.info(f"Loading model from: {filepath}")
        self.model = keras.models.load_model(filepath)
        logger.info("Model loaded successfully")

    def summary(self):
        """Print model summary"""
        if self.model is None:
            logger.warning("Model not created yet")
            return
        self.model.summary()
