import argparse
from lhc.io.loci import open_loci_file
from pysam import FastaFile
from lhc.binf.sequence.reverse_complement import reverse_complement


def generate_kmers(loci, genome, kmer_length):
    kmers = set()
    for locus in loci:
        if str(locus.chromosome) not in genome.references or locus.stop - locus.start < kmer_length:
            continue
        sequence = genome.fetch(str(locus.chromosome), locus.start.position, locus.stop.position)
        if locus.strand != '+':
            sequence = reverse_complement(sequence)
        for i in range(len(sequence) - kmer_length):
            kmers.add(sequence[i:i + kmer_length])
    return kmers


def kmer_filter(loci, genome, kmers, kmer_length):
    for locus in loci:
        if str(locus.chromosome) not in genome.references or locus.stop - locus.start < kmer_length:
            continue
        sequence = genome.fetch(str(locus.chromosome), locus.start.position, locus.stop.position)
        if locus.strand != '+':
            sequence = reverse_complement(sequence)
        if any(sequence[i:i + kmer_length] in kmers for i in range(len(sequence) - kmer_length)):
            yield locus


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser())


def define_parser(parser):
    parser.add_argument('input', nargs='?',
                        help='loci to generate kmers from(default: stdin).')
    parser.add_argument('output', nargs='?',
                        help='filtered_loci (default: stdout).')
    parser.add_argument('-i', '--input-format',
                        help='file format of input file (useful for reading from stdin).')
    parser.add_argument('-o', '--output-format',
                        help='file format of output file (useful for writing to stdout).')
    parser.add_argument('-l', '--loci',
                        help='loci to filter.')
    parser.add_argument('-s', '--sequence', required=True)
    parser.add_argument('-k', '--kmer_length', default=11, type=int)
    parser.set_defaults(func=init_kmer_filter)


def init_kmer_filter(args):
    genome = FastaFile(args.sequence)
    with open_loci_file(args.input, format=args.input_format) as loci:
        kmers = generate_kmers(loci, genome, args.kmer_length)

    with open_loci_file(args.loci, format=args.input_format) as loci,\
            open_loci_file(args.output, 'w', format=args.output_format) as outfile:
        for locus in kmer_filter(loci, genome, kmers, args.kmer_length):
            outfile.write(locus)


if __name__ == '__main__':
    main()
