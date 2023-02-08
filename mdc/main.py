from argparse import ArgumentParser
import sys
from typing import NamedTuple, List, Tuple, Dict, Any
import functions

Argument = Tuple[List[str], Dict[str, Any]]


class Command(NamedTuple):
    name: str
    description: str
    arguments: List[Argument]


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
                    "help": "Convert video from this time.",
                    "type": int,
                    "default": None,
                },
            ),
            (
                ["-e"],
                {
                    "help": "Convert video up to this time.",
                    "type": int,
                    "default": None,
                }
            ),
        ],
    ),
    Command(
        name = "image",
        description="Convert image to a palette of colors",
        arguments=[
            (
                ["image_name"],
                {
                    "help": "The path of the image you want to convert.",
                    "type": str,
                }
            ),
            (
                ["-c"],
                {
                    "help": "Number of colors in the palette.",
                    "type": int,
                    "default": None,
                }
            )
        ],
    ),

]

def get_parser():
    parser = ArgumentParser(prog="mdc")
    subparsers = parser.add_subparsers(title="commands")

    for command in commands:
        sub = subparsers.add_parser(name=command.name, description=command.description)
        sub.set_defaults(func=functions.__dict__.get(command.name))
        for args, kwargs in command.arguments:
            sub.add_argument(*args, **kwargs)
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    if "func" not in args:
        parser.print_help()
    try:
        args.func(args)
    except:
        sys.exit()

        
main()