from datetime import datetime
from app.bot.command_types import FreeTimeCommand
from app.bot.parsers.argparse_wrapper import BotArgumentParser
from app.bot.parsers.utils import parse_smart_date


def parse_free_time(args: list[str]) -> FreeTimeCommand | None:
    parser = BotArgumentParser(prog="free", add_help=False)
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
            base_dt = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

            start_str = join_args(parsed_args.start_date)
            start_time = parse_smart_date(start_str, base_date=base_dt)

            end_time = None
            if parsed_args.end_date:
                end_str = join_args(parsed_args.end_date)
                end_time = parse_smart_date(end_str, base_date=base_dt)
                if end_time.hour == 0 and end_time.minute == 0:
                    end_time = end_time.replace(hour=23, minute=59, second=59)
            else:
                end_time = start_time.replace(hour=23, minute=59, second=59)

            return FreeTimeCommand(start_time=start_time, end_time=end_time)
        except ValueError:
            return None
    except ValueError:
        return None
