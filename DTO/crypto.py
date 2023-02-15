from typing import List


def getCryptoList():
    import requests

    r = requests.get("https://s3.ap-northeast-2.amazonaws.com/crix-production/crix_master?nonce=1513815402981")
    if r.status_code != 200:
        print("Http Error Code " + str(r.status_code))
        return None

    return r.json()


class CryptoInfo:
    def __init__(self, **kwargs):
        self.fullCode = (kwargs['code'] if 'code' in kwargs else None)
        self.koreanName = (kwargs['koreanName'] if 'koreanName' in kwargs else None)
        self.localName = (kwargs['localName'] if 'localName' in kwargs else None)
        self.englishName = (kwargs['englishName'] if 'englishName' in kwargs else None)
        self.pair = (kwargs['pair'] if 'pair' in kwargs else None)
        self.baseCurrencyCode = (kwargs['baseCurrencyCode'] if 'baseCurrencyCode' in kwargs else None)
        self.quoteCurrencyCode = (kwargs['quoteCurrencyCode'] if 'quoteCurrencyCode' in kwargs else None)
        self.exchange = (kwargs['exchange'] if 'exchange' in kwargs else None)
        self.marketState = (kwargs['marketState'] if 'marketState' in kwargs else None)
        self.marketStateForIOS = (kwargs['marketStateForIOS'] if 'marketStateForIOS' in kwargs else None)
        self.isTradingSuspended = (kwargs['isTradingSuspended'] if 'isTradingSuspended' in kwargs else None)
        self.baseCurrencyDecimalPlace = (
            kwargs['baseCurrencyDecimalPlace'] if 'baseCurrencyDecimalPlace' in kwargs else None)
        self.quoteCurrencyDecimalPlace = (
            kwargs['quoteCurrencyDecimalPlace'] if 'quoteCurrencyDecimalPlace' in kwargs else None)
        self.listingDate = (kwargs['listingDate'] if 'listingDate' in kwargs else None)
        self.timestamp = (kwargs['timestamp'] if 'timestamp' in kwargs else None)
        self.tradeStatus = (kwargs['tradeStatus'] if 'tradeStatus' in kwargs else None)

        if self.fullCode is not None:
            self.code = self.fullCode[self.fullCode.find('-') + 1:]
        else:
            self.code = None

        if self.marketState == 'ACTIVE' and self.quoteCurrencyCode == 'KRW' and self.exchange == 'UPBIT':
            self.enable = True
        else:
            self.enable = False


indexer = -1


class Crypto:
    def __init__(self, cryptoInfo: CryptoInfo):
        from DTO.trade import Trade, TradeAnalysis
        from DTO.upbitReceiver import UpbitReceiver

        global indexer
        indexer += 1
        self.index: int = indexer
        self.name: str = cryptoInfo.koreanName
        self.code: str = cryptoInfo.code

        self.trades: List[Trade] = []
        self.tradeAnalysis: TradeAnalysis = TradeAnalysis()
        self.receiver: UpbitReceiver = UpbitReceiver(cryptoInfo.code)
        self.receiver.start()

    def addTradeData(self, trade):
        self.trades.insert(0, trade)
        while len(self.trades) > 3600:  # 트레이드 데이터 max 3600개
            del self.trades[-1]
