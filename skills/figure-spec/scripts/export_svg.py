#!/usr/bin/env python3
"""Export a local FigureSpec SVG to PDF or PNG using the available PyMuPDF."""
import argparse
from pathlib import Path
import fitz


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--dpi', type=int, default=200)
    args = parser.parse_args()
    if args.source.resolve() == args.output.resolve():
        parser.error('Source and output must be different files.')
    if args.output.suffix.lower() not in {'.pdf', '.png'}:
        parser.error('Output must be .pdf or .png.')
    if not 36 <= args.dpi <= 1200:
        parser.error('DPI must be between 36 and 1200.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with fitz.open(str(args.source)) as source:
        if args.output.suffix.lower() == '.pdf':
            args.output.write_bytes(source.convert_to_pdf())
        else:
            source[0].get_pixmap(dpi=args.dpi, alpha=False).save(str(args.output))
    print(args.output)


if __name__ == '__main__':
    main()
