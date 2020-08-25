データ収集に関する知識への一歩
---

> Folder *tradv* 
### Web Contentsより必要なデータを集めるパターンの練習

Tripadvisorより、日本基準の市町村location ID及びそのメイン画面のurlを収集

##### Python 3.8
- Thread + Semaphore活用
- decorator表現
- abstract class宣言 及び 継承

##### ライブラリ
- requests url先データGet
- pandasでファイル書き込み


> Folder *mashup*
### データを集め、可視化するパターン

下記の公的データを利用し、町丁別の人口変更を時系列で表現
- 立川市町丁別世帯数と人口（出所：立川市役所hp）
- 立川市町レベルの位置データ（出所：国土交通省 位置参照情報 ダウンロードサービス）

##### ライブラリ
- folium

##### 結果（screenshot）
- 立川市人口変動 2014～2019  
![立川市人口変動 2014～2019](https://github.com/yusunu/repo_py_web_crawling/blob/master/mashup/result.png)

