def get_interlayer_distances(surface,out_filname,append_symbol):

    #
    # Non-robust method of finding interlayer distances and dumping them into a text file.
    # Evaluates by chemical element.
    #

    from time import time, ctime
    import numpy as np
    import os

    symbols=surface.get_chemical_symbols()
    sort_bool= [False for i in range(len(symbols))]

    unique_symbols=set(surface.get_chemical_symbols())
    z_positions=surface.get_positions()[:,2]

    layer_dict={}
    layer_dist_dict={}

    for symbol in unique_symbols:

        mask=[list_symb==symbol for list_symb in symbols]
        value_element=np.sort(np.extract(mask,z_positions))
        layer_dict[symbol]=[]

        for num, val_element in enumerate(value_element):

            if not sort_bool[num]:
                sort_bool=np.abs(value_element - value_element[num])<0.5

                layer_z=np.mean(np.extract(sort_bool,value_element))

                layer_dict[symbol].append(layer_z)

                
    for key, layer in layer_dict.items():
        layer_dist_dict[key] = [x - layer[i-1] for i, x in enumerate(layer)][1:]

    if not os.path.exists(out_filname):
        with open(out_filname,'a+') as output:

            timeanddate = ctime(time())

            output.write('Interlayer distances for run at: '+timeanddate+'\n')
            output.write('Element,d12,d23,d34,d45,d56'+'\n')
        
    with open(out_filname,'a+') as output:
    
        for key, layer in layer_dist_dict.items():
            output.write(key+append_symbol+',')
            for distance in layer[:-1]:
                output.write(str(distance)+',')
                
            # Makes sure comma doesn't appear on last element
            output.write(str(layer[-1]))
            output.write('\n')
        
    return
