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

    new = sub.add_parser("new", help="Generate code (module, entity, usecase)")
    new_sub = new.add_subparsers(dest="kind")

    module_parser = new_sub.add_parser("module", help="Generate a business module")
    module_parser.add_argument("name")

    entity_parser = new_sub.add_parser("entity", help="Generate a domain entity")
    entity_parser.add_argument("module")
    entity_parser.add_argument("name")

    usecase_parser = new_sub.add_parser("usecase", help="Generate a use case")
    usecase_parser.add_argument("module")
    usecase_parser.add_argument("name")

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

        case "new":
            return run_new(parser, args)

        case _:
            parser.print_help()

            return 1


def run_new(parser, args):
    from generator import Generator

    generator = Generator()

    match args.kind:
        case "module":
            return generator.new_module(args.name) or 0

        case "entity":
            return generator.new_entity(args.module, args.name) or 0

        case "usecase":
            return generator.new_usecase(args.module, args.name) or 0

        case _:
            parser.parse_args(["new", "--help"])
            return 1


if __name__ == "__main__":
    sys.exit(main())
