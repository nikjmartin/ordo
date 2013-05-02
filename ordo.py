import re
from copy import deepcopy


def generate_sequences(iterable):
    '''Return a list of sequences generated from the *iterable* list of input items.
    A list of items that did not get sequenced will also be returned, so the caller
    gets back (sequences, non_sequences).

    Each sequence item will be a dictionary containing the following keys:
        * stem - the bit before the index
        * tail - the bit after the index
        * indexes - an array of index values
        * padding - the number of padding digits, or 0 for no padding

    '''
    regex = re.compile('(?P<stem>.*?)(?P<index>(?P<padding>0*)(\d+))(?P<tail>.*)$')
    sequences = {}
    non_sequences = []

    for item in iterable:
        match = regex.match(item)

        # Can't be part of a sequence
        if not match:
            non_sequences.append(item)
            continue

        # We have an indexed item - retrieve the values
        index = match.group('index')
        padding = 0
        if len(match.group('padding')):
            padding = len(index)

        stem = match.group('stem')
        tail = match.group('tail')

        if (stem, tail, padding) in sequences:
            sequences[(stem, tail, padding)]['indexes'].append(int(index))
        else:
            sequences[(stem, tail, padding)] = { 'stem': stem,
                                                 'tail': tail,
                                                 'indexes': [(int(index))],
                                                 'padding': padding }

    # We've found all the sequences, but some may be fragmented, so we need to
    # merge them together
    merged_sequences = []
    sequence_keys = sequences.keys()
    sequence_keys.sort()

    for key in sequence_keys:
        sequence = sequences[key]

        if len(merged_sequences):
            # If it doesn't get merged into the last sequence added then append
            new_sequence = merge(merged_sequences[-1], sequence)
            if new_sequence:
                merged_sequences[-1] = new_sequence
            else:
                merged_sequences.append(sequence)

        # We haven't got anything in the list yet
        else:
            merged_sequences.append(sequence)

    for sequence in merged_sequences:
        if sequence['padding'] == 0 and len(sequence['indexes']):
            if len(str(sequence['indexes'][0])) == len(str(sequence['indexes'][-1])):
                sequence['padding'] = len(str(sequence['indexes'][0]))

    return merged_sequences, non_sequences


def merge(first_sequence, second_sequence):
    '''Attempt to merge together the two input sequences. Returns a new merged
    sequence, or None if a merge is not possible.

    '''
    if first_sequence['stem'] == second_sequence['stem'] and\
            first_sequence['tail'] == second_sequence['tail']:

        if first_sequence['padding'] == second_sequence['padding']:
            # Merge the sequences and return a new sequence
            indexes = _merge_indexes([first_sequence['indexes'], second_sequence['indexes']])
            new_sequence = { 'stem': first_sequence['stem'],
                             'tail': first_sequence['tail'],
                             'indexes': indexes,
                             'padding': first_sequence['padding'] }
            return new_sequence

        else:
            # Merge if the padding is compatable but not equal
            # They will be compatable if the first index and last index of the
            # two sequences have the same number of digits in either:
            #   [first_sequence]---[second_sequence] or
            #   [second sequence]---[first_sequence]

            # First deal with empty sequences
            if len(first_sequence['indexes']) == 0:
                return deepcopy(second_sequence)
            elif len(second_sequence['indexes']) == 0:
                return deepcopy(first_sequence)

            # Test to see if the sequence padding do actually match
            if len(str(first_sequence['indexes'][-1])) == second_sequence['padding'] or\
                    len(str(second_sequence['indexes'][-1])) == first_sequence['padding']:

                if first_sequence['padding'] > second_sequence['padding']:
                    padding = first_sequence['padding']
                else:
                    padding = second_sequence['padding']

                indexes = _merge_indexes([first_sequence['indexes'], second_sequence['indexes']])
                new_sequence = { 'stem': first_sequence['stem'],
                                 'tail': first_sequence['tail'],
                                 'indexes': indexes,
                                 'padding': padding }
                return new_sequence
    return None


def _merge_indexes(indexes_list):
    '''Merge the indexes in *indexes_list*.'''
    indexes = set()
    for item in indexes_list:
        indexes.update(item)
    return sorted(indexes)