## 目的
Stable Diffusion用学習画像取得

## 使用の流れ

(A)検索ワードを用意してkeywords.csvに蓄積

--

(B)getURLformDuckDuckGo.pyを必要に応じて手動実行

(検索ワードからduckduckgo APIで画像タグ、画像URLを一括取得

+重複しているものを削除+imageURLs.csvに蓄積)

--

(C)AWS Lambdaで10分ごとにgetImagesFromURL.pyを実行(URLから画像を取得)

--

(D)画像タグ内頻出単語をcountWords.pyで算出してwordCount.csvに格納

keywords.csvの検索ワードに追加

--

(B)の進行具合に応じて(D)を実行+(C)の進行具合に応じて(B)を実行

## 使用ライブラリ
duckduckgo API(DDGS), pandas, requests, PurePosixPath(pathlib)
