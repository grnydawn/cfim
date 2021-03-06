from context import cfim
import unittest
from cfim import restore, span

class TestParser(unittest.TestCase):

    def _test_prep(self):
        #original_input = { 'data': { 0: 'Red', 1: 'Yellow', 2:'Blue' }, 'output': [(0,3)] }
        original_input = { 'data': { 0: 'Red', 1: 'Yellow', 2:'Blue' }, 'output': span(0,1,2) }
        output_data = {0: 'Purple', 1: 'Green', 2: 'Orange'}
        transformed_text = [0, 1, 2]
        #inversion_mapping = {0: 'exists(0) or exists(2)', 1: 'exists(1) or exists(2)', 2: 'exists(0) or exists(1)'}
        #inversion_mapping = {0: 'E(0) or E(2)', 1: 'E(1) or E(2)', 2: 'E(0) or E(1)'}
        inversion_mapping = {0: 'E(0) or E(2)', 1: 'E(1) or E(2)', 2: 'E(0,1)'}
        return {
            'input': original_input,
            'imap': inversion_mapping,
            'data': output_data,
            'output': transformed_text
        }

    def test_cfim(self):
        mapping = self._test_prep()
        selected = span(0, 1)
        restored = restore(mapping, selected)
        expected = restore(mapping['input'])
        assert restored == expected, '%s %s'%(restored, expected)

    def _test_intervals(self):
        i1 = span((1,2), (2,5), (7, 11))
        assert all(r in i1 for r in range(1,6))
        assert all(r in i1 for r in range(7,12))

if __name__ == '__main__':
    unittest.main.main()
