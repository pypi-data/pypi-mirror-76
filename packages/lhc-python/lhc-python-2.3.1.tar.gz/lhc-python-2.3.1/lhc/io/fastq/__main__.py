import argparse
import sys

from lhc.io.fastq.iterator import FastqEntryIterator
from lhc.io.fastq.tools import split
from lhc.io.txt.tools import compress


def iter_fastq(fname):
    for entry in FastqEntryIterator(fname):
        yield entry


def rmdup(input, output):
    def meanQuality(v):
        return mean(quality(v[2]))

    from collections import defaultdict
    from numpy import mean

    visited = defaultdict(list)
    for hdr, seq, plus, qua in input:
        visited[seq].append((hdr, seq, qua))
    print(list(visited.values())[0])
    for hdr, seq, qua in sorted(iter(visited.values()), key=meanQuality):
        output.write(hdr)
        output.write('\n')
        output.write(seq)
        output.write('\n+\n')
        output.write(qua)
        output.write('\n')


def quality(qua, offset=33):
    return [ord(char) - offset for char in qua]


def interleave(fastq1, fastq2, outfile=sys.stdout):
    with open(fastq1, encoding='utf-8') as infile1,\
            open(fastq2, encoding='utf-8') as infile2:
        try:
            while True:
                for i in range(4):
                    outfile.write(next(infile1))
                for i in range(4):
                    outfile.write(next(infile2))
        except StopIteration:
            pass


def to_fasta(input, output):
    for entry in input:
        output.write('>{}\n{}\n'.format(entry.hdr, entry.seq))


# CLI


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser())


def define_parser(parser):
    subparsers = parser.add_subparsers()

    compress_parser = subparsers.add_parser('compress')
    compress.define_parser(compress_parser)
    compress_parser.set_defaults(block_delimiter='\n>')
    
    parser_rmdup = subparsers.add_parser('rmdup')
    parser_rmdup.add_argument('input', nargs='?',
                              help='input file (default: stdin)')
    parser_rmdup.add_argument('output', nargs='?',
                              help='output file (default: stdout)')
    parser_rmdup.set_defaults(func=init_rmdup)
    
    parser_interleave = subparsers.add_parser('interleave')
    parser_interleave.add_argument('fastq1')
    parser_interleave.add_argument('fastq2')
    parser_interleave.set_defaults(func=lambda args: interleave(args.fastq1, args.fastq2))

    parser_split = subparsers.add_parser('split')
    split.define_parser(parser_split)
    
    parser_to_fasta = subparsers.add_parser('to_fasta')
    parser_to_fasta.add_argument('input', nargs='?',
                                 help='input fastq file (default: stdin).')
    parser_to_fasta.add_argument('output', nargs='?',
                                 help='output fasta file (default: stdout).')
    parser_to_fasta.set_defaults(func=init_to_fasta)
    return parser


def init_rmdup(args):
    import sys
    input = sys.stdin if args.input is None else args.input
    output = sys.stdout if args.output is None else args.output
    rmdup(input, output)
    input.close()
    output.close()


def init_to_fasta(args):
    import sys
    input = sys.stdin if args.input is None else args.input
    output = sys.stdout if args.output is None else args.output
    to_fasta(input, output)
    input.close()
    output.close()


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

