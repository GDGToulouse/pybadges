#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Licensed under the WTFPL license, http://sam.zoy.org/wtfpl/.

import os.path
import sys
import optparse
from qrcodes import download_qr_code

__version__ = '0.1'


def download_qr_codes(input_csv, output_directory):
    import csv
    csvFile = csv.reader(open(input_csv, 'rb'), delimiter=',')

    badges = list(csvFile)
    for index, badge in enumerate(badges):
        download_qr_code(badge, output_directory)


def main():
    usage = '%prog -o output-directory -i input-csv -b background-image'
    parser = optparse.OptionParser(usage=usage,
                                   version='%%prog %s' % __version__)
    parser.add_option('-o', dest='output_directory', metavar='OUTPUT_DIRECTORY',
                      help='specify the location of the output directory.')
    parser.add_option('-i', dest='input_csv', metavar='INPUT_CSV',
                      help='specify the location of the input CSV.')
    

    (options, args) = parser.parse_args()
    if len(args):
        parser.print_help()
        return 1

    if not options.output_directory:
        options.output_directory = "./qrcodes"
    if not os.path.exists(options.output_directory):
        os.makedirs(options.output_directory)

    if not options.input_csv:
        parser.error("Missing input CSV")
    if not os.path.exists(options.input_csv):
        parser.error("Input CSV %s does not exist" % options.input_csv)

    download_qr_codes(options.input_csv, options.output_directory)

if __name__ == '__main__':
    sys.exit(main())
