#!/usr/bin/env python

from buyers.dca import DollarCostAverageBuyer
import unittest
from unittest import mock

class TestDCABuyer(unittest.TestCase):

    def buildBuyer(self, price_per_buy=100, frequency=1, ceiling=10):
        return DollarCostAverageBuyer(price_per_buy, frequency, ceiling)

    def testBuy(self):
        lbp_price = 1
        price_per_buy = 100
        buyer = self.buildBuyer(price_per_buy=price_per_buy)

        lbp_mock = mock.Mock()
        lbp_mock.computePrice.return_value = lbp_price
        
        buyer.act(lbp_mock)
        
        lbp_mock.computePrice.assert_called_once()
        lbp_mock.buyTokens.assert_called_once()        
        assert lbp_mock.buyTokens.call_args == mock.call(usd=price_per_buy)

    def testBuysEveryTime(self):
        lbp_price = 1
        price_per_buy = 100
        buyer = self.buildBuyer(price_per_buy=price_per_buy)
        
        for i in range(10):
            lbp_mock = mock.Mock()
            lbp_mock.computePrice.return_value = lbp_price
            
            buyer.act(lbp_mock)

            lbp_mock.computePrice.assert_called_once()
            lbp_mock.buyTokens.assert_called_once()
            assert lbp_mock.buyTokens.call_args == mock.call(usd=price_per_buy)


    def testNoBuyAboveCeiling(self):
        lbp_price = 20
        ceiling = 10
        buyer = self.buildBuyer(ceiling=ceiling)

        lbp_mock = mock.Mock()
        lbp_mock.computePrice.return_value = lbp_price

        buyer.act(lbp_mock)

        lbp_mock.computePrice.assert_called_once()
        self.assertFalse(lbp_mock.buyTokens.called)


    #This is easily the least intuitive aspect. The "frequency" param governs how frequently the DCA buyer will
    #buy tokens. The default (1) is every time. '2' will be every second time, '3' every third time, etc.
    def testFrequency(self):
        lbp_price = 1
        price_per_buy = 100
        frequency = 5
        buyer = self.buildBuyer(price_per_buy=price_per_buy, frequency=frequency)
        
        for i in range(1, 15):
            lbp_mock = mock.Mock()
            lbp_mock.computePrice.return_value = lbp_price
            
            buyer.act(lbp_mock)

            if (i % frequency != 0):
                self.assertFalse(lbp_mock.computePrice.called)
                self.assertFalse(lbp_mock.buyTokens.called)
            else:             
                lbp_mock.computePrice.assert_called_once()
                lbp_mock.buyTokens.assert_called_once()
                assert lbp_mock.buyTokens.call_args == mock.call(usd=price_per_buy)        
