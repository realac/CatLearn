""" Script to test the database functions. """
from __future__ import print_function

from os import remove
from random import random

from ase.ga.data import DataConnection
from atoml.fingerprint_setup import return_fpv
from atoml.particle_fingerprint import ParticleFingerprintGenerator
from atoml.database_functions import DescriptorDatabase

# Define variables for database to store system descriptors.
db_name = 'fpv_store.sqlite'
names = ['AA', 'AB', 'BA', 'BB', 'Energy']
descriptors = ['AA', 'AB', 'BA', 'BB']
targets = ['Energy']

# Set up the database to save system descriptors.
dd = DescriptorDatabase(db_name=db_name,  table='FingerVector')
dd.create_db(names=names)

# Connect database generated by a GA search.
gadb = DataConnection('gadb.db')

# Get all relaxed candidates from the db file.
print('Getting candidates from the database')
all_cand = gadb.get_all_relaxed_candidates(use_extinct=False)

fpv = ParticleFingerprintGenerator(get_nl=False, max_bonds=13)
data = return_fpv(all_cand, [fpv.nearestneighbour_fpv])
new_data = []
for i, a in zip(data, all_cand):
    d = []
    d.append(a.info['unique_id'])
    for j in i:
        d.append(j)
    d.append(a.info['key_value_pairs']['raw_score'])
    new_data.append(d)

dd.fill_db(descriptor_names=names, data=new_data)

train_fingerprint = dd.query_db(names=descriptors)
train_target = dd.query_db(names=targets)
print(train_fingerprint, train_target)

cand_data = dd.query_db(unique_id='7a216711c2eae02decc04da588c9e592')
print(cand_data)

all_id = dd.query_db(names=['uuid'])
dd.create_column(new_column=['random'])
for i in all_id:
    dd.update_descriptor(descriptor='test', new_data=random(), unique_id=i[0])
print(dd.query_db(names=['random']))

print(dd.get_column_names())

remove(db_name)
