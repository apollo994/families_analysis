#!/usr/bin/env python3


import sys
import argparse
from collections import defaultdict
import pandas as pd

################################################################################

def get_species_list(input_file):

    sp_list=[]

    for i in input_file:
        sp=i.split("/")[-1]
        sp=sp.split("_")[0]
        sp_list.append(sp)

    return sp_list

################################################################################

def get_fam_dfs(input_file, sp_list):

    dfs_noname=[]

    for i in (input_file):
        sp=i.split("/")[-1]
        sp=sp.split("_")[0]

        dfs_noname.append(pd.read_csv(i, low_memory=False, sep="\t"))

    dfs = dict(zip(sp_list, dfs_noname))


    return (dfs)


################################################################################

def get_common_dict(dfs, sp_list):

    common_fam=[]
    common_df = pd.DataFrame()

    for i in dfs:
        fams=list(dfs[i]["FAM"])
        for fam in fams:
            common_fam.append(fam)

    common_set=[]

    for f in common_fam:
        if common_fam.count(f)/len(sp_list)==1:
            common_set.append(f)

    common_set=list(set(common_set))


    if len(common_set)==0:
        sys.exit("NO COMMON FAMILIES!")
        return()

    else:
        common_df["FAM"]=common_set

        for sp in sp_list:
            temp_df = dfs[sp].loc[dfs[sp]['FAM'].isin(common_set), ['FAM','DEGs_p','up_p']]
            temp_df.columns=['FAM','DEGs_p'+'_'+sp,'up_p'+'_'+sp]

            common_df = pd.merge(common_df, temp_df, on="FAM")



    return (common_df)


################################################################################

def main():

    parser = argparse.ArgumentParser(description='My nice tool.')
    parser.add_argument('--fam_tab', metavar='FAM_TAB', nargs='+', help='Families table')

    args = parser.parse_args()

    sp_list=get_species_list(args.fam_tab)

    dfs = get_fam_dfs(args.fam_tab, sp_list)
    
    common_df = get_common_dict(dfs, sp_list)

    filename="_".join(sp_list)+"_intersection.tsv"

    common_df.to_csv(filename, sep="\t", index = False)


if __name__ == "__main__":
  main()
