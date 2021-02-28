#!/usr/bin/env python

from lbp.lbp import LBP
import unittest
from unittest import mock

class TestFOMOBuyer(unittest.TestCase):

    def buildLBP(self):
        return LBP(
            weight_delta=0.9375,
            init_weight_usd=5,
            init_weight_token=95,
            init_balance_usd=650000,
            init_balance_token=13000000,
            verbose=False
        )
    
    def testLBPComputesPricesCorrectlyWithNoBuys(self):
        lbp = self.buildLBP()
        iterations = 48

        for i in range(iterations):
            lbp.step()

        #num iterations + 1 because the price history includes the initial price and then performs n iterations
        self.assertEqual(len(lbp.priceHistory), iterations + 1)
        self.assertEqual(lbp.priceHistory, [0.95, 0.7921, 0.6773, 0.59, 0.5214, 0.4661, 0.4206, 0.3824, 0.35, 0.3221, 0.2978, 0.2765, 0.2577, 0.2409, 0.2259, 0.2123, 0.2, 0.1888, 0.1786, 0.1692, 0.1605, 0.1525, 0.1451, 0.1382, 0.1318, 0.1258, 0.1202, 0.1149, 0.11, 0.1053, 0.1009, 0.0968, 0.0929, 0.0891, 0.0856, 0.0822, 0.079, 0.076, 0.0731, 0.0703, 0.0676, 0.0651, 0.0627, 0.0603, 0.0581, 0.056, 0.0539, 0.0519, 0.05])


    def testPriceUnchanged(self):
        lbp = self.buildLBP()
        init_price = 0.95
        price = lbp.computeRoundedPrice()
        self.assertEqual(price, init_price)
        price = lbp.computeRoundedPrice()
        self.assertEqual(price, init_price)

    def testPriceChangeAfterWeightChange(self):
        lbp = self.buildLBP()
        init_price = 0.95
        price = lbp.computeRoundedPrice()
        price_after_step = 0.7921
        self.assertEqual(price, init_price)
        lbp.step()
        price = lbp.computeRoundedPrice()
        self.assertEqual(price, price_after_step)
        self.assertTrue(init_price > price_after_step)

    def testPriceChangeAfterBuy(self):
        lbp = self.buildLBP()
        init_price = 0.95
        price = lbp.computeRoundedPrice()
        price_after_buy = 0.9515
        self.assertEqual(price, init_price)
        lbp.buyTokens(1000)
        price = lbp.computeRoundedPrice()
        self.assertEqual(price, price_after_buy)
        self.assertTrue(init_price < price_after_buy)


    def testPriceChangeAfterBuyAndStep(self):
        lbp = self.buildLBP()
        init_price = 0.95
        price = lbp.computeRoundedPrice()
        price_after = 0.7934
        self.assertEqual(price, init_price)
        lbp.buyTokens(1000)
        lbp.step()
        price = lbp.computeRoundedPrice()
        self.assertEqual(price, price_after)

    def testBuyReducesStock(self):
        lbp = self.buildLBP()
        budget = 95
        init_token_supply = 13000000
        self.assertEqual(lbp.balance_token, init_token_supply)

        price = lbp.computePrice()
        lbp.buyTokens(budget)
        new_supply = lbp.balance_token
        self.assertEqual(new_supply, init_token_supply - (budget/price))        
    
        price = lbp.computePrice()
        lbp.buyTokens(budget)
        self.assertEqual(lbp.balance_token, new_supply - (budget/price))        

        
        
    def testBuyTooMuch(self):
        lbp = self.buildLBP()
        self.assertEqual(lbp.balance_token, 13000000)
        lbp.buyTokens(12350000)
        self.assertEqual(lbp.balance_token, 0)

        lbp = self.buildLBP()
        self.assertEqual(lbp.balance_token, 13000000)
        lbp.buyTokens(999999999999999999999)
        self.assertEqual(lbp.balance_token, 0)        
