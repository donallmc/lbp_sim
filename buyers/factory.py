#!/usr/bin/env python
# -*- coding: utf-8 -*-

from buyers.allinatstart import *
from buyers.dca import *
from buyers.fomo import *
from buyers.targeted import *

'''
This is REALLY janky. Forgive me.

These configs are not truly serialized objects. They're really badly 
designed and hurriedly thrown-together JSON config objects. The intent
is to make this project accessible to people who aren't comfortable
coding python by given them a JSON-based configuration language.

If this should ever get used for anything serious, this class is probably
the first thing to get replaced!

'''
class BuyerFactory:
    def buildBuyers(self, buyersConfigList):
        buyers = []
        for config in buyersConfigList:
            buyerType = config["type"]
            if not buyerType:
                RuntimeError("No buyer type specified in config")
            elif buyerType == "AllInAtStart":
                for i in range(config["count"]): #TODO: ugh. Reformat this to not repeat these. Also redesign the config!!
                    buyers.append(AllInAtStartBuyer(config["budget"], config["ceiling"]))
            elif buyerType == "DollarCostAverage":
                for i in range(config["count"]):
                    buyers.append(DollarCostAverageBuyer(config["budget_per_buy"], config["frequency"], config["ceiling"]))
            elif buyerType == "TargetBuyer":
                for i in range(config["count"]):
                    buyers.append(TargetedBuyer(config["target"], config["budget"]))
            elif buyerType == "FOMOBuyer":
                for i in range(config["count"]):
                    buyers.append(FOMOBuyer(config["target_low"], config["target_high"], config["budget"], config["ceiling"]))
            else:
                RuntimeError("Unexpected buyer type: " + buyerType + ". If you are adding buyer types then please update the BuyerFactory")    

                    
        return buyers
