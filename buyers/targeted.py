#!/usr/bin/env python
# -*- coding: utf-8 -*-

class TargetedBuyer:

    def __init__(self, target, budget):
        self.target = target
        self.budget = budget        
        self.bought = False

    def act(self, lbp):
        if self.bought == False and self.target >= lbp.computePrice():
            lbp.buyTokens(usd=self.budget)
            self.bought = True
