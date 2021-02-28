#!/usr/bin/env python
# -*- coding: utf-8 -*-

class FOMOBuyer:

    def __init__(self, target_low, target_high, budget, ceiling):
        self.target_low = target_low
        self.target_high = target_high
        self.budget = budget        
        self.bought = False
        self.ceiling = ceiling

    def act(self, lbp):
        price = lbp.computePrice()
        if self.bought == False and (self.target_low >= price or self.target_high <= price) and price <= self.ceiling:
            lbp.buyTokens(usd=self.budget)
            self.bought = True

