from app.bot.command_types import RemoveEventCommand, RemoveAllEventsCommand
from app.bot.parsers.argparse_wrapper import BotArgumentParser


def parse_remove_event(
    args: list[str],
) -> RemoveEventCommand | RemoveAllEventsCommand | None:
    parser = BotArgumentParser(prog="remove", add_help=False)
    parser.add_argument("--title", required=False)
    parser.add_argument("--all", action="store_true")

    try:
        parsed_args = parser.parse_args(args)

        if parsed_args.all:
            return RemoveAllEventsCommand()

        if parsed_args.title:
            return RemoveEventCommand(title=parsed_args.title)

        return None
    except ValueError:
        return None
