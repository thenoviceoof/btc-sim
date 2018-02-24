#!/usr/bin/env python3
################################################################################
# - All sims start with prices at $10k.
# - Each sim tracks transaction drag: graph both with and without.
# - Log axes galore.
################################################################################

import csv
import numpy.random
import tempfile
import random
import subprocess

SIMULATION_COUNT = 600

START_PRICE = 10000
# Based on highs of average $50 fees.
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
                 sell_point=2):
        self.crash_function = crash_function
        self.sell_function = sell_function
        self.transaction_proportion = transaction_proportion
        self.sell_point = sell_point

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
            outcomes.append({'fraction': sell_fraction, 'money': account.money})
        return outcomes
    
################################################################################
# Normal: l = $100k

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
print '1.1 Normal average:'
average = sum([d['money'] for d in real_money])/len(real_money)
print average
print '1.1 Normal stdev:'
print (sum([(average - d['money'])**2 for d in real_money])/(len(real_money)-1))**0.5
print '1.1 Normal fraction < start:'
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
# double improper beta

# TODO
