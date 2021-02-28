#!/usr/bin/env python

from buyers.fomo import FOMOBuyer
import unittest
from unittest import mock

class TestFOMOBuyer(unittest.TestCase):

    def buildBuyer(self, low=1, high=10, price_per_buy=100, ceiling=10):
        return FOMOBuyer(low, high, price_per_buy, ceiling)

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

    #FOMO buyer has a fixed budget and he is looking to buy as soon as the price hits either of his targets (low target and high FOMO target). After one buy he should always ignore the market because he already made his buy.
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


    #FOMO buyer waits to hit his target and won't buy if the price is high                
    def testNoBuyBelowLowTarget(self):
        lbp_price = 2
        buyer = self.buildBuyer(low=1)

        lbp_mock = mock.Mock()
        lbp_mock.computePrice.return_value = lbp_price

        buyer.act(lbp_mock)

        lbp_mock.computePrice.assert_called_once()
        self.assertFalse(lbp_mock.buyTokens.called)

    #FOMO buyer waits to hit his target and won't buy if the price is high
    #However, he loses his composure and panic-buys above a certain value
    def testBuyAboveHighTarget(self):
        lbp_price = 11
        price_per_buy = 100
        buyer = self.buildBuyer(high=10, ceiling=15, price_per_buy=100)

        lbp_mock = mock.Mock()
        lbp_mock.computePrice.return_value = lbp_price

        buyer.act(lbp_mock)
        
        lbp_mock.computePrice.assert_called_once()
        lbp_mock.buyTokens.assert_called_once()        
        assert lbp_mock.buyTokens.call_args == mock.call(usd=price_per_buy)

    #FOMO buyer waits to hit his target and won't buy if the price is high
    #However, he loses his composure and panic-buys above a certain value
    def testNoBuyAboveCeiling(self):
        lbp_price = 20
        buyer = self.buildBuyer(high=10, ceiling=15)

        lbp_mock = mock.Mock()
        lbp_mock.computePrice.return_value = lbp_price

        buyer.act(lbp_mock)
        lbp_mock.computePrice.assert_called_once()
        self.assertFalse(lbp_mock.buyTokens.called)


        
