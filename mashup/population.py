import os
import pandas as pd
import folium
from folium import plugins


def input_path_join(path: str):
    # path の 先指定の後、filenameとjoin
    return lambda filename: os.path.join(path, filename)


def norm(x):
    # Normalize
    return (x - x.min()) / (x.max() - x.min())


path_join = input_path_join('mashup/input')

# Load 立川市町丁別世帯数と人口（CSV：20KB）
# https://www.city.tachikawa.lg.jp/somu/opendate/koukai/nennpou/jinnkou/zinkou.html
# 最初2行はメーダ情報っぽいのでskip

population_df = pd.read_csv(path_join('population.csv'), encoding="shift-JIS", header=2)
population_df = population_df.drop([0])

# 無名Columnsへ名前付与(変更) そもそも町名
population_df.rename(columns={'Unnamed: 0': 'key'}, inplace=True)
population_df.reset_index(inplace=True, drop=True)

# Load 立川市町レベルの位置データ
# 国土交通省 位置参照情報 ダウンロードサービス
geo_df = pd.read_csv(path_join('prefecturalCapital.csv'), encoding="shift-JIS")

geo_df.rename(
    columns={
        '大字町丁目名': 'key',
        '緯度': 'latitude',
        '経度': 'longitude'
    }, inplace=True)


# Merge 人口情報←位置情報(lat,lon)
pop_geo_info = pd.merge(population_df, geo_df[['key', 'latitude', 'longitude']], on='key', how='left')

# 「緯度」の欠損行を除外
pop_geo_info = pop_geo_info.dropna(subset=['latitude'])


# 2014年～2019年人口を　time flow
time_series = range(2014, 2019 + 1)
title = r'%s年人口（人）'
for year in time_series:
    col_pop = title % year
    pop_geo_info[col_pop] = pop_geo_info[col_pop].str.replace(',', '').astype(int)
    # 0.0 ～ 1.0 分布
    pop_geo_info[col_pop + '_nm'] = norm(pop_geo_info[col_pop])


# 地図描画

# 基本地図　立川市中心
japan_map = folium.Map(
    location=[35.7111, 139.409965],
    title='立川市人口（過去6年間)',
    tiles='cartodbpositron',
    zoom_start=13.4)

# メインデータ投入
heat_data = [[[row['latitude'],
               row['longitude'],
               row[(title % year)+'_nm']] for _, row in pop_geo_info.iterrows()] for year in time_series]

plugins.HeatMapWithTime(
    heat_data,
    index=[title % year for year in time_series],
    auto_play=True,
    radius=30,
    gradient={0.3: 'blue', 0.5: 'lime', 0.7: 'orange', 0.9: '#FC3800', 1: 'red'}
).add_to(japan_map)

# 町にマーカー
for i, row in pop_geo_info.iterrows():
    last_year = str(time_series[-1])
    tooltip = row['key'] + '<br> ' + last_year + '年現在：%s人' % (str(row[title % last_year]))

    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        popup=tooltip,
        color='#087FBF',
        fill_color='#087FBF',
        fill=True,
        fill_opacity=0.7,
        radius=5,
        weight=0
    ).add_to(japan_map)

japan_map.save(path_join('population_2014_2019_tachikawa.html'))
