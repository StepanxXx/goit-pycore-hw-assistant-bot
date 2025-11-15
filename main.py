"""Project entry point for running the assistant bot CLI."""

from src.assistant_bot import init_bot

def main():
    """Initialize storage, CLI, and enter the assistant bot loop."""
    init_bot()

if __name__ == "__main__":
    main()
