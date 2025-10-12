from flask import Flask, request
#from google.cloud import storage
import pandas as pd
import os

app = Flask(__name__)
#BUCKET_NAME = "getimagesfromduckduckgo"

# このスクリプトファイルが存在するディレクトリの絶対パスを取得
script_dir = os.path.dirname(os.path.abspath(__file__))
# スクリプトと同じフォルダにあるファイル名を結合
imageURLs_path = os.path.join(script_dir, 'imageURLs.csv')

@app.route("/", methods=["POST","GET"])
def run_taskDupl():
    #storage_client = storage.Client()
    #tmp = tempfile.NamedTemporaryFile(delete=False)
    #storage_client.bucket(BUCKET_NAME).blob("imageURLs.csv").download_to_filename(tmp.name)

    df = pd.read_csv(imageURLs_path, header=None)

    print("削除前")
    print(df)

    # 重複削除（下側を削除して最初の1件を残す）
    df_unique = df.drop_duplicates(subset=[0], keep="first")

    print("\n削除後")
    print(df_unique)

    df_unique.to_csv(imageURLs_path, index=False, header=False)

if __name__ == "__main__":
    print("removeSameURL")
    # 関数を直接呼んでテスト
    run_taskDupl()

    # サーバーも起動するならそのまま
    #port = int(os.environ.get("PORT", 8080))
    #app.run(host="0.0.0.0", port=port)