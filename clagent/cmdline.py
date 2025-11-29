import argparse


# commandline argument parsing
def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '--vacancy-url',
        type=str, required=True,
        help='URL of the vacancy'
    )
    arg_parser.add_argument(
        '--sys-prompt-file-path',
        type=str,
        required=False,
        default='./system.prompt',
        help='File path which contain the system prompt'
    )
    return arg_parser.parse_args()
