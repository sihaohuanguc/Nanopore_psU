import os
import sys
working_path=sys.path[0]
super_folder=working_path+"/fastq_collect"

for super_item in os.listdir(super_folder):
    in_folder=super_folder+"/"+super_item
    if os.path.isdir(in_folder) and not super_item[0]==".":
        for item in os.listdir(in_folder):
            sub_folder=in_folder+"/"+item
            if os.path.isdir(sub_folder) and "collect.fastq" in os.listdir(sub_folder) and "reference.fa" in os.listdir(sub_folder):
                in_file=sub_folder+"/collect"
                ref_fa=sub_folder+"/reference.fa"
                os.system("minimap2 -ax splice -uf -k14 "+ref_fa+" "+in_file+".fastq > "+in_file+".sam")
                os.system("samtools view -bS "+in_file+".sam > "+in_file+".bam")
                os.system("samtools sort "+in_file+".bam -o "+in_file+".sorted.bam")
                os.system("samtools mpileup -Q 0 -f "+ref_fa+" "+in_file+".sorted.bam > "+in_file+"_pile.txt")