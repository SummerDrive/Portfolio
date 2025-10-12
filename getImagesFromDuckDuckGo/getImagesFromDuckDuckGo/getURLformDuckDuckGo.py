import os
import time
import re
import tempfile
from typing import Type
import pandas as pd
from ddgs import DDGS

# このスクリプトファイルが存在するディレクトリの絶対パスを取得
script_dir = os.path.dirname(os.path.abspath(__file__))
# スクリプトと同じフォルダにあるファイル名を結合
keywords_path = os.path.join(script_dir, 'keywords.csv')
imageURLs_path = os.path.join(script_dir, 'imageURLs.csv')

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

def run_task():
    df1 = pd.read_csv(keywords_path)
    # 3列目(PorC)が "pending" の最初の行の index を取得
    pending_index = df1.index[df1["PorC"] == "Pending"].min()
    time.sleep(3)

    if pd.notna(pending_index):  # pending が存在する場合
        first_pending_keyword = df1.at[pending_index, "keyword"]
        print(first_pending_keyword)
        results = getURLfromAPI(first_pending_keyword)
    else:
        print("No Pending found")

    try:
        df2 = pd.read_csv(imageURLs_path, header=None)
    except Exception:
        df2 = pd.DataFrame()

    print(results)
    print(len(results))
    df_results = pd.DataFrame(results)
    df2 = pd.concat([df2, df_results], ignore_index=True)

    # 重複削除（下側を削除して最初の1件を残す）
    df_unique = df2.drop_duplicates(subset=[0], keep="first")

    print("\n削除後")
    print(df_unique)

    df_unique.to_csv(imageURLs_path, index=False, header=False)

    # PorC を "completed" に更新
    df1.at[pending_index, "PorC"] = "Completed"
    df1.to_csv(keywords_path, index=False)


if __name__ == "__main__":
    print("getURLfromDuckDuckGo")

    run_task()