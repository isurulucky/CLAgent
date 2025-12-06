import argparse

VACANCY_URL = '--vacancy-url'
CV = '--cv'
SAMPLE_COVER_LETTER_DIR = '--sample-cover-letter-dir'
SYS_PROMPT_FILE_PATH = '--sys-prompt-file-path'


# commandline argument parsing
def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        f'{VACANCY_URL}',
        type=str,
        required=True,
        help='URL of the vacancy'
    )
    arg_parser.add_argument(
        f'{CV}',
        type=str,
        required=True,
        help='Path to the CV (*.txt|pdf)'
    )
    arg_parser.add_argument(
        f'{SAMPLE_COVER_LETTER_DIR}',
        type=str,
        required=False,
        default="",
        help='Path to a directory containing sample cover letters'
    )
    arg_parser.add_argument(
        f'{SYS_PROMPT_FILE_PATH}',
        type=str,
        required=False,
        default='./system.prompt',
        help='File path which contain the system prompt'
    )
    return arg_parser.parse_args()
