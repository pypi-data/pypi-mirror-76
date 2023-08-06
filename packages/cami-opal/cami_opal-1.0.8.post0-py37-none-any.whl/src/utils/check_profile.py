#!/usr/bin/env python3
from src.utils import load_data
from src.utils import load_ncbi_taxinfo

PROFILE = '/home/fmeyer/Opal/mouse_gut/gs.profile'
NODES = '/home/fmeyer/cami2/taxdump_cami2_toy/nodes.dmp'


samples_list = load_data.open_profile_from_tsv(PROFILE, False)

tax_id_to_parent, tax_id_to_rank = load_ncbi_taxinfo.load_tax_info(NODES)

for sample in samples_list:
    # sample is a tuple -> (header['SAMPLEID'], header, profile)
    for prediction in sample[2]:
        for i, tax_id in enumerate(prediction.taxpath.split('|')):
            if tax_id in tax_id_to_rank and tax_id_to_rank[tax_id] != load_ncbi_taxinfo.RANKS[i]:
                print('{} {}'.format(sample[0], prediction.taxid))
                continue
