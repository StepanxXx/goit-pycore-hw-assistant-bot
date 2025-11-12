"""Assistant bot orchestration module."""

from src.assistant_bot_cli import AssistantCLI, Command
from src.assistant_bot_handlers import AssistantBotHandlers
from src.assistant_bot_storage import AssistantBotStorage


def init_bot():
    """Run the assistant bot CLI loop."""
    cli = AssistantCLI()
    storage = AssistantBotStorage()
    book = storage.load_data()
    handlers = AssistantBotHandlers(book)

    command_actions = {
        Command.ADD: (handlers.add_contact, True, cli.success_color),
        Command.CHANGE: (handlers.change_contact, True, cli.success_color),
        Command.PHONE: (handlers.show_phone, True, cli.warning_color),
        Command.ALL: (handlers.show_all, False, cli.warning_color),
        Command.ADD_BIRTHDAY: (handlers.add_birthday, True, cli.success_color),
        Command.SHOW_BIRTHDAY: (handlers.show_birthday, True, cli.warning_color),
        Command.BIRTHDAYS: (handlers.show_birthdays, False, cli.warning_color),
    }

    cli.print_message("Welcome to the assistant bot!", cli.info_color)
    
    while True:
        user_input = cli.get_user_input()
        if not user_input.strip():
            continue
        command, args = cli.parse_input(user_input)

        if command is None:
            cli.print_message("Invalid command.", cli.error_color)
            continue

        if command in (Command.CLOSE, Command.EXIT):
            cli.print_message("Good bye!", cli.info_color)
            break

        if command == Command.HELLO:
            cli.print_message("How can I help you?", cli.info_color)
            continue

        action = command_actions.get(command)
        if action is None:
            cli.print_message("Invalid command.", cli.error_color)
            continue

        handler, requires_args, color = action
        result = handler(args) if requires_args else handler()
        cli.print_message(result, color)

    storage.save_data(book)
