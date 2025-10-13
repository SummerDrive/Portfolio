## 目的
  某webサイトの過去3~4年分の某データを取得してGoogleスプレッドシート用にCSV化

## 使用の流れ
  某webサイトのデータページURLをページIDごとに作成しCSV化→SetCSV.csv
  
  CSV作成はスプシ+GoogleAppScript使用、4年分で14000行程度

  ↓
  
  Google Cloud RunでgetDevAndPop.pyを30分ごとに実行
  
  実行一回につきSetCSV.csvの上から6行分を順次取得
  
  ↓

  取得データはgetCSV.csvに蓄積→スプシで解析

##使用ライブラリ
  playwright,pandas,flask,google-cloud-storage

##（使用結果）
  2025/08中旬から2025/10初旬まで定期実行
  
  9月の１か月間で料金は￥2000程度
  
