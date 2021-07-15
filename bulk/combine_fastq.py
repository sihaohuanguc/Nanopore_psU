import os
import sys
working_path=sys.path[0]
in_folder=working_path+"/fastq_aligned"
out_folder=working_path+"/fastq_collect"

if not os.path.exists(out_folder):
    os.mkdir(out_folder)

for item in os.listdir(in_folder):
    sub_folder=in_folder+"/"+item
    if os.path.isdir(sub_folder):
        for sub_item in os.listdir(sub_folder):
            sub_sub_folder=sub_folder+"/"+sub_item
            if os.path.isdir(sub_sub_folder):
                out_sub_folder=out_folder+"/"+item
                if not os.path.exists(out_sub_folder):
                    os.mkdir(out_sub_folder)
                out_sub_sub_folder=out_sub_folder+"/"+sub_item
                if not os.path.exists(out_sub_sub_folder):
                    os.mkdir(out_sub_sub_folder)
                out_file=out_sub_sub_folder+"/collect.fastq"             
                with open(out_file,"w+") as out_f:
                    for sub_sub_item in os.listdir(sub_sub_folder):
                        in_file=sub_sub_folder+"/"+sub_sub_item
                        if os.path.isfile(in_file) and not sub_sub_item[0]=="." and sub_sub_item.split(".")[-1]=="fastq":
                            with open(in_file,"r") as f:
                                for line in f:
                                    out_f.write(line)
