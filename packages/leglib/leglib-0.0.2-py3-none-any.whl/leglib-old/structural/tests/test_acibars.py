from structural.acibars import Rebar
from structural.acibars import get_bar
import unittest


class TestRebar(unittest.TestCase):

    def test_name(self):
        no3 = get_bar(3)
        self.assertEqual("#3", "%s" % no3)
        no5 = get_bar("#5")
        self.assertEqual("#5", "%s" % no5)


if __name__ == '__main__': # pragma: no cover
    unittest.main()
