#!/usr/bin/env python3

import pandas as pd

x = pd.read_csv('/home/fmeyer/cami2/datasets/strain_madness/metaquast_megahit_short/all_alignments_strain_madness_fixed_best_w_length.binning', sep='\t', header=None)
x.rename(columns={0: 'SEQUENCEID', 1: 'BINID', 2: 'LENGTH'}, inplace=True)
print(x)
x = x.drop_duplicates(['SEQUENCEID', 'BINID'])
print(x)
