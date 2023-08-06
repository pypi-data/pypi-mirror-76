import gzip
import sys

from contextlib import contextmanager
from typing import Optional, IO


@contextmanager
def open_file(filename: Optional[str], mode='r', encoding='utf-8') -> IO:
    fileobj = sys.stdin if filename is None and 'r' in mode else \
        sys.stderr if filename is None and 'e' in mode and 'w' in mode else \
        sys.stdout if filename is None and 'w' in mode else \
        gzip.open(filename, '{}t'.format(mode), encoding=encoding) if isinstance(filename, str) and filename.endswith('.gz') else \
        open(filename, mode.replace('e', ''), encoding=encoding) if isinstance(filename, str) else \
        filename
    yield fileobj
    fileobj.close()
