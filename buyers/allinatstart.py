#!/usr/bin/env python
# -*- coding: utf-8 -*-

class AllInAtStartBuyer:

    def __init__(self, price_per_buy, ceiling):
        self.price = price_per_buy
        self.ceiling = ceiling
        self.iterations = 0

    def act(self, lbp):
        self.iterations += 1
        if self.iterations == 1 and lbp.computePrice() <= self.ceiling:
            lbp.buyTokens(usd=self.price)            
