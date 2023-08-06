"""CoBib export command."""

import argparse
import os
import sys
from zipfile import ZipFile

from cobib.config import CONFIG
from .base_command import ArgumentParser, Command
from .list import ListCommand


class ExportCommand(Command):
    """Export Command."""

    name = 'export'

    def execute(self, args, out=sys.stdout):
        """Export database.

        Exports all entries matched by the filter queries (see the list docs).
        Currently supported exporting formats are:
        * BibLaTex databases
        * zip archives

        Args: See base class.
        """
        parser = ArgumentParser(prog="export", description="Export subcommand parser.")
        parser.add_argument("-b", "--bibtex", type=argparse.FileType('a'),
                            help="BibLaTeX output file")
        parser.add_argument("-z", "--zip", type=argparse.FileType('a'),
                            help="zip output file")
        parser.add_argument('list_args', nargs='*')

        if not args:
            parser.print_usage(sys.stderr)
            sys.exit(1)

        try:
            largs = parser.parse_intermixed_args(args)
        except argparse.ArgumentError as exc:
            print("{}: {}".format(exc.argument_name, exc.message), file=sys.stderr)
            return

        if largs.bibtex is None and largs.zip is None:
            return
        if largs.zip is not None:
            largs.zip = ZipFile(largs.zip.name, 'w')
        out = open(os.devnull, 'w')
        labels = ListCommand().execute(largs.list_args, out=out)

        try:
            for label in labels:
                entry = CONFIG.config['BIB_DATA'][label]
                if largs.bibtex is not None:
                    entry_str = entry.to_bibtex()
                    largs.bibtex.write(entry_str)
                if largs.zip is not None:
                    if 'file' in entry.data.keys() and entry.data['file'] is not None:
                        largs.zip.write(entry.data['file'], label+'.pdf')
        except KeyError:
            print("Error: No entry with the label '{}' could be found.".format(largs.label))

    @staticmethod
    def tui(tui):
        """See base class."""
        # handle input via prompt
        tui.prompt_handler('export')
