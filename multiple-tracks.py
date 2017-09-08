#!/usr/bin/env python

# Licensed under the WTFPL license, http://sam.zoy.org/wtfpl/.

from pybadges import generate_document
import sys

def main():
    
    tracks = ['staff', 'speaker', 'public']

    for track in tracks:
        input_csv = 'badges-%s.csv' % track
        output_pdf = 'badges-%s.pdf' % track
        background = 'badges-%s.png' % track
        generate_document(input_csv, output_pdf, background)

if __name__ == '__main__':
    sys.exit(main())
