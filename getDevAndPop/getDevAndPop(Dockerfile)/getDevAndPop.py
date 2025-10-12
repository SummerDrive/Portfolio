import os
import time
import re
import tempfile
import pandas as pd
from flask import Flask, request
from google.cloud import storage
from playwright.sync_api import sync_playwright

app = Flask(__name__)
BUCKET_NAME = "getdevandpop"

htmlArray1 = [['.RaceOdds_HorseList.Tanfuku',"odds-1_1"], 
              ['.RaceOdds_HorseList.Umaren',"odds-4_1"], 
              ['.RaceOdds_HorseList.Umatan',"odds-6_1"], 
              ['.RaceOdds_HorseList.Ufuku',"odds-7_1"], 
              ['div.RaceOdds_HorseList.\\33 Tan.New3Tan',"odds-8_1"]]

htmlArray2 = ['.Umatan', '.Fuku3', '.Tan3']

def openWebsite(numAndUrl, pw):
    array = [numAndUrl[0]]
    browser = pw.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
    context = browser.new_context()
    page = context.new_page()
    page.goto(numAndUrl[1], wait_until="domcontentloaded")
    time.sleep(3)

    txt0 = page.locator(".RaceData02").inner_html()
    match0 = re.search(rf'<span>(.*?)頭</span>', txt0)
    array.append(match0.group(1) if match0 else "No Data")

    for row in htmlArray1:
        time.sleep(3)
        txt = page.locator(row[0]).inner_html()
        match1 = re.search(rf'<span\s+class="Odds\s+Odds_Ninki"\s+id="{re.escape(row[1])}">([\d.]+)</span>', txt)
        if match1:
            target = int(match1.group(1).replace('.', '')) * 10
        else:
            match2 = re.search(rf'<span\s+id="{re.escape(row[1])}">([\d.]+)</span>', txt)
            target = int(match2.group(1).replace('.', '')) * 10 if match2 else "No Data"
        array.append(target)

    page.get_by_role("link", name="結果・払戻").click()
    time.sleep(3)
    for cls in htmlArray2:
        time.sleep(3)
        txt2 = page.locator(cls).inner_html()
        match3 = re.search(r'<td\s+class="Payout"><span>([\d,]+)円</span></td>', txt2)
        array.append(int(match3.group(1).replace(',', '')) if match3 else "No Data")
        match4 = re.search(r'<td\s+class="Ninki">\s*<span>([\d,]+)人気</span>', txt2)
        array.append(int(match4.group(1).replace(',', '')) if match4 else "No Data")

    context.close()
    browser.close()
    return array

@app.route("/", methods=["POST","GET"])
def run_task():
    with sync_playwright() as pw:
        storage_client = storage.Client()
        tmp1 = tempfile.NamedTemporaryFile(delete=False)
        tmp2 = tempfile.NamedTemporaryFile(delete=False)
        storage_client.bucket(BUCKET_NAME).blob("SetCSV.csv").download_to_filename(tmp1.name)
        storage_client.bucket(BUCKET_NAME).blob("GetCSV.csv").download_to_filename(tmp2.name)

        df1 = pd.read_csv(tmp1.name)
        head_rows = df1.head(6)
        results = [openWebsite(row, pw) for _, row in head_rows.iterrows()]

        try:
            df2 = pd.read_csv(tmp2.name, header=None)
        except Exception:
            df2 = pd.DataFrame()

        df_results = pd.DataFrame(results)
        df2 = pd.concat([df2, df_results], ignore_index=True)
        df2.to_csv(tmp2.name, index=False, header=False)
        df1.iloc[6:].to_csv(tmp1.name, index=False)

        storage_client.bucket(BUCKET_NAME).blob("SetCSV.csv").upload_from_filename(tmp1.name)
        storage_client.bucket(BUCKET_NAME).blob("GetCSV.csv").upload_from_filename(tmp2.name)

    return "Task Completed", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)