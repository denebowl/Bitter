from typing import Dict

from DTO.crypto import CryptoInfo, Crypto, getCryptoList
from DTO.database import MysqlDatabase

coinList: Dict[str, CryptoInfo] = {}
cryptos: Dict[str, Crypto] = {}
mysqlDatabase: MysqlDatabase or None = None


def init():
    global coinList, cryptos, mysqlDatabase

    # 코인리스트 웹에서 받아옴
    for crypto in getCryptoList():
        obj = CryptoInfo(**crypto)
        if obj.enable:
            coinList[obj.code] = obj

        # 임시수량제한
        # if len(coinList) > 2:
        #    break

    # 크립토 인포 생성
    for cryptoInfo in coinList.values():
        if cryptoInfo.enable:
            cryptos[cryptoInfo.code] = Crypto(cryptoInfo)

    # 데이터베이스 연결 생성
    mysqlDatabase = MysqlDatabase()


init()