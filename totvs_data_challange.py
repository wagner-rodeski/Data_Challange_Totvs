# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 08:09:22 2018

@author: wagner_rodeski
"""

import pandas as pd

base = pd.read_table ('sample.txt', names = {'teste'}, skiprows = 1)

base_2 = base.drop(base[(base['teste'].str.contains('],')) | (base['teste'] == '{') |
        (base['teste'] == ',{') | (base['teste'] == '}') |
        (base['teste'].str.contains('  {')) | (base['teste'].str.contains(' }'))].index)

base_2.reset_index(inplace = True)

base_2.drop('index', axis = 1, inplace = True)

base_3 = base_2['teste'].str.strip('" "{}[],"')

base_4 = base_3.str.split(':', expand=True, n = 1)

base_4.rename(columns = {0:'nome_campo',1:'valor'}, inplace = True)

base_4['nome_campo'] = base_4['nome_campo'].str.strip('"')
base_4['valor'] = base_4['valor'].str.strip(' "')

base_4.dropna(inplace = True)

campos = base_4['nome_campo'].unique().tolist()

base_4['customer_id'] = ''
k = 0
for i in base_4.index:
    if base_4['nome_campo'][i]  == 'complemento':
        k = k + 1
        base_4['customer_id'][i] = k
    base_4['customer_id'][i] = k

base_4.head(20)

base_5 = base_4[['nome_campo', 'valor', 'customer_id']].where((base_4['nome_campo'] == 'vnf')|
        (base_4['nome_campo'] == 'nItem')|(base_4['nome_campo'] == '$date')).dropna()

base_5 = base_5.groupby(['customer_id', 'nome_campo']).max()
base_5 = base_5.reset_index()

base_6 = base_5.pivot(index = 'customer_id', columns = 'nome_campo', values = 'valor')

