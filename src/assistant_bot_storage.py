"""Persistence helpers for the assistant bot."""

import pickle
from pathlib import Path
from src.notes import Notes
from src.address_book import AddressBook


class AssistantBotStorage:
    """Handles serialization of the address book to disk."""

    def __init__(self, data_dir: Path | None = None) -> None:
        base_dir = Path(__file__).resolve().parent.parent
        self.data_dir = data_dir or (base_dir / "data")
        self.address_book_file = self.data_dir / "assistant_bot.pkl"

    def ensure_data_dir(self) -> None:
        """Ensure that the storage directory for the address book exists."""
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def save_data(self, data: tuple, filename: Path | None = None):
        """Persist the address book to disk."""
        self.ensure_data_dir()
        target_file = filename or self.address_book_file
        with target_file.open("wb") as file_handle:
            pickle.dump(data, file_handle)

    def load_data(self, filename: Path | None = None):
        """Load the address book from disk or return a new one if no file exists."""
        self.ensure_data_dir()
        target_file = filename or self.address_book_file
        try:
            with target_file.open("rb") as file_handle:
                return pickle.load(file_handle)
        except FileNotFoundError:
            return (AddressBook(), Notes())
