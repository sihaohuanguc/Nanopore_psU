import os
import sys
working_path=sys.path[0]
in_folder=working_path+"/your_fastq_folder"
out_file=working_path+"/all_pass_fastq.fastq"

with open(out_file,"w+") as out_f:
    for item in os.listdir(in_folder):
        in_file=in_folder+"/"+item
        if os.path.isfile(in_file) and not item[0]=="." and item.split(".")[-1]=="fastq":
            with open(in_file,"r") as f:
                switch=0
                for line in f:
                    if switch==0 and line[0]=="@":
                        switch=1
                    elif switch==1 and line[0] in ["A","C","G","U"]:
                        switch=0
                        line=line.replace("U","T")
                    out_f.write(line)