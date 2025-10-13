import os
import requests
import pandas as pd
import time
from pathlib import PurePosixPath
import boto3
from io import StringIO

def lambda_handler(event, context):
    # S3の情報
    bucket_name = "csvforddg"     # ←バケット名を入れる
    imageURLs_key = "CSVforDDG/imageURLs.csv"
    folder_path = "CSVforDDG/getIMG/"

    s3 = boto3.client("s3")

    try:
        # --- CSVファイルの読み込み ---
        objURL = s3.get_object(Bucket=bucket_name, Key=imageURLs_key)
        dfURL = pd.read_csv(objURL["Body"], header=None, encoding="utf-8-sig", encoding_errors='backslashreplace')

        # 3列目が "pending" の最初の行の index を取得
        pending_index = dfURL.index[dfURL[2] == "Pending"].min()
        print(str(pending_index) + "  /  " + str(dfURL.shape[0]))

        if pd.isna(pending_index):  # Pendingが存在しない場合
            print("No Pending found")
            return {"status": "done", "message": "No Pending found"}

        first_pending_URL = dfURL.at[pending_index, 1]
        print("Target URL:", first_pending_URL)

        try:
            # --- 画像取得 ---
            response = requests.get(first_pending_URL, timeout=10)
            response.raise_for_status()  # ステータスコード4xx/5xxで例外発生

            # --- S3に画像を保存 ---
            imgName = PurePosixPath(first_pending_URL).name
            s3_key = os.path.join(folder_path, imgName)

            s3.put_object(
                Bucket=bucket_name,
                Key=s3_key,
                Body=response.content,
                ContentType=response.headers.get('Content-Type', 'application/octet-stream')
            )

            print(f"Uploaded to S3: s3://{bucket_name}/{s3_key}")

            # 状態を "Completed" に変更
            dfURL.at[pending_index, 2] = "Completed"

        except Exception as e:  # ダウンロードに失敗した場合
            print("Image download failed:", e)
            # 状態を "ERROR" に変更
            dfURL.at[pending_index, 2] = "ERROR"
    
        # --- df1を書き戻し ---
        bufferURL = StringIO()
        dfURL.to_csv(bufferURL, index=False, header=False)
        s3.put_object(Bucket=bucket_name, Key=imageURLs_key, Body=bufferURL.getvalue())
    except Exception as e:
        print("Error:", e)
        return {"status": "error", "message": str(e)}
    
    print("getIMG実行完了")
    return {"status": "done"}
