#!/usr/bin/env python3



import sys
import argparse
import os
from collections import defaultdict



def main():
    parser = argparse.ArgumentParser(description='My nice tool.')
    parser.add_argument('--conv', metavar='CONV', help='converter tab')
    parser.add_argument('--tab', metavar='TAB', help='table to be converted')


    args = parser.parse_args()

    con_dict = {}


    with open(args.conv) as con_file:
        for line in con_file:
            line=line.split("\t")

            con_dict[line[0]]=line[1].strip("\n")


    c =0

    with open(args.tab) as table_file:
        for line in table_file:
            line = line.split(",")


            if line[0] in con_dict.keys():

                print (str(con_dict[line[0]])+","+line[1].strip("\n"))

            else:
                c+=1


    # print ("NOT CONVERTED: ", c)



if __name__ == "__main__":
  main()
