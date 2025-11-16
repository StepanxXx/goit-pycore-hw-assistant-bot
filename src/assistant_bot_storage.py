"""Persistence helpers for the assistant bot."""

import pickle
from pathlib import Path


class AssistantBotStorage:
    """Handles serialization of the data to disk."""

    def __init__(self, data_dir: Path | None = None) -> None:
        base_dir = Path(__file__).resolve().parent.parent
        self.data_dir = data_dir or (base_dir / "data")
        self.address_book_file = self.data_dir / "assistant_bot.pkl"

    def ensure_data_dir(self) -> None:
        """Ensure that the storage directory for the data exists."""
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def save_data(self, data, filename: Path | None = None):
        """Persist the data to disk."""
        self.ensure_data_dir()
        target_file = filename or self.address_book_file
        with target_file.open("wb") as file_handle:
            pickle.dump(data, file_handle)

    def load_data(self, filename: Path | None = None):
        """Load the data from disk or return a None if no file exists."""
        self.ensure_data_dir()
        target_file = filename or self.address_book_file
        try:
            with target_file.open("rb") as file_handle:
                return pickle.load(file_handle)
        except FileNotFoundError:
            return None
