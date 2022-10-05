from chemsh       import *
from chemsh.io.tools import *
from ase.io import read

# Creation of zeolite cluster fragment
precluster = Fragment(coords='cluster.pun', connect_mode='covalent')
h_atom     = convert_atoms_to_frag(read('h_atom.xyz'))
precluster.names[0] = 'Al'
precluster.znums[0] = '13'

precluster.append(h_atom)

precluster.save('zsm5.pun', 'pun')
precluster.save('zsm5.xyz', 'xyz')

zsm5 = Fragment(coords='zsm5.pun', connect_mode='covalent')
methanol =  convert_atoms_to_frag(read('rotated_methanol.xyz'))

zsm5.append(methanol)

zsm5.save('adsorbate_and_cluster.pun','pun')
zsm5.save('adsorbate_and_cluster.xyz','xyz')
