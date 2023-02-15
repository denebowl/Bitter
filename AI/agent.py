from AI.ai_base import ArtificialIntelligence
from DTO.crypto import Crypto


class Agent:

    def __init__(self, parent_main, money):
        self.parent_main = parent_main

        self.maxCash: float = money
        self.walletCash: float = money
        self.walletCrypto = {}
        for crypto in cryptos.values():
            self.walletCrypto[crypto.code] = 0

        self.brain = ArtificialIntelligence(self)
        print('agent created')

    def rebirth(self):
        self.walletCash = self.maxCash
        for crypto in cryptos:
            self.walletCrypto[crypto.code] = 0
        print('rebirth')

    def addTradingData(self, crypto: Crypto):
        if len(crypto.tradeData) < 11:
            print('아직 11개가 안모였당')
            return

        self.brain.giveHomework(crypto.tradeData[:10])

    '''def buy(self, amount, fee=0.0005):  # 업비트 기준 수수료 0.05%
        price = None
        if self.parent_main.store.latestData is not None:
            price = self.parent_main.store.latestData.trade_price

        if price is None or self.walletCash < amount:
            return

        self.walletCash -= amount * (1 + fee)
        self.walletCrypto += amount / price

    def sell(self, amount, fee=0.0005):  # 업비트 기준 수수료 0.05%
        price = None
        if self.parent_main.store.latestData is not None:
            price = self.parent_main.store.latestData.trade_price

        if price is None or self.walletCrypto < (amount / price):
            return

        self.walletCrypto -= amount / price
        self.walletCash += amount * (1 - fee)'''

    def buy(self, crypto, percent, fee=0.0005):  # 업비트 기준 수수료 0.05%
        price = crypto.tradeData[0].trade_price
        amount = self.walletCash * percent * 0.01

        self.walletCash -= amount * (1 + fee)
        self.walletCrypto += amount / price

    def sell(self, crypto, percent, fee=0.0005):  # 업비트 기준 수수료 0.05%
        price = crypto.tradeData[0].trade_price
        amount = self.walletCrypto[crypto.code] * percent * 0.01

        self.walletCrypto -= amount
        self.walletCash += (amount * price) * (1 - fee)
