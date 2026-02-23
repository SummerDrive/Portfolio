## 目的
AWS EC2,S3,lambda(Node.js),GoogleMapAPIを使用したwebサイト立ち上げ練習<br>
思いつくまま興味のある機能を増設中

EC2インスタンス上にWebページを公開

index1 - Map表示 GoogleMapAPI

index2 - S3内のCSVから各レース情報を取得して表示<br>
> 各レースの反映ボタンで API gateway > lambda(Node.js) > playwright > 某webサイトから配当情報を取得<br>
> ページに反映

[https://summerdrivewebmaptest.s3.ap-northeast-1.amazonaws.com/index1.html](https://summerdrivewebmaptest.s3.ap-northeast-1.amazonaws.com/index1.html)

※リンクはCtrl+クリック（MacはCmd+クリック）で別タブで開けます。

### 更新履歴
2026/2/14 公開

2/16 GoogleMapAPIにhttpリファラ制限を設定

2/23 某webサイトからの配当情報取得ページ増設

### 今後の実装

