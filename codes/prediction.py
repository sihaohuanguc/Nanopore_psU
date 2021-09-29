import sys
import numpy
import pandas as pd
import pickle
from sklearn.ensemble import ExtraTreesClassifier
working_path=sys.path[0]
in_folder=working_path+"/alignment"
in_file=in_folder+"/features.csv"
in_model=working_path+"/model_3_0.pkl"
out_prediction_file=in_folder+"/prediction.csv"

numpy.set_printoptions(suppress=True)
pd.set_option("display.max_columns",None)

df=pd.read_csv(in_file,header=None,names=["transcript_ID","position","base_type","coverage","ins","ins_len","del","del_len","fuzzy","mis","misA","misC","misG","base_qual_mean","base_qual_STD","base_qual_count_0"])
cols=["transcript_ID","position","base_type","coverage"]
site_info=df[cols]
df.drop(["transcript_ID","position","base_type","coverage"],axis=1,inplace=True)

with open(in_model,"rb") as f:
    ET1=pickle.load(f)

ET1_predict_proba=ET1.predict_proba(df)
prob_unmodified=[]
prob_modified=[]
for i in range(len(ET1_predict_proba)):
    prob_unmodified.append(ET1_predict_proba[i][0])
    prob_modified.append(ET1_predict_proba[i][1])
site_info["prob_unmodified"]=prob_unmodified
site_info["prob_modified"]=prob_modified

site_info.to_csv(out_prediction_file,index=False,header=None)



