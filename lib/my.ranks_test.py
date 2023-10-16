
import unittest

from ui.tabular.models.Ranks import Ranks

class Ranks_test(unittest.TestCase):
    
    def testFlushes(self):
        fixture = Ranks()
        fixture.build()

if __name__ == "__main__":
    unittest.main()

