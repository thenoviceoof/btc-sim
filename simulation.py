#!/usr/bin/env python3
################################################################################
## Copyright 2018 "Nathan Hwang" <thenoviceoof>
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
################################################################################
# Assumptions:
# - All sims start with prices at $10k.
# - Each sim tracks transaction drag: graph both with and without.
################################################################################

import csv
import numpy.random
import tempfile
import random
import subprocess
import math

# This strikes a balance between graph readability and amount of data.
SIMULATION_COUNT = 600

START_PRICE = 10000
# Based on highs of average $50 fees for $10k BTC.
TRANSACTION_PROPORTION = 0.005

LAMBDA = 100000

def FN_NORMAL():
    return abs(numpy.random.normal(START_PRICE, LAMBDA - START_PRICE))

def FN_EXP():
    return numpy.random.exponential(LAMBDA - START_PRICE) + START_PRICE

class Account:
    def __init__(self,
                 sell_fraction,
                 sell_point=2,
                 transaction_proportion=TRANSACTION_PROPORTION):
        self.sell_fraction = sell_fraction
        self.sell_point = sell_point
        self.transaction_proportion = transaction_proportion

        self.price = START_PRICE
        self.btc = 1.0
        self.money = 0

    def reset(self):
        self.price = START_PRICE
        self.btc = 1.0
        self.money = 0

    def increment(self, crash_point):
        # Check if the next time we sell is above the crash point.
        if self.price * self.sell_point > crash_point:
            return False

        self.price *= self.sell_point

        # If we have enough money to cover the transaction fees...
        if self.btc > self.transaction_proportion:
            self.btc -= self.transaction_proportion
            self.money += self.btc * self.sell_fraction * self.price
            self.btc *= (1 - self.sell_fraction)

        return True

class Population(object):
    def __init__(self,
                 crash_function,
                 sell_function,
                 transaction_proportion,
                 sell_point=2,
                 live_function=None):
        self.crash_function = crash_function
        self.sell_function = sell_function
        self.transaction_proportion = transaction_proportion
        self.sell_point = sell_point
        self.live_function = live_function

    def simulate(self, account_count):
        outcomes = []
        for i in range(account_count):
            crash_point = self.crash_function()
            sell_fraction = self.sell_function()
            account = Account(sell_fraction,
                              transaction_proportion=self.transaction_proportion,
                              sell_point=self.sell_point)
            while account.increment(crash_point):
                pass
            outcome = {
                'fraction': sell_fraction,
                'money': account.money,
            }
            if self.live_function:
                if self.live_function(crash_point):
                    outcome['money'] += account.btc * crash_point
            outcomes.append(outcome)
        return outcomes
    
################################################################################
# Normal: l = $100k

# Might as well have deterministic random values.
random.seed(11)
numpy.random.seed(11)

ideal_population = Population(FN_NORMAL,
                              lambda: random.random(),
                              0)
ideal_money = ideal_population.simulate(SIMULATION_COUNT)

real_population = Population(FN_NORMAL,
                             lambda: random.random(),
                             TRANSACTION_PROPORTION)
real_money = real_population.simulate(SIMULATION_COUNT)

_, ideal_file = tempfile.mkstemp()
_, real_file = tempfile.mkstemp()

with tempfile.NamedTemporaryFile() as ideal_file, tempfile.NamedTemporaryFile() as real_file:
    ideal_writer = csv.DictWriter(ideal_file, ['fraction', 'money'])
    ideal_writer.writeheader()
    ideal_writer.writerows(ideal_money)
    ideal_file.flush()

    real_writer = csv.DictWriter(real_file, ['fraction', 'money'])
    real_writer.writeheader()
    real_writer.writerows(real_money)
    real_file.flush()

    # Run ggplot on the output.
    subprocess.call([
        'Rscript', 'plot.R',
        ideal_file.name, real_file.name, 'plot_normal.png']
    )

# Calculate expected money.
print 'Normal average:'
average = sum([d['money'] for d in real_money])/len(real_money)
print average
print 'Normal stdev:'
print (sum([(average - d['money'])**2 for d in real_money])/(len(real_money)-1))**0.5
print 'Normal fraction < start:'
print float(len([d for d in real_money if d['money'] < START_PRICE]))/len(real_money)
print ''

################################################################################
# Normal: l = $100k, 1.2x frequency

random.seed(11)
numpy.random.seed(11)

ideal_population = Population(FN_NORMAL,
                              lambda: random.random(),
                              0,
                              sell_point = 1.2)
ideal_money = ideal_population.simulate(SIMULATION_COUNT)

real_population = Population(FN_NORMAL,
                             lambda: random.random(),
                             TRANSACTION_PROPORTION,
                             sell_point = 1.2)
real_money = real_population.simulate(SIMULATION_COUNT)

_, ideal_file = tempfile.mkstemp()
_, real_file = tempfile.mkstemp()

with tempfile.NamedTemporaryFile() as ideal_file, tempfile.NamedTemporaryFile() as real_file:
    ideal_writer = csv.DictWriter(ideal_file, ['fraction', 'money'])
    ideal_writer.writeheader()
    ideal_writer.writerows(ideal_money)
    ideal_file.flush()

    real_writer = csv.DictWriter(real_file, ['fraction', 'money'])
    real_writer.writeheader()
    real_writer.writerows(real_money)
    real_file.flush()

    # Run ggplot on the output.
    subprocess.call([
        'Rscript', 'plot.R',
        ideal_file.name, real_file.name, 'plot_normal_1_2.png']
    )

