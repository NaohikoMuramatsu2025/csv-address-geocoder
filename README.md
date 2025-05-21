# csv_address_geocoder

## 概要
本ツールは、CSVファイルに含まれる日本語住所をもとにジオコーディングを実行し、緯度・経度を取得したうえで、CSVおよびGeoJSON形式で出力するPythonスクリプトです。

## 特徴
- **入力**：住所列を含むCSVファイル（例：所在地）
- **出力**：
  - 緯度・経度を追加したCSV（UTF-8 BOM形式）
  - GeoJSONファイル（地図アプリで活用可能）
- **使用API**：[http://www.geocoding.jp](http://www.geocoding.jp)（無料サービス）
- **対応環境**：Windows環境対応（バッチファイル付きで簡単起動）

---

## フォルダ構成
```plaintext
csv_address_geocoder/
├── Input/ # 入力CSVファイルを配置
├── Output/ # 出力CSV・GeoJSONが保存されます
├── Python_Src/ # Pythonスクリプトおよび設定ファイル
│ ├── csv_address_geocoder.py
│ └── config.ini
└── start_csv_address_geocoder.bat # 実行用バッチファイル（Windows）
```
---

## 使用方法

### 1. 入力CSVの準備
`Input/02kenchiku.csv` のように、住所情報を含むCSVファイルを `Input` フォルダに配置してください。住所列の列名（例：`所在地`）は、後述の設定ファイルで指定します。

### 2. 設定ファイル（config.ini）の確認・編集
`Python_Src/config.ini` を以下の形式で編集してください：

```ini
[Paths]
input_csv = ../Input/02kenchiku.csv
output_csv = ../Output/02kenchiku_with_geo.csv
output_geojson = ../Output/02kenchiku.geojson
address_column = 所在地

