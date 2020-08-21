import abc
import threading
from typing import List, final
from tripadv.utilpack import request_content, wait_like_human


class Retrievable(threading.Thread, metaclass=abc.ABCMeta):
    # 抽象クラスの宣言
    """指定のurlのWeb contentを取得する

    指定のカラムに基づき、
    下位のデータを構成する抽象メソッドself._parsingをoverrrideすること。

    Thread実行はfunction「trigger_retrievable」を利用すること。
    """

    def __init__(self, base_url: str):
        self._base_url = base_url
        self._result: list = None
        threading.Thread.__init__(self, name=base_url)

    @final
    def _retreive(self) -> list:
        """urlのWeb contentを取得

        1. urlからresponseを取得する（tuple res.ok, res.url, res.content)
        2. responseの正味であるres.contentを解析し抽出したlist系データを返す

        precondition:
            Retreivable::_parsingがoverrideされていること

        Returns:
            list: res.content 解析済みの結果
        """
        result = request_content(self._base_url)
        if result is None or not result[0]:
            return None
        return self._parsing(result[2].decode())

    # 抽象メソッド override促すために、NotImplementedError
    @abc.abstractmethod
    def _parsing(self, html_content: str) -> list:
        """html_contentを解析する

        html_contentを解析し、好みのデータ配列に再構成
        子クラスにて処理をOverrideすること

        Args:
            html_content (str): 解析対象のhtml構造の文字列

        Returns:
            list: 解析済みのデータ群
        """
        raise NotImplementedError

    # -----------------
    # Thread + semaphore 試み

    _cls_v_lock = threading.RLock()
    _cls_v_smp = threading.Semaphore(5)

    @classmethod
    def set_pool_size(cls, size):
        # semaphore sizeを設定
        cls._cls_v_smp._value = size

    @final
    def run(self):
        with Retrievable._cls_v_smp:
            print('run ' + self.name)
            self._result = self._retreive()
            wait_like_human(0.5, 1)

    @final
    def result(self):
        # thread.startの後、結果データを取得する
        self.join()
        print('end ' + self.name)
        return self._result


def trigger_retrievable(entry: List[Retrievable], pool: int = 5) -> list:
    """Thread TypeのRetrievableを実行し、結果をまとめて返す

    Args:
        entry (List[Retrievable]): 実行対象Retrievable
        pool (int, optional): 同時実行Thread群数. Defaults to 5.
    """
    Retrievable.set_pool_size(pool)
    threads = []
    [(entr.start(), threads.append(entr)) for entr in entry]
    payload = []
    [payload.extend(entr.result()) for entr in threads]
    return payload
