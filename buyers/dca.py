#!/usr/bin/env python
# -*- coding: utf-8 -*-

class DollarCostAverageBuyer:

    def __init__(self, price_per_buy, frequency, ceiling):
        self.price = price_per_buy
        self.frequency = frequency
        self.iterations = 0
        self.ceiling = ceiling
        
    def act(self, lbp):
        self.iterations += 1
        if (self.iterations % self.frequency) == 0 and lbp.computePrice() <= self.ceiling:
            lbp.buyTokens(usd=self.price)
