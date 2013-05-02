import unittest

import ordo


class TestOrdo(unittest.TestCase):

    def test_generate_sequences(self):
        # Test for alphanumeric and empty tail values, with non sequence item
        iterable = [
            'seq.0001.ext', 'seq.0002.ext', 'seq.0003.ext', 'seq.0004.ext',
            'seq.0001_1', 'seq.0002_1', 'seq.0003_1', 'seq.0004_1',
            'seq.0001', 'seq.0002', 'seq.0003', 'seq.0004', 'single_item'
        ]
        expected = [{
            'padding': 4,
            'tail': '.ext',
            'indexes': [1, 2, 3, 4],
            'stem': 'seq.'
        },
        {
            'padding': 4,
            'tail': '_1',
            'indexes': [1, 2, 3, 4],
            'stem': 'seq.'
        },
        {
            'padding': 4,
            'tail': '',
            'indexes': [1, 2, 3, 4],
            'stem': 'seq.'
        }]
        
        sequences, non_sequences = ordo.generate_sequences(iterable)
        self.assertItemsEqual(sequences, expected)
        self.assertListEqual(non_sequences, ['single_item'])
        
        # Test for distiction between different padding values
        iterable = [
            'seq.0001.ext', 'seq.0002.ext', 'seq.0003.ext', 'seq.0004.ext',
            'seq.005.ext', 'seq.006.ext', 'seq.007.ext', 'seq.008.ext',
        ]
        expected = [{
            'padding': 4,
            'tail': '.ext',
            'indexes': [1, 2, 3, 4],
            'stem': 'seq.'
        },
        {
            'padding': 3,
            'tail': '.ext',
            'indexes': [5, 6, 7, 8],
            'stem': 'seq.'
        }]
        
        sequences, non_sequences = ordo.generate_sequences(iterable)
        self.assertItemsEqual(sequences, expected)
        self.assertListEqual(non_sequences, [])
        
        # Test for broken sequences being treated as one
        iterable = [
            'seq.0001.ext', 'seq.0002.ext', 'seq.0003.ext', 'seq.0004.ext',
            'seq.0006.ext', 'seq.0007.ext'
        ]
        expected = [{
            'padding': 4,
            'tail': '.ext',
            'indexes': [1, 2, 3, 4, 6, 7],
            'stem': 'seq.'
        }]
        
        sequences, non_sequences = ordo.generate_sequences(iterable)
        self.assertItemsEqual(sequences, expected)
        self.assertListEqual(non_sequences, [])


if __name__ == '__main__':
    unittest.main()