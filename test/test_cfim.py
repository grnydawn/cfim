from context import cfim
import unittest
from cfim import restore

class TestParser(unittest.TestCase):

    def _test_prep(self):
        original_text = 'Red'
        transformed_text = 'Blue'
        inversion_mapping = {(0,3): 'exists((0,4))'}
        return {
            'input': original_text,
            'imap': inversion_mapping,
            'output': transformed_text
        }

    def test_cfim(self):
        mapping = self._test_prep()
        selected = ( 0, (1, 4) )
        restored = restore(mapping, selected)
        expected = mapping['input']
        assert restored == expected

if __name__ == '__main__':
    unittest.main.main()
