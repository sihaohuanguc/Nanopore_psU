import os
import sys
working_path=sys.path[0]
in_file=working_path+"/all_pass_fastq.fastq"
temp_folder=working_path+"/temp"
out_folder=working_path+"/fastq_aligned"

if not os.path.exists(temp_folder):
    os.mkdir(temp_folder)
if not os.path.exists(out_folder):
    os.mkdir(out_folder)

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

def rev_score(str1):
    list1=list(str1)
    list1.reverse()
    return "".join(list1)

ref_fa=working_path+"/GRCh38.p13.genome.fa"

count_file=0
sam_file=temp_folder+"/all_pass_fastq.sam"
os.system("minimap2 -ax splice -uf -k14 "+ref_fa+" "+in_file+" > "+sam_file)

with open(sam_file,"r") as in_sam:
    for line in in_sam:
        if not line[0]=="@" and len(line)>1:
            elements=line.split("\t")
            aligned_gene=elements[2]
            aligned_strand=elements[1]
            if not aligned_gene=="*" and (aligned_strand=="0" or aligned_strand=="16"):
                count_file+=1
                out_sub_folder=out_folder+"/"+aligned_gene
                if not os.path.exists(out_sub_folder):
                    os.mkdir(out_sub_folder)
                if aligned_strand=="0":
                    out_sub_sub_folder=out_sub_folder+"/plus_strand"
                    if not os.path.exists(out_sub_sub_folder):
                        os.mkdir(out_sub_sub_folder)
                    out_file=out_sub_sub_folder+"/"+str(count_file)+".fastq"
                    out_line=["@"+elements[0],elements[9],"+",elements[10]]
                elif aligned_strand=="16":
                    out_sub_sub_folder=out_sub_folder+"/minus_strand"
                    if not os.path.exists(out_sub_sub_folder):
                        os.mkdir(out_sub_sub_folder)
                    out_file=out_sub_sub_folder+"/"+str(count_file)+".fastq"
                    out_line=["@"+elements[0],rev_comp(elements[9]),"+",rev_score(elements[10])]
                with open(out_file,"w+") as out_f:
                    for k in out_line:
                        out_f.write(k+"\n")
                                    
os.system("rm -r "+temp_folder)