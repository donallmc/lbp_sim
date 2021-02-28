#!/usr/bin/env python

from buyers.allinatstart import AllInAtStartBuyer
import unittest
from unittest import mock

class TestAllInAtStartBuyer(unittest.TestCase):

    def buildBuyer(self, price_per_buy=100, ceiling=10):
        return AllInAtStartBuyer(price_per_buy, ceiling)

    def testBuy(self):
        lbp_price = 0.1
        price_per_buy = 100
        buyer = self.buildBuyer(price_per_buy=price_per_buy)

        lbp_mock = mock.Mock()
        lbp_mock.computePrice.return_value = lbp_price
        
        buyer.act(lbp_mock)
        
        lbp_mock.computePrice.assert_called_once()
        lbp_mock.buyTokens.assert_called_once()        
        assert lbp_mock.buyTokens.call_args == mock.call(usd=price_per_buy)

    #AllInAtStart buyer is a bot. It is looking to buy as soon as the liquidity is available.
    #It should ignore the market after the initial buy
    def testBuysOnlyOnce(self):
        lbp_price = 0.1
        price_per_buy = 100
        buyer = self.buildBuyer(price_per_buy=price_per_buy)
        
        for i in range(10):
            lbp_mock = mock.Mock()
            lbp_mock.computePrice.return_value = lbp_price
            
            buyer.act(lbp_mock)

            if (i == 0):
                lbp_mock.computePrice.assert_called_once()
                lbp_mock.buyTokens.assert_called_once()
                assert lbp_mock.buyTokens.call_args == mock.call(usd=price_per_buy)
            else:
                self.assertFalse(lbp_mock.buyTokens.called)  


    ##AllInAtStart buyer is programmed with a ceiling above which it shouldn't make any buys, in case it gets out-botted by other bots and the price spikes                
    def testNoBuyAboveCeiling(self):
        lbp_price = 20
        buyer = self.buildBuyer(ceiling=15)

        lbp_mock = mock.Mock()
        lbp_mock.computePrice.return_value = lbp_price

        buyer.act(lbp_mock)
        lbp_mock.computePrice.assert_called_once()
        self.assertFalse(lbp_mock.buyTokens.called)


        
