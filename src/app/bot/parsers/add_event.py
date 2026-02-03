from app.bot.command_types import AddEventCommand
from app.bot.parsers.argparse_wrapper import BotArgumentParser
from app.bot.parsers.utils import parse_smart_date


def parse_add_event(args: list[str]) -> AddEventCommand | None:
    parser = BotArgumentParser(prog="add", add_help=False)
    parser.add_argument("--title", required=True)
    parser.add_argument(
        "--start-date", "--start", "--from", dest="start_date", required=True, nargs="+"
    )
    parser.add_argument("--end-date", "--end", "--to", dest="end_date", nargs="+")

    try:
        parsed_args = parser.parse_args(args)

        def join_args(a):
            if isinstance(a, list):
                return " ".join(a)
            return a

        try:
            start_str = join_args(parsed_args.start_date)
            start_time = parse_smart_date(start_str)

            end_time = None
            if parsed_args.end_date:
                end_str = join_args(parsed_args.end_date)
                end_time = parse_smart_date(end_str)

            return AddEventCommand(
                title=parsed_args.title, start_time=start_time, end_time=end_time
            )
        except ValueError:
            return None
    except ValueError:
        return None
