#!/usr/bin/env python3

"""
Example script showing how to add a hydrogen to a zeolite cluster,
then add and rotate an ethanol molecule to the desired position.
"""

from ase.io import read, write
from ase.build import molecule
from ase import Atoms
from ase.visualize import view
import numpy as np

from carmm.build.adsorbate_placer import place_adsorbate, rotate_and_place_adsorbate

molecule = molecule('CH3OH')
h_atom = read('h_atom.xyz')
site = read('cluster.xyz')

zeolite, rotated_h = place_adsorbate(h_atom, site, 0, 2, 1.0, lps=2, lp_idx=0)
#zeolite, rotated_h = place_adsorbate(h_atom, zeolite, 0, 3, 1.0, lps=1, lp_idx=1)

write("zeolite.xyz", zeolite)


ads_and_site, rotated_ads = rotate_and_place_adsorbate(molecule, zeolite, 1.5,
                                                       1, 0, 0,
                                                       rotation=[0, 45, -90],
                                                       lps=1, lp_idx=0)

view(ads_and_site[0:60])
write("zeolite.xyz",zeolite)
write("methanol_MFI.xyz",ads_and_site)
write("rotated_methanol.xyz",rotated_ads)
write("h_atom.xyz",rotated_h)

