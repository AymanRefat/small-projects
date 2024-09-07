from argparse import ArgumentParser

from app import commands, utils


def main():
    parser = ArgumentParser()
    sub_parser = parser.add_subparsers(dest="command")
    commands_list = utils.load_subclasses_from_module(commands, commands.BaseCommand)
    for command in commands_list:
        command().install(sub_parser)
    args = parser.parse_args()
    for command in commands_list:
        if command.name == args.command:
            cmd = command()
            print(vars(args))
            cmd.add_data(vars(args))
            cmd.run()


if __name__ == "__main__":
    main()
