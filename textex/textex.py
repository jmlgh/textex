import os
import argparse
import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from enum import Enum


NAME = 'Textex'
VERSION = '1.0.0'


class ExtractionChoice(Enum):
    END_OF_LINE = 0
    END_OF_FILE = 1
    TEXT_LINE = 2


class FileTypes(Enum):
    INVALID = -1
    TEXT = 0
    PDF = 1


class Textex:
    def __init__(self, file_path, section_start, extraction_choice, end_line):
        self._file_path = file_path
        self._section_start = section_start
        self._extraction_choice = extraction_choice
        self._end_line = end_line
        self._file_extension = self._get_file_extension()

    def _get_file_extension(self):
        assert os.path.exists(self._file_path)
        extension = self._file_path.split(os.sep)[-1].split('.')[-1]
        if extension == 'txt':
            return FileTypes.TEXT
        elif extension == 'pdf':
            return FileTypes.PDF
        else:
            return FileTypes.INVALID

    def _extract_text_lines(self):
        lines = []
        if self._file_extension == FileTypes.TEXT:
            with open(self._file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        elif self._file_extension == FileTypes.PDF:
            # TODO: extract text from pdf file using Apache Tika
            pass
        else:
            raise Exception(f'Invalid file type: {self._file_extension}')
        return [l.strip() for l in lines]

    def extract_section(self):
        text_lines = self._extract_text_lines()
        block_start = None
        block_end = None
        for line_num, line in enumerate(text_lines):
            if self._section_start.lower() in line.lower():
                block_start = line_num
                break
        if block_start is None:
            raise Exception('Specified start line was not found in the file')         
        
        if self._extraction_choice == ExtractionChoice.END_OF_FILE:
            block_end = text_lines.index(text_lines[-1]) + 1
        elif self._extraction_choice == ExtractionChoice.END_OF_LINE:
            block_end = block_start + 1
        else:
            for line_num, line in enumerate(text_lines):
                if self._end_line.lower() in line.lower():
                    block_end = line_num
                    break
        if block_end is None:
            raise Exception('Specified end line was not found in the file')

        return '\n'.join([text_lines[i] for i in range(block_start, block_end)])
        

def get_program_info():
    return {
        'prog': f'{NAME} v{VERSION}',
        'usage': f'Usage: {NAME.lower()} <file_path> <section_start> [<section_end>]',
        'description': '''Textex extracts text sections from a given text/pdf file.
    * <section_start>: The line of text from where to start the text extraction
    * <section_end>: The section has to be specified using the following special flags:
        * -t: A line of text marking the end of the extraction block
        * -l: from <start_section> to the end of the line
        * -e: from <start_section> to the end of the file. This is the default option
            if no <section_end> is specified
        '''
    }


def parse_cmds(cmd_args):
    program_info = get_program_info()
    parser = ArgumentParser(**program_info, formatter_class=RawTextHelpFormatter)
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


def parse_section_end(args):
    for k, v in args.items():
        if k == 'end_of_file' and v:
            return ExtractionChoice.END_OF_FILE
        elif k == 'end_of_line' and v:
            return ExtractionChoice.END_OF_LINE
        elif k == 'text_line' and v:
            return ExtractionChoice.TEXT_LINE    


def main(args):
    extraction_choice = parse_section_end(args)
    textex = Textex(args['file_path'], args['section_start'], extraction_choice, args['text_line'])
    section = textex.extract_section()
    print(section)


if __name__ == '__main__':
    args = parse_cmds(sys.argv[1:])
    # set end-of-file as default section_end if no other strategy was specified
    if not args.end_of_file and not args.end_of_line and not args.text_line:
        args.end_of_file = True
    main(vars(args))
