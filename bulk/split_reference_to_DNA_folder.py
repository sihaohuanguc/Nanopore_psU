import os
import sys
working_path=sys.path[0]
in_file=working_path+"/reference.fa"
in_folder=working_path+"/"+"fastq_collect"

def rev_comp(ref):
    rev_comp=[]
    for item in ref:
        if item=="A":
            rev_comp.append("T")
        elif item=="C":
            rev_comp.append("G")
        elif item=="G":
            rev_comp.append("C")
        elif item=="T":
            rev_comp.append("A")
        elif item=="N":
            rev_comp.append("N")
        else:
            print(item+": Wrong input!")
    rev_comp.reverse()
    return "".join(rev_comp)

all_gene_name=[]
for item in os.listdir(in_folder):
    if not item[0]==".":
        all_gene_name.append(item)

with open(in_file,"r") as f:
    all_ref=[]
    one_strand=[]
    all_text=[]
    for line in f:
        if line[0]==">":
            all_text="".join(all_text)
            one_strand.append(all_text)
            all_ref.append(one_strand)
            one_strand=[]
            one_strand.append(line.strip("\n").strip(">").split(" ")[0])
            all_text=[]
        else:
            all_text.append(line.strip("\n"))
    all_text="".join(all_text)
    one_strand.append(all_text)
    all_ref.append(one_strand)
    all_ref=all_ref[1:]
    for i in range(len(all_ref)):
        if all_ref[i][0] in all_gene_name:
            in_sub_folder=in_folder+"/"+all_ref[i][0]
            if "plus_strand" in os.listdir(in_sub_folder):
                out_file=in_sub_folder+"/plus_strand/reference.fa"
                with open(out_file,"w+") as out_f:
                    out_f.write(">"+all_ref[i][0]+"_F\n")
                    out_f.write(all_ref[i][1])
            if "minus_strand" in os.listdir(in_sub_folder):
                out_file=in_sub_folder+"/minus_strand/reference.fa"
                with open(out_file,"w+") as out_f:
                    out_f.write(">"+all_ref[i][0]+"_R\n")
                    out_f.write(rev_comp(all_ref[i][1]))
                    
