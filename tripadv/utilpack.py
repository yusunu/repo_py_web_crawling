
from time import sleep
import numpy as np
import pandas
import requests


def wait_like_human(wait_time=2, delay=2):
    """ 待機(sleep)する

    待機時間：基本待機(秒)「wait_time」～最大遅延(秒)「wait_time + delay」
       例)Deafultの場合 2～4秒の範囲で待機時間が決定

    Args:
        wait_time (int, optional): 基本待機時間. Defaults to 2秒.
        delay (int, optional): 最大遅延加味. Defaults to 2秒.
    """
    wait_time = float('{:.3f}'.format(np.random.rand() * delay + wait_time))
    sleep(wait_time)


def task_with_retry(retry=3, wait_time=1):
    """ 関数リトライ

    関数実行後Exception発生時リトライさせる
    decorator

    Args:
        task (function): 実行対象の関数
        retry (int, optional): リトライ回数. Defaults to 1回.
        delay (int, optional): リトライ再開遅延. Defaults to 1秒.
    Returns:
        decorator (None有)
    """
    def deco(task):
        def wrapper(*args, **kwargs):
            for i in range(1, retry + 1):
                try:
                    return task(*args, **kwargs)
                except Exception as e:
                    print("error:{e} retry:{i}/{max}".format(e=e, i=i, max=retry))
                    wait_like_human(wait_time)
            return None
        return wrapper
    return deco


@task_with_retry(retry=2, wait_time=3)
def request_content(url: str, opts={}) -> any:
    """送信 [GET]

    Args:
        url (str): base url
        opts (dict, optional): parameter or options for url Defaults to {}.

    Returns:
        tules[...]: res.ok, res.url, res.content
    """
    with requests.get(url.format_map(opts)) as res:
        return res.ok, res.url, res.content


def to_excel(data: list, columns: list, sheet_name='output', excel_name='result.xlsx'):
    """結果dictをExcelに書き込み

    1 Sheet, 1 Excel File
    Args:
        data (list): メインデータ群
        columns (list): headerとなるcolums名
        sheet_name (str, optional): Excelシート. Defaults to 'output'.
        excel_name (str, optional): Excelファイル. Defaults to 'result.xlsx'.
    """
    df = pandas.DataFrame(data=data, columns=columns)
    df.to_excel(excel_name,
                sheet_name=sheet_name,
                index=False,
                encoding='utf-8')
