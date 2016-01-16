
# import csv
import pandas as pd
import os
import json

from fermi2.model.component import Component
from fermi2.model.estimate import Estimate

FNAME = 'microsoft_word_man_months'

INPUT_FILE = os.path.abspath('.') + '/fermi2/data/' + FNAME + '.csv'
INPUT_FILE_ESTIMATE = os.path.abspath('.') + '/fermi2/data/' + FNAME + '.json'

# read in components
with open(INPUT_FILE, 'r') as f:
	df = pd.read_csv(f)
	data = df.to_dict(orient='records')
components = {c['var']:Component(**c) for c in data}

# read in estimate
with open(INPUT_FILE_ESTIMATE, 'r') as f:
	indata = json.load(f)
	indata['component_dict'] = components
# indata = json.load{'name': 'number of people in the air at this moment',
# 		  'var_name': 'num_ppl_in_air',
# 		  'expression_str': '50 * airport_per_state * flight_per_airport * ppl_per_flight',
# 		  'component_dict': components,
# 		  'actual': 100000,
# 		  'source': 'www.google.com'}
estimate = Estimate(**indata)

# run simulations
estimate.simulate(num_runs=1000)
# make a plot of the simulations
estimate.plot()
