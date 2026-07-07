import argparse
import sys

from engine import BootstrapEngine


def build_parser():

    parser = argparse.ArgumentParser(
        prog="labaps",
        description="Lab APS Developer CLI",
    )

    sub = parser.add_subparsers(
        dest="command",
    )

    sub.add_parser("init")

    sub.add_parser("verify")

    sub.add_parser("doctor")

    sub.add_parser("clean")

    return parser


def main():

    parser = build_parser()

    args = parser.parse_args()

    engine = BootstrapEngine()

    match args.command:
        case "init":
            return engine.initialize() or 0

        case "verify":
            return engine.verify() or 0

        case "doctor":
            return engine.doctor() or 0

        case "clean":
            return engine.clean() or 0

        case _:
            parser.print_help()

            return 1


if __name__ == "__main__":
    sys.exit(main())
