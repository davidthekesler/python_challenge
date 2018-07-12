# vim: ts=4:sw=4:expandtabs

__author__ = 'theddavidkesler@gmail.com'
__doc__ = """

"""


from python_coding_test_david_kesler import Account

from python_coding_test_david_kesler import MarketSegment

import unittest
 
class MarketSegmentTest(unittest.TestCase):
 
    def setUp(self):
 
        self.marketSegment1 = MarketSegment("wheat")
        self.marketSegment2 = MarketSegment("corn")

        self.account1 = Account("account1")
        self.account2 = Account("account2")
 
         
    def test_add_account(self):
 
        self.marketSegment1.add_account(self.account1)
        self.marketSegment1.add_account(self.account1)

        if len(self.marketSegment1._accounts) > 1:
            raise ValueError("The same account can't be added more than once to a single market segment.")

    def test_set_market_segments(self):

        self.account1.set_market_segments([self.marketSegment1, self.marketSegment1])

        if len(self.account1._market_segments) > 1:
            raise ValueError("The same market segment can't be added more than once to a single account.")
            
if __name__ == '__main__':
    unittest.main()
 
