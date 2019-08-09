import argparse
import sys
from enum import Enum


NAME = 'Textex'
VERSION = '1.0.0'


def get_program_info():
    return {
        'prog': f'{NAME} v{VERSION}',
        'usage': f'Usage: {NAME.lower()} <file_path> <section_start> [<section_end>]',
        'description': '''
            Textex extracts text sections from a given text file (PDF not yet supported).\n
            * <section_start>: The line of text from where to start the text extraction\n
            * <section_end>: The line of text that marks the end of the extraction block.\n
            It has to be specified using the following special flags:\n
                * -t: A line of text marking the end of the extraction block\n
                * -l: from <start_section> to the end of the line\n
                * -e: from <start_section> to the end of the file. This is the default option
                    if no <section_end> is specified
        '''
    }

def parse_cmds(cmd_args):
    program_info = get_program_info()
    parser = argparse.ArgumentParser(**program_info)
    parser.add_argument('file_path', help='The path for the text file containing the text to be extracted')
    parser.add_argument('section_start', help='The line of text from where to start the text extraction')
    parser.add_argument('-t', '--text-line', help='The line of text marking the end of the extraction block')
    parser.add_argument('-e', '--end-of-file', 
                        help='Extraction block begins at <start_block> and ends at the end of the file',
                        action='store_true')
    parser.add_argument('-l', '--end-of-line',
                        help='Extraction block begins at <start_block> and ends at the end of the line',
                        action='store_true')
    return parser.parse_args(cmd_args)


def main(args):
    print(args)


if __name__ == '__main__':
    args = parse_cmds(sys.argv[1:])
    # set end-of-file as default section_end if no other strategy was specified
    if not args.end_of_file and not args.end_of_line and not args.text_line:
        args.end_of_file = True
    main(vars(args))
    