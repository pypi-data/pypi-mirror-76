from argparse import ArgumentParser
from itertools import product

from lhc.binf.sequence.reverse_complement import reverse_complement as rc
from lhc.io.fasta import iter_fasta
from lhc.io.fasta.tools import wrap, index
from lhc.io.txt.tools import compress


def cross_product(xs, ys):
    for x, y in product(iter_fasta(xs), iter_fasta(ys)):
        sys.stdout.write('>{}_{}\n{}{}\n'.format(x.hdr, y.hdr, x.seq, y.seq))


def revcmp(input, output, both=False):
    if both:
        for hdr, seq in input:
            output.write('>{}\n{}\n'.format(hdr, seq))
            output.write('>{}_revcmp\n{}\n'.format(hdr, rc(seq)))
    else:
        for hdr, seq in input:
            output.write('>{}_revcmp\n{}\n'.format(hdr, rc(seq)))


def compare(a_fname, b_fname):
    a_hdrs = _get_headers(a_fname)
    b_hdrs = _get_headers(b_fname)

    a_only = sorted(a_hdrs - b_hdrs)
    print('{} headers unique to first fasta:'.format(len(a_only)))
    print('\n'.join(a_only))
    b_only = sorted(b_hdrs - a_hdrs)
    print('{} headers unique to second fasta:'.format(len(b_only)))
    print('\n'.join(b_only))
    both = sorted(a_hdrs & b_hdrs)
    print('{} headers common to both fastas:'.format(len(both)))
    print('\n'.join(both))

    print('The common headers differ at the following positions:')
    a_parser = iter_fasta(a_fname)
    b_parser = iter_fasta(b_fname)
    for hdr in both:
        for i, (a, b) in enumerate(zip(a_parser[hdr], b_parser[hdr])):
            if a.lower() != b.lower():
                print('{} starts to differ at position {}: {} {}'.format(hdr, i, a, b))
                break


def _get_headers(fname):
    with open(fname, encoding='utf-8') as fileobj:
        hdrs = [line for line in fileobj if line.startswith('>')]
    return hdrs


def extract(fname, header, out_fname=None):
    with sys.stdout if out_fname is None else open(out_fname, 'w') as output, \
            open(fname, encoding='utf-8') as input:
        extracting = False
        for line in input:
            if line[0] == '>':
                if extracting:
                    break
                elif line[1:].startswith(header):
                    extracting = True
            if extracting:
                output.write(line)

# CLI


def main():
    parser = get_parser()
    args = parser.parse_args()
    args.func(args)


def get_parser():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    compare_parser = subparsers.add_parser('compare')
    compare_parser.add_argument('input_a')
    compare_parser.add_argument('input_b')
    compare_parser.set_defaults(func=lambda args: compare(args.input_a, args.input_b))

    compress_parser = subparsers.add_parser('compress')
    compress.define_parser(compress_parser)

    extract_parser = subparsers.add_parser('extract')
    extract_parser.add_argument('input')
    extract_parser.add_argument('header')
    extract_parser.add_argument('-o', '--output')
    extract_parser.set_defaults(func=lambda args: extract(args.input, args.header, args.output))

    index_parser = subparsers.add_parser('index')
    index.define_parser(index_parser)

    product_parser = subparsers.add_parser('product')
    product_parser.add_argument('input1', help='Input fasta (default: stdin).')
    product_parser.add_argument('input2', help='Output fasta (default: stdout).')
    product_parser.set_defaults(func=lambda args: cross_product(args.input1, args.input2))

    revcmp_parser = subparsers.add_parser('revcmp')
    revcmp_parser.add_argument('-b', '--both', action='store_true', help='Keep both')
    revcmp_parser.add_argument('input', nargs='?',
                               help='input file (default: stdin)')
    revcmp_parser.add_argument('output', nargs='?',
                               help='output file (default: stdout)')
    revcmp_parser.set_defaults(func=init_revcmp)

    sort_parser = subparsers.add_parser('sort')
    #sort.define_parser(sort_parser)

    wrap_parser = subparsers.add_parser('wrap')
    wrap.define_parser(wrap_parser)

    return parser


def init_revcmp(args):
    import sys
    input = sys.stdin if args.input is None else args.input
    output = sys.stdin if args.output is None else args.output
    revcmp(input, output)
    input.close()
    output.close()


if __name__ == '__main__':
    import sys
    sys.exit(main())
