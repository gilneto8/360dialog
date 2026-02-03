from datetime import datetime
from app.bot.command_types import ListEventsCommand
from app.bot.parsers.argparse_wrapper import BotArgumentParser
from app.bot.parsers.utils import parse_smart_date


def parse_list_events(args: list[str]) -> ListEventsCommand | None:
    parser = BotArgumentParser(prog="list", add_help=False)
    parser.add_argument(
        "--start-date", "--date", "--start", "--from", dest="start_date", nargs="+"
    )
    parser.add_argument("--end-date", "--end", "--to", dest="end_date", nargs="+")

    try:
        parsed_args = parser.parse_args(args)
        start_date = None
        end_date = None

        def join_args(a):
            if isinstance(a, list):
                return " ".join(a)
            return a

        if parsed_args.start_date:
            try:
                base_dt = datetime.now().replace(
                    hour=0, minute=0, second=0, microsecond=0
                )

                start_str = join_args(parsed_args.start_date)
                start_date = parse_smart_date(start_str, base_date=base_dt)
            except ValueError:
                pass

        if parsed_args.end_date:
            try:
                base_dt = datetime.now().replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
                end_str = join_args(parsed_args.end_date)
                end_date = parse_smart_date(end_str, base_date=base_dt)
            except ValueError:
                pass
        elif start_date:
            end_date = start_date.replace(
                hour=23, minute=59, second=59, microsecond=999999
            )

        return ListEventsCommand(start_date=start_date, end_date=end_date)
    except ValueError:
        return None
