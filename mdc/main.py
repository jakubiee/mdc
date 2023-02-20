from argparse import ArgumentParser, ArgumentTypeError
import sys
from typing import NamedTuple, List, Tuple, Dict, Any
import mdc.functions

Argument = Tuple[List[str], Dict[str, Any]]


class Command(NamedTuple):
    name: str
    description: str
    arguments: List[Argument]


def time(time: str):
    parts = []
    for p in time.split(":"):
        parts.append(int(p))
    hours, minutes = parts[0], parts[1]
    seconds = parts[2] if len(parts) > 2 else 0

    if hours < 0 or not (0 <= minutes <= 59) or not (0 <= seconds <= 59):
        raise ArgumentTypeError

    return hours * 3600 + minutes * 60 + seconds


commands = [
    Command(
        name="video",
        description="Convert video to a palette",
        arguments=[
            (
                ["video_name"],
                {
                    "help": "The path of the video you want to convert.",
                    "type": str,
                    "nargs": "+",
                },
            ),
            (
                ["-s"],
                {
                    "help": "Convert video from this time. (hh:mm:ss)",
                    "type": time,
                    "default": None,
                },
            ),
            (
                ["-e"],
                {
                    "help": "Convert video up to this time. (hh:mm:ss)",
                    "type": time,
                    "default": None,
                },
            ),
            (
                ["-t"],
                {
                    "help": "Set a palette title.",
                    "type": str,
                    "default": None,
                },
            ),
        ],
    ),
    Command(
        name="image",
        description="Convert image to a palette of colors",
        arguments=[
            (
                ["image_name"],
                {
                    "help": "The path of the image you want to convert.",
                    "type": str,
                    "nargs": "+",
                },
            ),
            (
                ["-c"],
                {
                    "help": "Number of colors in the palette.",
                    "type": int,
                    "default": 5,
                },
            ),
            (
                ["-t"],
                {
                    "help": "Set a chart title.",
                    "type": str,
                    "default": None,
                },
            ),
            (
                ["-hex"],
                {
                    "help": "Shows the hex color code of each color on the palette.",
                    "type": bool,
                    "nargs": "?",
                    "const": True,
                    "default": False,
                },
            ),
        ],
    ),
]


def get_parser():
    parser = ArgumentParser(prog="mdc")
    subparsers = parser.add_subparsers(title="commands")

    for command in commands:
        sub = subparsers.add_parser(name=command.name, description=command.description)
        sub.set_defaults(func=mdc.functions.__dict__.get(command.name))
        for args, kwargs in command.arguments:
            sub.add_argument(*args, **kwargs)
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    if "func" not in args:
        parser.print_help()
    args.func(args)
