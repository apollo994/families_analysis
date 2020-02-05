#!/usr/bin/env python3



import sys
import argparse
import os
from collections import defaultdict


##############################################################################


def get_sp_dictionary(dict_file, species):

    fam_id_dict={}
    gene_fam_dict={}

    with open (dict_file, "r") as fams:
        for line in fams:
            line = line.split("\t")

            fam = line[0]
            sp = line[1]
            gene = line[2].strip("\n")

            if sp == species:

                if fam not in fam_id_dict.keys():
                    fam_id_dict[fam]=[gene]
                else:
                    fam_id_dict[fam].append(gene)

                gene_fam_dict[gene]=fam


    return fam_id_dict, gene_fam_dict

############################################################################



def get_signle_gene_list(list_path, gene_fam_dict):

    gene_to_fam = {}
    gene_list = []
    fam_list = []

    with open(list_path,"r") as gene_fc:
        # print (str(list_path)+"/"+f)
        for line in gene_fc:
            line=line.split(",")

            gene = line[0]
            FC= line[1].strip("\n")
            if float(FC)>0:
                up_dw="up"
            else:
                up_dw="dw"

            excluded = 0

            if gene in gene_fam_dict.keys():
                fam = gene_fam_dict[gene]

                gene_to_fam[gene]= [FC, up_dw, fam]

                # gene_to_fam.append([gene, FC, up_dw, fam])
                gene_list.append(gene)
                fam_list.append(fam)

            if gene not in gene_fam_dict.keys():
                excluded +=1
    # fam_list=list(set(fam_list))

    print ("Not found in Plaza: ", excluded)

    return gene_to_fam, gene_list, fam_list


##############################################################################

def generate_gene_table(gene_table, sp):
    with open (sp+"_gene_table.tsv", "w") as out:
        out.write("ID\tFC\tup_dw\tFAM\n")

        for i in gene_table:
            line="\t".join(gene_table[i])
            line=i+"\t"+line+"\n"
            out.write(line)




################################################################################

def generate_fam_table(fam_id_dict, sp_dict, gene_list, fam_list, sp):

    uniq_fam=list(set(fam_list))

    with open (sp+"_fam_table.tsv", "w") as out:
        out.write("FAM\tsize\tDEGs\tDEGs_p\tup\tdw\tup_p\tup\tdw\n")

        for fam in uniq_fam:

            up=[]
            dw=[]


            for i in sp_dict:
                if sp_dict[i][2]==fam:
                    if float(sp_dict[i][0])>1:
                        up.append(i)
                    else:
                        dw.append(i)

            fam = fam
            size = len(fam_id_dict[fam])
            degs = fam_list.count(fam)
            degs_p = round(degs/size,2)
            up_n=len(up)
            dw_n=len(dw)
            if up_n == 0:
                up_p=0
                up_list="NA"
                dw_list=",".join(dw)

            if dw_n == 0:
                up_p=1
                up_list=",".join(up)
                dw_list="NA"

            if up_n!=0 and dw_n!=0:
                up_p=round(up_n/(up_n+dw_n),2)
                up_list=",".join(up)
                dw_list=",".join(dw)

            out.write(fam+"\t"+str(size)+"\t"+str(degs)+"\t"+str(degs_p)+"\t"
                        +str(up_n)+"\t"+str(dw_n)+"\t"+str(up_p)+"\t"
                        +up_list+"\t"+dw_list+"\n")


################################################################################




def main():
    parser = argparse.ArgumentParser(description='My nice tool.')
    parser.add_argument('--plaza', metavar='PLAZA', help='plaza tab')
    parser.add_argument('--gl', metavar='GENE_LISTS', help='path to gene lists')


    args = parser.parse_args()


#  species list     #############################################################

    sp=args.gl.split("/")[-1]
    sp=sp.split("_")[0]

    print ("working on:", args.gl)
    print ("species: ",sp)

    fam_id_dict,gene_fam_dict = get_sp_dictionary(args.plaza, sp)

    sp_dict, gene_list, fam_list = get_signle_gene_list(args.gl, gene_fam_dict)

    generate_gene_table(sp_dict, sp)

    generate_fam_table(fam_id_dict, sp_dict, gene_list, fam_list, sp)



if __name__ == "__main__":
  main()
