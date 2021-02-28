#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Simulator:

    def run(self, lbp, iterations, buyers, show_chart=True):
        lbp.printTokenBalance()
        lbp.printPrice()
        for i in range(iterations):
            for buyer in buyers:
                buyer.act(lbp)
            lbp.step()
            lbp.printPrice()

        lbp.printPriceHistory()
        lbp.printTokenBalance()
        if show_chart:
            lbp.printChart() 
