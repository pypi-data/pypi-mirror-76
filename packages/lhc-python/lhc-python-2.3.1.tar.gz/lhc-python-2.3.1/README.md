[![Build Status](https://travis-ci.org/childsish/lhc-python.svg?branch=master)](https://travis-ci.org/childsish/lhc-python)

lhc-python
==========

This is my personal library of python classes and functions, many of them have bioinformatics applications. The library changes constantly and at a whim. If you want to use it, approach with caution. Over time however, parts appear to be settling on a stable configuration.

lhc.binf
--------

**lhc.binf.alignment**

A pure Python implementation of the Smith-Waterman local alignment algorithm.

**lhc.binf.digen**

A C++ and pure Python implementation of sequence generation algorithm. The generated sequence will have a specified dinucleotide frequency.

**lhc.binf.genomic_coordinate**

An implementation of intervals and points for genomic coordinates. Useful for representing gene models.

**lhc.binf.genetic_code**

A class to read genetic codes and translate DNA sequences into protein sequences

**lhc.binf.iupac**

A class to convert protein names between the one and three letter codes and the full name.

**lhc.binf.kmer**

A class that calculates k-mers for a given sequence. The class behaves likea dict, but calculates new k-mers on the fly.

**lhc.binf.skew**

A class that calculates skews for a given sequence. The class behaves like a dict, but calculates new skews on the fly.

lhc.collections
---------------

Several collections mostly for holding intervals. If only intervals need to be held, use the IntervalTree, otherwise the MultiDimensionMap may be more appropriate.

lhc.filetools
-------------

Classes for working with files

lhc.graph
---------

A pure Python implementation of graphs

lhc.indices
-----------

Intended to be my own code for indexing files but is still very unstable an immature

lhc.interval
------------

A class for intervals and interval operations

lhc.io
------

Classes for parsing and working with several file formats

lhc.itertools
-------------

Classes for working with iterators

lhc.tools
---------

Various classes, mostly unused and out-of-date

lhc.random
----------

**lhc.random.reservoir**

An implementation of the reservoir sampling algorithm. Can also be run from the command line to sample lines from files. To sample 50 lines from a file called input_file.txt, run:

```bash
python -m lhc.random.reservoir input_file.txt 50
```

lhc.stats
---------

Really old code. Probably the NIPALS and PCA algorithms are of most use.

lhc.test
--------

Unit tests! These should be mostly up-to-date now.

lhc.tools
---------

**lhc.tools.sorter**

A sorter for very large iterators. The iterator will be split into chunks which are then sorted individually and then merged into a single file.

**lhc.tools.tokeniser**

A basic tokeniser. Users define which characters belong to which classes and the tokeniser will split strings into substrings where all characters have the same type.

```python
>>> tokeniser = Tokeniser({'word': 'abcdefghijklmnopqrstuvwxyz',
                       'number': '0123456789',
                       'space': ' \t'})
>>> tokens = tokeniser.tokenise('there were 1000 bottles on the wall')
>>> tokeniser.next()
Token(type='word', value='there')
>>> tokeniser.next()
Token(type='space', value=' ')
>>> tokeniser.next()
Token(type='word', value='were')
>>> tokeniser.next()
Token(type='space', value=' ')
>>> tokeniser.next()
Token(type='number', value='1000')
```
