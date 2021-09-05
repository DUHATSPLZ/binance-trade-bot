import json

from .binance_api_manager import BinanceAPIManager
from .config import Config
from .database import Database, LogScout
from .logger import Logger

class AutoCoinSelector:
    def __init__(self, binance_manager: BinanceAPIManager, database: Database, logger: Logger, config: Config):
        self.manager = binance_manager
        self.db = database
        self.logger = logger
        self.config = config


    def get_coins_to_trade(self): 

        self.logger.info(f"Using auto coin selector to get coins to trade - min volume: {self.config.AUTO_COIN_SELECTOR_MIN_VOLUME}")

        coins_to_trade = []

        tradable_coins = self.manager.get_tradable_coins(self.config.BRIDGE.symbol)

        for coin in tradable_coins:

            if coin in self.config.AUTO_COIN_SELECTOR_BLACKLIST:
                continue

            ticker = self.manager.get_ticker(coin + self.config.BRIDGE.symbol)
            if float(ticker['quoteVolume']) >= self.config.AUTO_COIN_SELECTOR_MIN_VOLUME:
                coins_to_trade.append(coin)


        # append current coin if current coin isn't an option anymore yet we're still hodling it
        current_coin = self.db.get_current_coin()

        if current_coin is None:
            current_coin = self.config.CURRENT_COIN_SYMBOL
        else: 
            current_coin = current_coin.symbol

        if current_coin and current_coin not in coins_to_trade:
            coins_to_trade.append(current_coin)


        return coins_to_trade