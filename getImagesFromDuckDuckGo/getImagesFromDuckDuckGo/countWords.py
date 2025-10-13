import os
import re
import pandas as pd
import boto3
from io import StringIO
import datetime

def lambda_handler(event, context):
    # S3の情報
    bucket_name = "csvforddg"     # ←バケット名を入れる
    imageURLs_key = "CSVforDDG/imageURLs.csv"
    wordCount_key = "CSVforDDG/wordCount.csv"

    s3 = boto3.client("s3")

    t_start = datetime.datetime.now()

    try:
        # --- CSVファイルの読み込み ---
        objURL = s3.get_object(Bucket=bucket_name, Key=imageURLs_key)
        dfURL = pd.read_csv(objURL["Body"], header=None, encoding="utf-8-sig", encoding_errors='backslashreplace')

        objCount = s3.get_object(Bucket=bucket_name, Key=wordCount_key)
        dfCount = pd.read_csv(objCount["Body"], header=None, encoding="utf-8-sig", encoding_errors='backslashreplace')
        dfCount.iloc[:, 1] = 0

        rowCount = dfURL.shape[0]
        for i in range(rowCount):
            sntnc = dfURL.iloc[i,0]
            wrds = re.findall(r"[A-Za-z]+", sntnc)

            for wrd in wrds:
                if wrd in dfCount.iloc[:, 0].values:
                    # 存在するなら2列目を+1
                    dfCount.loc[dfCount.iloc[:, 0] == wrd, 1] += 1
                else:
                    # 存在しないなら行を追加
                    dfCount.loc[len(dfCount)] = [wrd, 1]

        dfC_sorted = dfCount.sort_values(by = 1, ascending = False, kind = "mergesort").reset_index(drop = True)
  
        # --- dfCountを書き戻し ---
        bufferCount = StringIO()
        dfCount.to_csv(bufferCount, index=False, header=False)
        s3.put_object(Bucket=bucket_name, Key=wordCount_key, Body=bufferCount.getvalue())

        t_end = datetime.datetime.now()
        print("time : ", t_end -t_start)
            
        print("countKeyWords実行完了")
        return {"status": "done"}
    except Exception as e:
        t_end = datetime.datetime.now()
        print("time : ", t_end -t_start)

        print("Error:", e)
        return {"status": "error", "message": str(e)}

