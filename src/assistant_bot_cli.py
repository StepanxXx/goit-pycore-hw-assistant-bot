"""CLI helpers, command definitions, and styling for the assistant bot."""

from enum import Enum
from typing import List, Optional, Tuple

from colorama import Fore, Style as ColoramaStyle, init as colorama_init
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style

colorama_init(autoreset=True)


class Command(str, Enum):
    """Supported commands for the assistant bot."""

    ADD = "add"
    CHANGE = "change"
    PHONE = "phone"
    ALL = "all"
    ADD_BIRTHDAY = "add-birthday"
    SHOW_BIRTHDAY = "show-birthday"
    BIRTHDAYS = "birthdays"
    HELLO = "hello"
    EXIT = "exit"
    CLOSE = "close"


class FirstWordCompleter(Completer):
    """Completer that suggests commands only for the first word."""

    def __init__(self, commands: List[str]) -> None:
        self.commands = commands

    def get_completions(self, document, complete_event):
        text_before_cursor = document.text_before_cursor
        stripped_before_cursor = text_before_cursor.lstrip()

        # Disable completion after the user starts typing arguments.
        if " " in stripped_before_cursor:
            return

        word_before_cursor = document.get_word_before_cursor()
        word_lower = word_before_cursor.lower()

        for command in self.commands:
            if command.startswith(word_lower):
                yield Completion(command, start_position=-len(word_before_cursor))


class AssistantCLI:
    """Encapsulates user interaction utilities for the assistant bot."""

    def __init__(self) -> None:
        self.prompt_style = Style.from_dict({"prompt": "#00aa00 bold"})
        self.prompt_message = [("class:prompt", "Enter a command: ")]
        self.command_completer = FirstWordCompleter([command.value for command in Command])

        self.default_color = Fore.WHITE
        self.info_color = Fore.CYAN
        self.success_color = Fore.LIGHTGREEN_EX
        self.warning_color = Fore.YELLOW
        self.error_color = Fore.RED

    def print_message(self, message: str, color: Optional[str] = None) -> None:
        """Print a message to stdout with color highlighting."""
        applied_color = color or self.default_color
        print(f"{applied_color}{message}{ColoramaStyle.RESET_ALL}")

    def get_user_input(self) -> str:
        """Return user input read using prompt_toolkit for better UX."""
        return prompt(
            self.prompt_message,
            completer=self.command_completer,
            style=self.prompt_style,
        )

    def parse_input(self, user_input: str) -> Tuple[Optional["Command"], List[str]]:
        """Parse raw user input into a command enum and arguments."""
        parts = user_input.split()
        if not parts:
            return None, []
        cmd, *args = parts
        cmd = cmd.strip().lower()
        try:
            return Command(cmd), args
        except ValueError:
            return None, args
