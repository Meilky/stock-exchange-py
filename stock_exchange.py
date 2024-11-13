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

    def __str__(self):
        return f"- {f"{self.asks[0][1]}@{self.asks[0][0]}" if len(self.asks) > 0  else "N/A"}\n= {self.spread if self.spread != None else "N/A"}\n+ {f"{self.bids[0][1]}@{self.bids[0][0]}" if len(self.bids) > 0  else "N/A"}"


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

        ask_limit = None
        if len(self.sell_orders) > 0:
            ask_amount = 0
            ask_limit = self.sell_orders[0].limit

            for sell_order in self.sell_orders:
                if sell_order.limit != ask_limit:
                    break

                ask_amount += sell_order.amount

            data.asks.append((ask_limit, ask_amount))

        bid_limit = None
        if len(self.buy_orders) > 0:
            bid_amount = 0
            bid_limit = self.buy_orders[0].limit

            for buy_order in self.buy_orders:
                if buy_order.limit != bid_limit:
                    break

                bid_amount += buy_order.amount

            data.bids.append((bid_limit, bid_amount))

        if (bid_limit != None) and (ask_limit != None):
            data.spread = ask_limit - bid_limit

        return data


class Exchange:
    name: str
    stocks: dict[str, Stock] = {}
    orders: dict[int, Order] = {}

    next_order_id = 0

    def __init__(self, name: str):
        self.name = name

    def add_stock(self, stock: Stock):
        if stock.symbol in self.stocks.keys():
            return

        self.stocks[stock.symbol] = stock

    def get_l1_data(self, symbol: str) -> None | MarketData:
        if not (symbol in self.stocks.keys()):
            return

        return self.stocks[symbol].get_l1_data()

    def order(
        self,
        symbol: str,
        action: OrderAction,
        amount: int,
        limit: float | None = None,
    ):
        if not (symbol in self.stocks.keys()):
            return

        order = Order(self.next_order_id, symbol, action, amount, limit)

        self.next_order_id += 1

        stock = self.stocks[symbol]

        if action == OrderAction.BUY:
            stock.buy_orders.append(order)
        elif action == OrderAction.SELL:
            stock.sell_orders.append(order)


def main():
    nasdaq = Exchange("nasdaq")

    nasdaq.add_stock(Stock("aapl"))

    nasdaq.order("aapl", OrderAction.BUY, 10, 100)
    nasdaq.order("aapl", OrderAction.SELL, 10, 125)

    print(nasdaq.get_l1_data("aapl"))


if __name__ == "__main__":
    main()
