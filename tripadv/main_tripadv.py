
import os
import re
from tripadv.retreivable import Retrievable, trigger_retrievable
from tripadv.utilpack import to_excel

# python練習
# Web clawling(※)
# ※著作権に注意
# 　robot.txtのDisallowもしくはサイトの規約を確認すること


class Restaurant_tripa(Retrievable):
    """
    Tripadvisor Restaurant 取得用
    """
    columns = ['location_id', 'location', 'url']

    def __init__(self, base_url):
        super().__init__(base_url=base_url)

    def _parsing(self, html_content: str) -> list:
        # 取得対象のデータが簡単だったため、BeutifulSoup利用バージョンから変更
        # ↓ Grouping [0] url , [1] location_id , [2] location
        PATTERN = u'<a href="(/Restaurants-g(\d+)-.*?.html)".*?>(.*?)のレストラン</a>'
        list_geo_name = re.findall(pattern=PATTERN,
                                   string=html_content)
        # columnsに合わせて再編成
        list_replace = []
        [list_replace.append([geo_name[1], geo_name[2], geo_name[0]]) for geo_name in list_geo_name]
        return list_replace


def trigger_Restaurant_tripa():
    """
    Tripadvisor Restaurant 取得用
    """

    # -------------------
    # 地域別のレストランメイン画面リストを取得（1～88） 1750件?
    BASE_URL = "https://www.tripadvisor.jp/Restaurants-g294232{oa}Japan.html#LOCATION_LIST"
    PER_PAGE, MAX_PAGE = 20, 2  # 頁当20件 / 総8ページ 2020年
    entry = [
        # {oa} 1pageの場合'-', 2page以降は'-oa9999-' ※9999:2020年現在20～1750
        Restaurant_tripa(BASE_URL.format(oa='-' if page_cnt == 0 else('-oa' + str(page_cnt * PER_PAGE) + '-')))
        for page_cnt in range(MAX_PAGE)
    ]
    data = trigger_retrievable(entry=entry)

    # -------------------
    # Excelに書き込み
    to_excel(
        data=data,
        columns=Restaurant_tripa.columns,
        excel_name='restaurant_pagelist.xlsx')


if __name__ == '__main__':
    trigger_Restaurant_tripa()
