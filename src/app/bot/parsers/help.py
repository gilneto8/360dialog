from app.bot.command_types import HelpCommand


def parse_help(args: list[str]) -> HelpCommand | None:
    return HelpCommand()
