import os
import time
import re
import tempfile
from typing import Type
import pandas as pd
from ddgs import DDGS
import boto3
from io import StringIO

def getURLfromAPI(kws):
    with DDGS() as dudugos:
        results = list(dudugos.images(
            query = kws,       # ← ここは query
            region = 'jp-jp',
            safesearch = 'off',
            timelimit = None,
            max_results = 100
        ))

        data = [
            [r.get("title",""), r["image"], r.get("PorC","Pending")]  # 1行 = [タイトル, 画像URL]
            for r in results
            if r["image"].lower().endswith((".jpg", ".jpeg", ".png"))
            and r.get("width", 0) >= 512
            and r.get("height", 0) >= 512
        ]

    return data

def lambda_handler(event, context):
    # S3の情報
    bucket_name = "csvforddg"     # ←バケット名を入れる
    imageURLs_key = "CSVforDDG/imageURLs.csv"
    keywords_key = "CSVforDDG/keywords.csv"  # ←フォルダ＋ファイル名

    s3 = boto3.client("s3")

    try:
        # --- CSVファイルの読み込み ---
        obj1 = s3.get_object(Bucket=bucket_name, Key=keywords_key)
        df1 = pd.read_csv(obj1["Body"])

        obj2 = s3.get_object(Bucket=bucket_name, Key=imageURLs_key)
        df2 = pd.read_csv(obj2["Body"], header=None)

        # 3列目(PorC)が "pending" の最初の行の index を取得
        pending_index = df1.index[df1["PorC"] == "Pending"].min()

        if pd.notna(pending_index):  # pending が存在する場合
            first_pending_keyword = df1.at[pending_index, "keyword"]
            print(first_pending_keyword)
            results = getURLfromAPI(first_pending_keyword)
        else:
            print("No Pending found")
        
        # PorC を "completed" に更新
        df1.at[pending_index, "PorC"] = "Completed"

        print(results)
        print(len(results))
        df_results = pd.DataFrame(results)
        df2 = pd.concat([df2, df_results], ignore_index=True)

        # 重複削除（下側を削除して最初の1件を残す）
        df_unique = df2.drop_duplicates(subset=[0], keep="first")

        print("\n削除後")
        print(df_unique)

        # --- df1を書き戻し ---
        buffer1 = StringIO()
        df1.to_csv(buffer1, index=False)
        s3.put_object(Bucket=bucket_name, Key=keywords_key, Body=buffer1.getvalue())

        # --- df2を書き戻し ---
        buffer2 = StringIO()
        df_unique.to_csv(buffer2, index=False, header=False)  # headerなしで書き戻す場合
        s3.put_object(Bucket=bucket_name, Key=imageURLs_key, Body=buffer2.getvalue())
    except Exception as e:
        print("Error:", e)
        return {"status": "error", "message": str(e)}
    
    print("getURL実行完了")
    return {"status": "done"}
