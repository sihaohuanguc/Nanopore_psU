import sys
import csv
working_path=sys.path[0]
in_file=working_path+"/all_features.csv"
out_file=working_path+"/all_U_features.csv"

with open(out_file,"w+") as out_f:
    writer=csv.writer(out_f)
    with open(in_file,"r") as f:
        reader=csv.reader(f)
        for line in reader:
            if line[2]=="T" and int(line[3])>20:
                writer.writerow(line)

        