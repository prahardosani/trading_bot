import backtrader as bt # Import backtrader for backtesting and strategy implementation
import os # Import the os module for working with file paths

# The code below defines a class called MovingAverageCrossStrategy that inherits from bt.Strategy. This is where you define your trading strategy.
# params attribute: This section defines parameters that can be customized when creating an instance of the strategy. These parameters include the short and long moving average periods and the risk percentage.

class MovingAverageCrossStrategy(bt.Strategy):
    params = (
        ("short_period", 10),
        ("long_period", 50),
        ("risk_percentage", 0.75),  # 75% of portfolio risk
    )

    # __init__(self): This is the constructor method for the strategy. It is called when a strategy object is created. In this method:

    # self.short_ma and self.long_ma are created as simple moving averages (SMA) based on the historical closing prices (self.data.close) with periods specified by self.params.short_period and self.params.long_period. 

    def __init__(self):
        self.short_ma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.short_period)
        self.long_ma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.long_period)

    #next(self): This method is called for each data point (e.g., daily data) and is where your trading logic is implemented. In this method:

    # It checks whether the short-term moving average is greater than the long-term moving average. If it is, it considers it a "Golden Cross" and a potential buy signal.

    # If the position size is 0 (no open position), it calculates the position size based on the risk percentage of the available cash and executes a buy order (self.buy).

    # Conversely, if the short-term moving average is less than the long-term moving average, it considers it a "Death Cross" and a potential sell signal.

    # If there's an open position (position size is greater than 0), it executes a sell order (self.close) to close the position.

    def next(self):
        if self.short_ma > self.long_ma:
            # Golden Cross: Buy
            if self.position.size == 0:
                risk = self.broker.get_cash() * self.params.risk_percentage
                self.size = int(risk / self.data.close)
                self.buy(size=self.size)

        elif self.short_ma < self.long_ma:
            # Death Cross: Sell
            if self.position.size > 0:
                self.close()

if __name__ == "__main__": # Ensures that the following code is executed only if the script is run as the main program.
    # Define the folder where the CSV data is located
    data_folder = "./Historical_Data"

    # Specify the CSV file name
    csv_file_name = "AAPL_2020-01-01_2024-08-17.csv"

    # Create a Cerebro engine
    cerebro = bt.Cerebro()

    # Add a data feed (CSV file with OHLCV data)
    data_path = os.path.join(data_folder, csv_file_name)

    # Add a data feed (e.g., CSV file with OHLCV data)
    data = bt.feeds.YahooFinanceCSVData(dataname=data_path)

    cerebro.adddata(data)
    cerebro.addstrategy(MovingAverageCrossStrategy)

    # Set your initial cash
    cerebro.broker.set_cash(1000)

    # Define position size and commission
    cerebro.addsizer(bt.sizers.PercentSizer, percents=75)
    cerebro.broker.setcommission(commission=0.001)  # 0.1% commission

    # Print the starting cash
    print(f"Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")

    # Run the backtest
    cerebro.run()

    # Print the final portfolio value
    print(f"Ending Portfolio Value: {cerebro.broker.getvalue():.2f}")