#!/bin/python3

# WILL MAKE INTO PROGRAM LATER, BUT THIS IS A SET OF SCRIPTS
# DESIGNED FOR AN EXTENDABLE, GENERAL PURPOSE FILE READER.

def read_aims_file(res_fil):

    # DICTIONARY STRUCTURE: 0: index, 1: string match, 2: row number of value, 3: block_length 4: offset.
    # First few dictionary itemsx are saved for basic information (ie., atoms nos)
    # which are needed for reading other dictionary items
    binfo_ind_dict = ind_dict_gen('aims')
    
    # THIS READS EVERYTHING FROM THE AIMS FILE. :) 
    binfo_dict = aimsread(res_fil,binfo_ind_dict)

    return binfo_dict

def get_value_file_loop(key, root_dir, filename, ind1=0, ind2=0, dict_type='aims'):

    import os

    dirs = os.listdir(root_dir)

    dir_list = [os.path.join(root_dir,directory) for directory in dirs if (os.path.isdir(os.path.join(root_dir,directory)) and not directory.startswith('.'))]

    dir_list = sorted(dir_list)

    # Messy stop gap - need to know whether dictionary element being read is a nested list or not.
    binfo_ind_dict = ind_dict_gen('aims')

    if(type(binfo_ind_dict[key][2])==list):
       values = [float(read_aims_file(os.path.join(_dir,filename))[key][ind1][ind2]) for _dir in dir_list]
    else:
       values = [float(read_aims_file(os.path.join(_dir,filename))[key][ind1]) for _dir in dir_list]

    return values
   

def aimsread(res_fil,ind_dict):
    
    import copy
    
    # input - name of file
    # output - list of indices
    
    # Define output directory based on input directory.
    output_dict = copy.deepcopy(ind_dict)

    for key in output_dict:
        output_dict[key].clear()

    with open(res_fil, "r") as file:
        
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        # First, establish the atom number for future reference.
        
        nat_line,npsp_line=-1,-1
        for line_no, line in enumerate(lines):
            
            nat_line=line_grab(line,line_no,ind_dict['n_at'][1],nat_line
                                          ,block_len=ind_dict['n_at'][3],offset=ind_dict['n_at'][4])
            npsp_line=line_grab(line,line_no,ind_dict['n_pseudo'][1],npsp_line
                                          ,block_len=ind_dict['n_pseudo'][3],offset=ind_dict['n_pseudo'][4])

        if len(npsp_line)==1:
            n_at=ind2val(lines,nat_line,ind_dict['n_at'][2])
            n_psp=ind2val(lines,nat_line,ind_dict['n_pseudo'][2])
            # Set the block length for whichever species require it.
            ind_dict['final_forces'][3]=int(n_at[0])+int(n_psp[0])
        else:
            n_at=ind2val(lines,nat_line,ind_dict['n_at'][2])
            ind_dict['final_forces'][3]=int(n_at[0])

        #print(f"{n_at[0]},{n_psp},{ind_dict['final_forces'][3]}")
        # Now loop through the lines for all dictionary items
        for line_no, line in enumerate(lines):
            
            for key in ind_dict:
                ind_dict[key][0]=line_grab(line,line_no,ind_dict[key][1],ind_dict[key][0]
                                           ,block_len=ind_dict[key][3],offset=ind_dict[key][4])

        for key in ind_dict:
            output_dict[key]=ind2val(lines,ind_dict[key][0],ind_dict[key][2])

    return output_dict



def ind2val(lines,dict_item,row_nums):

    val = []
    for idx in dict_item:
        spl_line=lines[idx].split()
    
        if not isinstance(row_nums,list):
            val.append(spl_line[row_nums])
    
        else:
            val.append([spl_line[idx] for idx in row_nums])
        
    return val

def line_grab(line,line_no,string,ind_dict,block_len=0,offset=0):

    if block_len == 0:

        if ind_dict==-1:
            ind_dict=[]

        val = single_line_grab(line,line_no,string,ind_dict,offset)

    if block_len > 0:

        if ind_dict==-1:
            ind_dict=[]

        val = block_line_grab(line,line_no,string,ind_dict,block_len,offset)
        
    if val!=None:
        ind_dict=val
        return ind_dict
    
    else:
        return ind_dict
        
def single_line_grab(line,line_no,string,ind_dict,offset):

    found = line.startswith(string)

    if found:
        ind_dict.append(line_no + offset)

        return ind_dict
    
    else:
        return None

def block_line_grab(line,line_no,string,ind_dict,block_len,offset):

    found = line.startswith(string)
    
    if found:
        for idx in range(block_len):
            ind_dict.append(line_no+idx+offset)
            
        return ind_dict
    
    else:
        return None

def ind_dict_gen(dict_type):

    if dict_type=='aims':

        inp_dict={"n_at":[-1,'| Number of atoms', 5, 0, 0],"n_sp":[-1,'| Number of species', 5, 0, 0], "n_pseudo": [-1,'| Number of pseudocores', 5, 0, 0]
                ,"n_sp_pseudo": [-1,'| Number of pseudoized species', 6, 0, 0], "final_energy":[-1,'| Total energy uncorrected',5, 0, 0]
                  ,"pre_final_forces":[-1,'Total forces',[4,5,6], 0, 0], "final_forces":[-1,'Total atomic forces',[2,3,4], 0, 1]
                  ,"pp_gga_forces":[-1,'Final GGA Forces',4, 0, 0] ,"pp_lda_forces":[-1,'Final LDA Forces',4, 0, 0]
                  ,"nlcc_energy":[-1]:[-1,"| nonlinear core correction", 7, 0, 0]
                }

        return inp_dict

    else:
        
        raise Exception('Invalid input type. Need dictionary to load values into.')
