
import unittest

from ui.tabular.models.Cards import Cards

class Cards_test(unittest.TestCase):
    
    def testKindkey(self):
        fixture = Cards(["2c", "2d", "2h", "2s", "3c"])
        expected = "STTTT"
        self.assertEqual(fixture.kindkey(), expected)
    
    def testSuitkey(self):
        fixture = Cards(["2c", "2d", "2h", "2s", "3c"])
        expected = "2111"
        self.assertEqual(fixture.suitkey(), expected)
    
    def testNumbkey(self):
        fixture = Cards(["2c", "2d", "2h", "2s", "3c"])
        expected = 2**4 + 3**1
        self.assertEqual(fixture.numbkey(), expected)
    
    def testHandkey(self):
        fixture = Cards(["2c", "2d", "2h", "2s", "3c"])
        expected = "STTTT.2111"
        self.assertEqual(fixture.handkey(), expected)
    
    def testAdd(self):
        fixture = Cards(["2c", "2d", "2h", "2s", "3c"])
        fixture.add("3d")
        fixture.add("3h")
        expected = "SSSTTTT.2221"
        self.assertEqual(fixture.handkey(), expected)

if __name__ == "__main__":
    unittest.main()

