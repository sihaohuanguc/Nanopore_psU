import os
import sys
import numpy
import pandas as pd
import pickle
from sklearn.ensemble import ExtraTreesClassifier

def pred():
    working_path=os.getcwd()
    in_folder=working_path+"/alignment"
    in_file=in_folder+"/features.csv"
    out_prediction_file=in_folder+"/prediction.csv"
    
    print(sys.path[0])
    base_path=os.path.abspath(__file__)
    folder=os.path.dirname(base_path)
    python_version=sys.version[0]
    if python_version=="2":
        in_model=folder+"/data/model/model_3_0_p2.pkl"
    elif python_version=="3":
        in_model=folder+"/data/model/model_3_0.pkl"
    print(base_path)
    print(folder)
    print(in_model)
    print(sys.version)
    numpy.set_printoptions(suppress=True)
    pd.set_option("display.max_columns",None)

    with open(in_model,"rb") as f:
        ET1=pickle.load(f)
    print("OK")

    df=pd.read_csv(in_file,header=None,names=["transcript_ID","position","base_type","coverage","ins","ins_len","del","del_len","fuzzy","mis","misA","misC","misG","base_qual_mean","base_qual_STD","base_qual_count_0"])
    cols=["transcript_ID","position","base_type","coverage"]
    site_info=df[cols]
    df.drop(["transcript_ID","position","base_type","coverage"],axis=1,inplace=True)

    ET1_predict_proba=ET1.predict_proba(df)
    prob_unmodified=[]
    prob_modified=[]
    for i in range(len(ET1_predict_proba)):
        prob_unmodified.append(ET1_predict_proba[i][0])
        prob_modified.append(ET1_predict_proba[i][1])
    site_info["prob_unmodified"]=prob_unmodified
    site_info["prob_modified"]=prob_modified

    site_info.to_csv(out_prediction_file,index=False,header=None)