# Calculate expected money.
print '1.2 Normal average:'
average = sum([d['money'] for d in real_money])/len(real_money)
print average
print '1.2 Normal stdev:'
print (sum([(average - d['money'])**2 for d in real_money])/(len(real_money)-1))**0.5
print '1.2 Normal fraction < start:'
print float(len([d for d in real_money if d['money'] < START_PRICE]))/len(real_money)
print ''

################################################################################
# exponential, but with 4x4 frequency/margin tradeoffs

# TODO

################################################################################
# Exponential: l = $100k

random.seed(11)
numpy.random.seed(11)

ideal_population = Population(FN_EXP,
                              lambda: random.random(),
                              0)
ideal_money = ideal_population.simulate(SIMULATION_COUNT)

real_population = Population(FN_EXP,
                             lambda: random.random(),
                             TRANSACTION_PROPORTION)
real_money = real_population.simulate(SIMULATION_COUNT)

_, ideal_file = tempfile.mkstemp()
_, real_file = tempfile.mkstemp()

with tempfile.NamedTemporaryFile() as ideal_file, tempfile.NamedTemporaryFile() as real_file:
    ideal_writer = csv.DictWriter(ideal_file, ['fraction', 'money'])
    ideal_writer.writeheader()
    ideal_writer.writerows(ideal_money)
    ideal_file.flush()

    real_writer = csv.DictWriter(real_file, ['fraction', 'money'])
    real_writer.writeheader()
    real_writer.writerows(real_money)
    real_file.flush()

    # Run ggplot on the output.
    subprocess.call([
        'Rscript', 'plot.R',
        ideal_file.name, real_file.name, 'plot_exponential.png']
    )

# Calculate expected money.
print 'Exponential average:'
average = sum([d['money'] for d in real_money])/len(real_money)
print average
print 'Exponential stdev:'
print (sum([(average - d['money'])**2 for d in real_money])/(len(real_money)-1))**0.5
print 'Exponential fraction < start:'
print float(len([d for d in real_money if d['money'] < START_PRICE]))/len(real_money)
print ''

################################################################################
# Bounded cap and survival chance.

random.seed(11)
numpy.random.seed(11)

# With $100T total market cap, and approximately $100B BTC market cap, we could
# assume a 1000x cap on BTC price increases, so $10k current -> max $10M.
MAX_VALUE_BTC = 10000000

def FN_EXP_NORMALIZED():
    # We just keep trying to find a stop point which fits under our
    # limit.
    value = numpy.random.exponential(2)
    while value > 2:
        value = numpy.random.exponential(2)

    # Transform the range 0-2 to the log $10k-$10M range.
    money_value = 10**(1.5*value + 4)
    assert money_value >= START_PRICE
    assert money_value <= MAX_VALUE_BTC

    return money_value

def FN_WEIRD_LIVE(crash_point):
    # This is a weird function: it's not normed, it's not even a
    # distribution. It's just mapping money to probability BTC
    # stabilizes instead of crashing, and totally made up.
    x = (math.log10(crash_point)-math.log10(START_PRICE))/(math.log10(MAX_VALUE_BTC)-math.log10(START_PRICE))
    survival_probability = (1 - x) * (x - 0.5)**2 + 0.99 * x**4 * 4**(1-x)
    assert survival_probability < 1.0
    assert survival_probability > 0.0
    return random.random() < survival_probability

ideal_population = Population(FN_EXP_NORMALIZED,
                              lambda: random.random(),
                              0,
                              live_function=FN_WEIRD_LIVE)
ideal_money = ideal_population.simulate(SIMULATION_COUNT)

real_population = Population(FN_EXP,
                             lambda: random.random(),
                             TRANSACTION_PROPORTION,
                             live_function=FN_WEIRD_LIVE)
# Include more points, since there's more noise.
real_money = real_population.simulate(2 * SIMULATION_COUNT)

_, ideal_file = tempfile.mkstemp()
_, real_file = tempfile.mkstemp()

with tempfile.NamedTemporaryFile() as ideal_file, tempfile.NamedTemporaryFile() as real_file:
    ideal_writer = csv.DictWriter(ideal_file, ['fraction', 'money'])
    ideal_writer.writeheader()
    ideal_writer.writerows(ideal_money)
    ideal_file.flush()

    real_writer = csv.DictWriter(real_file, ['fraction', 'money'])
    real_writer.writeheader()
    real_writer.writerows(real_money)
    real_file.flush()

    # Run ggplot on the output.
    subprocess.call([
        'Rscript', 'plot_bounded.R',
        ideal_file.name, real_file.name, 'plot_bounded.png']
    )

# Calculate expected money.
print 'Bounded average:'
average = sum([d['money'] for d in real_money])/len(real_money)
print average
print 'Bounded stdev:'
print (sum([(average - d['money'])**2 for d in real_money])/(len(real_money)-1))**0.5
print 'Bounded fraction < start:'
print float(len([d for d in real_money if d['money'] < START_PRICE]))/len(real_money)
print ''
