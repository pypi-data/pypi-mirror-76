import argparse


class FastaIndexer(object):
    def __init__(self, fname, key=lambda line: line.split()[0]):
        self.fname = fname
        self.fhndl = open(fname)
        self.key = key
        self.line = self.readline()
        self.offset = self.fhndl.tell()
        self.n_bytes, self.n_bases = self.get_width()

    def __del__(self):
        self.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.line == '':
            return()

        length = self.n_bases
        line = self.readline()
        while line != '' and not line.startswith('>'):
            length += len(line.strip())
            line = self.readline()
        hdr = self.key(self.line.strip().split()[0])
        offset = self.offset
        self.offset = self.fhndl.tell()
        self.line = line
        return hdr[1:], length, offset, self.n_bases, self.n_bytes

    def readline(self):
        try:
            return self.fhndl.readline()
        except RuntimeError as e:
            raise RuntimeError('{}\nIf a RuntimeError has occurred, '.format(e) +
                               'the sequences may not be split over several lines. ' +
                               'Try: python -m lhc.io.fasta wrap {}'.format(self.fname))

    def get_width(self):
        line = self.readline()
        n_bytes = len(line)
        n_bases = len(line.strip())
        return n_bytes, n_bases

    def close(self):
        if hasattr(self.fhndl, 'close'):
            self.fhndl.close()


def index(input, extension='.fai'):
    with open('{}{}'.format(input, extension), 'w') as out_fhndl:
        indexer = FastaIndexer(input)
        for hdr, length, offset, n_bases, n_bytes in indexer:
            out_fhndl.write('{}\t{}\t{}\t{}\t{}\n'.format(hdr, length, offset, n_bases, n_bytes))


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser())


def define_parser(parser):
    add_arg = parser.add_argument
    add_arg('input', help='The input fasta file.')
    add_arg('-e', '--extension', default='.fai',
            help='The extension of the index file (default: .fai).')
    parser.set_defaults(func=lambda args: index(args.input, args.extension))
    return parser

if __name__ == '__main__':
    import sys
    sys.exit(main())
