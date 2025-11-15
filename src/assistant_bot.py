"""Assistant bot orchestration module."""

from src.assistant_bot_cli import AssistantCLI, Command
from src.assistant_bot_handlers import AssistantBotHandlers
from src.assistant_bot_storage import AssistantBotStorage
from src.notes import Notes
from src.address_book import AddressBook

def init_bot():
    """Run the assistant bot CLI loop."""
    cli = AssistantCLI()
    storage = AssistantBotStorage()
    book,notes = storage.load_data() or (AddressBook(), Notes())
    handlers = AssistantBotHandlers(book, notes)

    command_actions = {
        Command.ADD: (handlers.add_contact, True, cli.success_color),
        Command.DELETE: (handlers.delete_contact, True, cli.info_color),
        Command.SEARCH: (handlers.search_contact, True, cli.info_color),
        Command.ADD_EMAIL: (handlers.add_email, True, cli.success_color),
        Command.EMAILS: (handlers.show_emails, True, cli.warning_color),
        Command.CHANGE_EMAIL: (handlers.change_email, True, cli.success_color),
        Command.SET_ADDRESS: (handlers.set_address, True, cli.success_color),
        Command.CHANGE_PHONE: (handlers.change_phone, True, cli.success_color),
        Command.PHONES: (handlers.show_phones, True, cli.warning_color),
        Command.ALL: (handlers.show_all, False, cli.warning_color),
        Command.ADD_BIRTHDAY: (handlers.add_birthday, True, cli.success_color),
        Command.SHOW_BIRTHDAY: (handlers.show_birthday, True, cli.warning_color),
        Command.BIRTHDAYS: (handlers.show_birthdays, True, cli.warning_color),
        Command.ADD_NOTE: (handlers.add_note, True, cli.success_color),
        Command.FIND_NOTE: (handlers.find_note, True, cli.warning_color),
        Command.SHOW_NOTES: (handlers.show_notes, False, cli.warning_color),
        Command.EDIT_NOTE: (handlers.edit_note, True, cli.success_color),
        Command.DELETE_NOTE: (handlers.delete_note, True, cli.success_color),
        Command.ADD_NOTE_TAG: (handlers.add_note_tag, True, cli.success_color),
        Command.DELETE_NOTE_TAG: (handlers.delete_note_tag, True, cli.success_color),
        Command.FIND_NOTE_BY_TAG: (handlers.find_note_by_tag, True, cli.warning_color),
        Command.SHOW_NOTES_ORDERED_BY_TAG_ASC: \
            (handlers.show_notes_tag_sorted, False, cli.warning_color),
        Command.SHOW_NOTES_ORDERED_BY_TAG_DESC: \
            (handlers.show_notes_tag_desc_sorted, False, cli.warning_color),
    }
    mutating_commands = {
        Command.ADD,
        Command.DELETE,
        Command.ADD_EMAIL,
        Command.CHANGE_EMAIL,
        Command.SET_ADDRESS,
        Command.CHANGE_PHONE,
        Command.ADD_BIRTHDAY,
        Command.ADD_NOTE,
        Command.EDIT_NOTE,
        Command.DELETE_NOTE,
        Command.ADD_NOTE_TAG,
        Command.DELETE_NOTE_TAG,
    }

    cli.print_message("Welcome to the assistant bot!", cli.info_color)
    cli.print_main_menu()

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

        if command in mutating_commands:
            storage.save_data((book, notes))

    storage.save_data((book, notes))
