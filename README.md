ordo
====

Ordo is a sequence analysis toolkit, providing a simple mechanism for converting
an iterable of strings into a tuple of sequence data and remaining non-sequence
items.

The sequence data is a list of dictionaries, containing the following keys:
    * stem: the bit before the number
    * tail: the bit after the number
    * padding: the total number of numerical digits including leading zeros
    * indexes: a list of integers found

For example:

    >>> import ordo
    >>> input = ['foo.001.ext', 'foo.002.ext', 'foo.003.ext', 'foo.004.ext', 'bar']
    >>> ordo.generate_sequences(input)
    ([{'padding': 3, 'tail': '.ext', 'indexes': [1, 2, 3, 4], 'stem': 'foo.'}], ['bar'])