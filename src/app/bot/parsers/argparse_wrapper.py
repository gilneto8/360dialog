import argparse


class BotArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        """Prevent exit on error, raise exception instead."""
        raise ValueError(message)
