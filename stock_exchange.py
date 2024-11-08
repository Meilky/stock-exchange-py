from enum import StrEnum, auto


class OrderAction(StrEnum):
    BUY = auto()
    SELL = auto()


class Order:
    id: int
    symbol: str
    action: OrderAction
    amount: int
    limit: float | None

    def __init__(
        self,
        id: int,
        symbol: str,
        action: OrderAction,
        amount: int,
        limit: float | None = None,
    ):
        self.id = id
        self.symbol = symbol
        self.action = action
        self.amount = amount
        self.limit = limit


class MarketData:
    bids: list[tuple[float | None, int]]
    asks: list[tuple[float | None, int]]

    spread: float | None

    def __init__(self):
        self.asks = []
        self.bids = []
        self.spread = None


class Stock:
    symbol: str
    sell_orders: list[Order]
    buy_orders: list[Order]

    def __init__(self, symbol: str):
        self.symbol = symbol
        self.sell_orders = []
        self.buy_orders = []

    def get_l1_data(self) -> MarketData:
        data = MarketData()

        ask_amount = None
        if len(self.sell_orders) > 0:
            ask = self.sell_orders[0]

            data.asks.append(())
        highest_bid = self.buy_orders[0]
        lowest_ask = self.sell_orders[0]

        spread = float("nan")

        # NaN are not equal to each other
        if (lowest_ask.limit == lowest_ask.limit) and (
            highest_bid.limit == highest_bid.limit
        ):
            spread = lowest_ask.limit - highest_bid.limit

        return data


class Exchange:
    name: str
    stocks: dict[str, Stock] = {}
    orders: dict[int, Order] = {}

    next_order_id = 0

    def __init__(self, name: str):
        self.name = name

    def add_stock(self, stock: Stock):
        self.stocks[stock.symbol] = stock

    def order(
        self,
        symbol: str,
        action: OrderAction,
        amount: int,
        limit: float | None = None,
    ):
        order = Order()

        order.id = self.next_order_id
        order.symbol = symbol
        order.limit = limit
        order.action = action
        order.amount = amount

        self.next_order_id += 1

        return order


def main():
    nasdaq = Exchange("nasdaq")

    nasdaq.add_stock(Stock("aaple"))


if __name__ == "main":
    main()
