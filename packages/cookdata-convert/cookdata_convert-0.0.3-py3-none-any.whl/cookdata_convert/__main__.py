import argparse

from .cookDataToYml import sbyml_to_yml
from .cookDataToSbyml import yml_to_sbyml


def main() -> None:
    parser = argparse.ArgumentParser(description="Tool for converting CookData in LoZ:BotW")

    subparsers = parser.add_subparsers(dest="command", help="Command")
    subparsers.required = True

    y_parser = subparsers.add_parser(
        "yml", description="Search for flags in Bootup.pack", aliases=["y"]
    )
    y_parser.set_defaults(func=lambda a: sbyml_to_yml())

    s_parser = subparsers.add_parser(
        "sbyml", description="Converts CookData.yml to CookData.sbyml", aliases=["s"]
    )
    s_parser.add_argument(
        "-b", "--bigendian", help="Use big endian mode (for Wii U)", action="store_true",
    )
    s_parser.set_defaults(func=lambda a: yml_to_sbyml(a))

    args = parser.parse_args()
    args.func(args)
