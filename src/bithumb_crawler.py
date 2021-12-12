"""Bithumb API.

Author:
    - Name: Wooshik Myung
    - Email: wooshik.m@gmail.com
"""

from collections import defaultdict
from typing import DefaultDict, List

import pybithumb


class BithumbAPI:
    """Bithumb API.

    References:
        https://wikidocs.net/21881

    Notes:
        * pybithumb.get_market_detail("BTC"): Tuple[float, float, float, float]
        * pybithumb.get_orderbook("BTC"): Dict[str, Any]
        * pybithumb.get_current_price("ALL"): Dict[str, Dict[str, float]]
        * pybithumb.get_ohlcv("BTC")

        + we also can consider python CCXT.
    """

    tickers = pybithumb.get_tickers()
    prices: DefaultDict[str, List[float]] = defaultdict(list)

    def print_price(self) -> None:
        """Print prices."""
        while True:
            for ticker in self.tickers:
                self.prices[ticker].append(pybithumb.get_current_price(ticker))
            print(self.prices)
