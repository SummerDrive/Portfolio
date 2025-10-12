import os
import requests
import pandas as pd
from flask import Flask, request
import time
from pathlib import PurePosixPath

# このスクリプトファイルが存在するディレクトリの絶対パスを取得
script_dir = os.path.dirname(os.path.abspath(__file__))
# スクリプトと同じフォルダにあるファイル名を結合
imageURLs_path = os.path.join(script_dir, 'imageURLs.csv')
images_dir = os.path.join(script_dir, 'downloadedPics')

app = Flask(__name__)
#BUCKET_NAME = "getimagesfromduckduckgo"

@app.route("/", methods=["POST","GET"])
def run_task():
    #storage_client = storage.Client()
    #tmp1 = tempfile.NamedTemporaryFile(delete=False)
    #tmp2 = tempfile.NamedTemporaryFile(delete=False)
    #storage_client.bucket(BUCKET_NAME).blob("keywordURLs.csv").download_to_filename(tmp1.name)
    #storage_client.bucket(BUCKET_NAME).blob("imageURLs.csv").download_to_filename(tmp2.name)

    dfr = pd.read_csv(imageURLs_path, header=None, encoding="utf-8-sig", encoding_errors='backslashreplace')
    # 3列目が "pending" の最初の行の index を取得
    pending_index = dfr.index[dfr[2] == "Pending"].min()
    time.sleep(3)

    if pd.notna(pending_index):  # pending が存在する場合
        first_pending_URL = dfr.at[pending_index, 1]
        print(first_pending_URL)
    else:
        print("No Pending found")

    try:
        response = requests.get(first_pending_URL)
        imgName = PurePosixPath(first_pending_URL).name
        images_path = os.path.join(images_dir, imgName)
        print(images_path)
        time.sleep(3)
        with open(images_path, 'wb') as f:
            f.write(response.content)

        # 取得済み行を "completed" に更新
        dfr.at[pending_index, 2] = "Completed"
        dfr.to_csv(imageURLs_path, index=False, header=False)
    except Exception:
        print("failed")

    #storage_client.bucket(BUCKET_NAME).blob("SetCSV.csv").upload_from_filename(tmp1.name)
    #storage_client.bucket(BUCKET_NAME).blob("GetCSV.csv").upload_from_filename(tmp2.name)

    return "Task Completed", 200
if __name__ == "__main__":
    print("getImagesFromURL")

    # 関数を直接呼んでテスト
    run_task()

    # サーバーも起動するならそのまま
    #port = int(os.environ.get("PORT", 8080))
    #app.run(host="0.0.0.0", port=port)
