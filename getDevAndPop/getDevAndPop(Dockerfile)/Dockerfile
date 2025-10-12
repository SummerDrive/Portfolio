FROM mcr.microsoft.com/playwright/python:v1.54.0-noble

# 作業ディレクトリ
WORKDIR /app

# 必要なPythonライブラリ
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Playwright のブラウザもインストール
RUN playwright install

# ソースをコピー
COPY . .

# Cloud Run ポート指定
ENV PORT 8080

# Flask 起動
# Chromium起動オプション追加
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
CMD ["python", "getDevAndPop.py"]