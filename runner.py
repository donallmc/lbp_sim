#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import json

from lbp.lbp import LBP
from buyers.factory import BuyerFactory
from simulator.simulator import Simulator

if len(sys.argv) != 2 or not sys.argv[1]:
    print("Must specify a config file for buyers. Usage: 'python runner.py <path_to_config>'")
    sys.exit()

#json config file specifying buyer strategies. Required. Also janky as fuck :D    
config_file = sys.argv[1]
try:
    buyer_config = json.load(open(config_file,))
except Exception as e:
    print("Error loading json config at '" + config_file + "'. Does file exist? And is json formatted correctly?")
    print("Error caused by: ")
    print(e)
    sys.exit()
factory = BuyerFactory()
buyers = factory.buildBuyers(buyer_config)

# the number of iterations is the number of times the pool should adjust weights. In this case it corresponds to 48 iterations, once per hour
iterations = 48

# will print info about each buy and the state of the pool at each iteration. Set to false for less noise
verbose = False

# set to True to plot the final price history (at hourly resolution). Requires matplotlib
show_chart = True

# most of these params are hopefully self-explanatory!
# The pool assumes prices will be listed in USD but you can treat is as anything.
# The init_balance_token is the number of tokens that are available for sale. This will reduce over time.
# The init_balance_usd is the amount of USD added to the pool initially. This will increase over time
# weight_delta is the change in weights (negative for the token, positive for usd)
lbp = LBP(
          weight_delta=0.9375,
          init_weight_usd=5,
          init_weight_token=95,
          init_balance_usd=650000,
          init_balance_token=13000000,
          verbose=verbose
    )

simulator = Simulator()
simulator.run(lbp, iterations, buyers, show_chart)
