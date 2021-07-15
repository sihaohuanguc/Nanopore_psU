import os
import sys
import csv
working_path=sys.path[0]
super_folder=working_path+"/fastq_collect"
out_file=working_path+"/all_features.csv"

with open(out_file,"w+") as output:
    writer=csv.writer(output)
    for super_item in os.listdir(super_folder):
        in_folder=super_folder+"/"+super_item
        if os.path.isdir(in_folder) and not super_item[0]==".":
            for item in os.listdir(in_folder):
                sub_folder=in_folder+"/"+item
                if os.path.isdir(sub_folder) and "features.csv" in os.listdir(sub_folder):
                    in_file=sub_folder+"/features.csv"
                    with open(in_file,"r") as inf:
                        reader=csv.reader(inf)
                        for line in reader:        
                            writer.writerow(line)

