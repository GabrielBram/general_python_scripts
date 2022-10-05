from chemsh import *
from ase.io import read

def cif2frac(charge_dict, in_fname, out_fname, origin_atom,
             cluster_r=40.0, active_r=20.0, bq_margin=5.0, bq_density=2.0, adjust_charge='coordination_scaled'):

    frag=chemsh.io.tools.convert_atoms_to_frag(read(in_fname))
    frag.addCharges(charge_dict)

    cluster=frag.construct_cluster(radius_cluster=40.0, origin_atom=280, adjust_charge='coordination_scaled',
                                       radius_active=20.0, bq_margin=5.0, bq_density=2)

    # Saving cluster
    cluster.save(out_fname+'.pun', 'pun')
    cluster.save(out_fname+'.xyz', 'xyz')
