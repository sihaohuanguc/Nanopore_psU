import sys
import os
import csv
import re
working_path=sys.path[0]
target_gene="GENE_NAME"
chrom="CHROM"
search_start=0
search_end=0

if chrom.split("_")[1]=="F":
    strand_folder="plus_strand"
elif chrom.split("_")[1]=="R":
    strand_folder="minus_strand"

in_folder=working_path
if os.path.isdir(in_folder) and "collect.sam" in os.listdir(in_folder) and "reference.fa" in os.listdir(in_folder):
    in_file=in_folder+"/collect.sam"
    ref_fa=in_folder+"/reference.fa"
    out_folder=working_path+"/"+target_gene
    out_file=out_folder+"/all_U_features.csv"
    out_temp_folder=working_path+"/temp_folder"
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)
    if not os.path.exists(out_temp_folder):
        os.mkdir(out_temp_folder)
    with open(out_file,"w+") as out_f:
        writer=csv.writer(out_f)
        with open(in_file,"r") as f:
            head_line=[]
            read_index=0
            for line in f:
                if line[0]=="@":
                    head_line.append(line)
                else:
                    temp_file_index=out_temp_folder+"/"+str(read_index)
                    out_sam=temp_file_index+".sam"
                    elements=line.strip("\n").split("\t")
                    if elements[1]=="0" and int(elements[3])>=search_start and int(elements[3])<=search_end:
                        with open(out_sam,"w+") as out_temp:
                            for item in head_line:
                                out_temp.write(item)
                            out_temp.write(line)
                        os.system("samtools mpileup -Q 0 -f "+ref_fa+" "+out_sam+" > "+temp_file_index+"_pile.txt")
                        in_pile_file=temp_file_index+"_pile.txt"
                        for line in open(in_pile_file,"r"):
                            site=line.strip("\n").split("\t")
                            if site[2]=="T":
                                out_line=[read_index]
                                out_line.extend(site[:3])
                                pattern=re.compile("\\^.")
                                alignment=re.sub(pattern,"",site[4])
                                qual=site[5]
                                if not alignment[0]==">":
                                    if alignment[0]=="." or alignment[0]==",":
                                        if len(alignment)>1 and alignment[1]=="+":
                                            num_pattern=re.compile("[0-9]+")
                                            new_str=re.search(num_pattern,alignment).group()
                                            out_line.extend([1,int(new_str),0,0,0,0,0,0,0,0,ord(qual)-33])
                                        elif len(alignment)>1 and alignment[1]=="-":
                                            num_pattern=re.compile("[0-9]+")
                                            new_str=re.search(num_pattern,alignment).group()
                                            out_line.extend([0,0,1,int(new_str),0,0,0,0,0,0,ord(qual)-33])
                                        elif len(alignment)>1 and alignment[1]=="$":
                                            out_line.extend([0,0,0,0,0,0,0,0,0,0,ord(qual)-33])                   
                                        else:
                                            out_line.extend([0,0,0,0,0,0,0,0,0,0,ord(qual)-33])      
                                    elif alignment[0]=="*":
                                        out_line.extend([0,0,0,0,1,0,0,0,0,0,ord(qual)-33])                                     
                                    elif alignment[0]=="A" or alignment[0]=="a":
                                        out_line.extend([0,0,0,0,0,1,1,0,0,0,ord(qual)-33])                                    
                                    elif alignment[0]=="C" or alignment[0]=="c":
                                        out_line.extend([0,0,0,0,0,1,0,1,0,0,ord(qual)-33])
                                    elif alignment[0]=="G" or alignment[0]=="g":
                                        out_line.extend([0,0,0,0,0,1,0,0,1,0,ord(qual)-33])
                                    elif alignment[0]=="T" or alignment[0]=="t":
                                        out_line.extend([0,0,0,0,0,1,0,0,0,1,ord(qual)-33])
                                    writer.writerow(out_line)
                    read_index+=1
    os.system("rm -r "+out_temp_folder)
