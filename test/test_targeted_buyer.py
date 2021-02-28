#!/usr/bin/env python

from buyers.targeted import TargetedBuyer
import unittest
from unittest import mock

class TestTargetedBuyer(unittest.TestCase):

    def buildBuyer(self, target=10, price_per_buy=100):
        return TargetedBuyer(target, price_per_buy)

    def testBuy(self):
        lbp_price = 0.1
        price_per_buy = 100
        target = 10
        buyer = self.buildBuyer(target=target, price_per_buy=price_per_buy)

        lbp_mock = mock.Mock()
        lbp_mock.computePrice.return_value = lbp_price
        
        buyer.act(lbp_mock)
        
        lbp_mock.computePrice.assert_called_once()
        lbp_mock.buyTokens.assert_called_once()        
        assert lbp_mock.buyTokens.call_args == mock.call(usd=price_per_buy)

    #Target buyer is stoically waiting for the price to dip below his target and then he's putting all his chips in at once. He ignores the market after one successful buy
    def testBuysOnlyOnce(self):
        lbp_price = 0.1
        price_per_buy = 100
        target = 10
        buyer = self.buildBuyer(target=target, price_per_buy=price_per_buy)
        
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


    #Targeted buyer waits to hit his target and won't buy if the price is high, no matter what
    #However, he loses his composure and panic-buys above a certain value
    def testNoBuyAboveCeiling(self):
        lbp_price = 11
        target = 10
        buyer = self.buildBuyer(target=target)
        
        for i in range(100):
            lbp_price += 1
            lbp_mock = mock.Mock()
            lbp_mock.computePrice.return_value = lbp_price
            
            buyer.act(lbp_mock)

            self.assertFalse(lbp_mock.buyTokens.called)


        
