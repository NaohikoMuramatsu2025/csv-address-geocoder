import os
import requests
import xml.etree.ElementTree as ET
import pandas as pd
import json
import configparser
import time

class AddressConverter:
    API_URL = "http://www.geocoding.jp/api/"

    def convert_address_to_lat_long(self, w_addr):
        """指定した住所から緯度と経度を取得"""
        url = f"{self.API_URL}?q={w_addr.strip()}"
        geo_code_result = None

        try:
            response = requests.get(url)
            if response.status_code == 200:
                xml_str = response.text
                xml_doc = ET.fromstring(xml_str)
                coordinate_element = xml_doc.find("coordinate")
                if coordinate_element is not None:
                    lat = coordinate_element.find("lat").text
                    lng = coordinate_element.find("lng").text
                    if lat and lng:
                        geo_code_result = (float(lat), float(lng))
        except Exception as ex:
            print(f"An error occurred: {ex}")

        return geo_code_result

def load_config(config_file):
    """複数のエンコーディングでINIファイルを読み込む"""
    config = configparser.ConfigParser()
    encodings_to_try = ['utf-8', 'shift_jis', 'cp932']
    for enc in encodings_to_try:
        try:
            print(f"Trying to read INI as {enc}...")
            config.read(config_file, encoding=enc)
            return config
        except UnicodeDecodeError:
            print(f"→ {enc} でのINI読み込みに失敗しました。")
        except Exception as e:
            print(f"→ {enc} での読み込み中にエラー: {e}")
    raise Exception("INIファイルの読み込みに失敗しました。")

def read_csv_fallback(filepath):
    """複数のエンコーディングを試してCSVファイルを読み込む"""
    encodings_to_try = ['utf-8-sig', 'utf-8', 'shift_jis', 'cp932']
    for enc in encodings_to_try:
        try:
            print(f"Trying to read CSV as {enc}...")
            return pd.read_csv(filepath, encoding=enc)
        except UnicodeDecodeError:
            print(f"→ {enc} での読み込みに失敗しました。")
        except Exception as e:
            print(f"→ {enc} での読み込み中にエラー: {e}")
    raise Exception("CSVファイルの読み込みに失敗しました。サポートされている文字コードではありません。")

def process_csv(input_csv, output_csv, output_geojson, address_column, converter):
    """CSVの処理とGeoJSONの出力"""
    input_csv = os.path.abspath(input_csv)
    output_csv = os.path.abspath(output_csv)
    output_geojson = os.path.abspath(output_geojson)

    print(f"Reading CSV file from: {input_csv}")
    df = read_csv_fallback(input_csv)

    geometries = []
    for index, row in df.iterrows():
        address = row[address_column]
        print(f"[{index}] 住所: {address}")
        result = converter.convert_address_to_lat_long(address)
        print(f" → 結果: {result}")
        time.sleep(3)  # 3秒待機

        if result:
            lat, lng = result
            wkt = f"POINT({lng} {lat})"
        else:
            wkt = None
        geometries.append(wkt)

    df['geometry'] = geometries
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"ジオコーディング済みのCSVが作成されました: {output_csv}")

    features = []
    for _, row in df.iterrows():
        if row['geometry']:
            lng, lat = map(float, row['geometry'].replace("POINT(", "").replace(")", "").split())
            point = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lng, lat]
                },
                "properties": row.drop('geometry').to_dict()
            }
            features.append(point)

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(output_geojson, 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, ensure_ascii=False, indent=4)
    print(f"GeoJSONファイルが作成されました: {output_geojson}")

if __name__ == "__main__":
    config = load_config("config.ini")
    input_csv = config['Paths']['input_csv']
    output_csv = config['Paths']['output_csv']
    output_geojson = config['Paths']['output_geojson']
    address_column = config['Paths'].get('address_column', '場所')  # デフォルトは「場所」

    converter = AddressConverter()
    process_csv(input_csv, output_csv, output_geojson, address_column, converter)
