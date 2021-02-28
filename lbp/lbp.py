#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import json
import matplotlib.pyplot as plt

class LBP:

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.logger = self.initLogger(self.verbose)
        self.logger.info("Starting LBP with attributes:\n" + json.dumps(kwargs))
        self.balance_usd = self.init_balance_usd
        self.weight_usd = self.init_weight_usd
        self.balance_token = self.init_balance_token
        self.weight_token = self.init_weight_token
        self.iteration = 0
        self.priceHistory = [self.computeRoundedPrice()]

    def initLogger(self, verbose):
        logger = logging.getLogger()
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - LBP_POOL - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        if verbose:
            logger.setLevel(logging.INFO)
            handler.setLevel(logging.INFO)            

        return logger         

    def step(self):
        self.iteration += 1
        self.updateWeights()
        self.priceHistory.append(self.computeRoundedPrice())

    def printPrice(self):
        self.logger.info("Iteration " + str(self.iteration) + ". Price: " + str(self.computeRoundedPrice()) + ". " + str(self.balance_token) + " tokens remaining.")
            
    def computePrice(self):
        if self.balance_token > 0:
            self.last_price = (self.balance_usd / self.weight_usd) / (self.balance_token / self.weight_token)
        return self.last_price

    def computeRoundedPrice(self):
        return round(self.computePrice(), 4)

    def updateWeights(self):
        self.weight_usd += self.weight_delta
        self.weight_token -= self.weight_delta

    def buyTokens(self, usd):
        if self.balance_token > 0:
            price = self.computePrice()
            tokens = usd/price
            if tokens < self.balance_token:
                self.logger.info("Buying " + str(tokens) + " tokens for $" + str(usd) + " at $" + str(price) + " per token.")
            elif tokens >= self.balance_token:
                tokens = self.balance_token
                usd = tokens * price
                self.logger.info("Buying ALL REMAINING (" + str(tokens) + ") tokens for $" + str(usd) + " at $" + str(price) + " per token.")
            else:
                self.logger.info("No Sale. Out of stock")
                usd = 0
                tokens = 0
            self.balance_usd += usd
            self.balance_token -= tokens

    def printPriceHistory(self):
        print("\n\n--- PRICE HISTORY ---")
        for i in range(len(self.priceHistory)):
            print("Iteration #" + str(i) + ":\t$" + str(self.priceHistory[i]))

    def printTokenBalance(self):            
        print("Remaining available tokens: " + '{:,}'.format(round(self.balance_token, 2)))
        
    def printChart(self):
        plt.plot(range(0, len(self.priceHistory)), self.priceHistory)
        plt.title("LBP Price chart for token in USD")
        plt.xlabel("Iterations")
        plt.ylabel("Price")
        plt.show()
