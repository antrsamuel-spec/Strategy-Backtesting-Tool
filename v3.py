from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QComboBox, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import pyqtgraph as pg
import yfinance as yf
import numpy as np

font = QFont("Arial", 40)

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Strategy Backtesting Tool")
        self.resize(1400, 800)
        
        self.layout = QHBoxLayout()
        self.sidebar_layout = QVBoxLayout()
        
        self.investment = 100
        
        # Sidebar
        
        self.sidebar = QWidget()
        self.sidebar.setLayout(self.sidebar_layout)
        
        self.ticker_selector = QComboBox()
        self.ticker_selector.addItems(["Apple", "NVIDIA", "Microsoft", "Google", "Amazon", "Tesla", "Meta"])
        self.ticker_selector.currentTextChanged.connect(self.select_ticker)
        
        self.signal = QLabel()
        self.signal.setFont(font)
        
        self.latest = QLabel()
        self.latest.setFont(QFont("Arial", 40))
        
        self.test_strategy = QPushButton("Test New Strategy")
        self.test_strategy.setFont(QFont("Arial"))
        self.test_strategy.clicked.connect(self.open_strategy_window)
        
        # Main Widget
        
        self.chart = pg.PlotWidget()
        self.chart.setFixedWidth(1050)
        
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        
        self.layout.addWidget(self.sidebar)
        self.sidebar_layout.addWidget(self.signal, alignment = Qt.AlignmentFlag.AlignHCenter)
        self.sidebar_layout.addWidget(self.ticker_selector, alignment = Qt.AlignmentFlag.AlignHCenter)
        self.sidebar_layout.addWidget(self.latest, alignment = Qt.AlignmentFlag.AlignHCenter)
        self.sidebar_layout.addWidget(self.test_strategy, alignment = Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.chart)
        
        
    # Strategy Parameter Window
        
    def open_strategy_window(self):
        
        self.strategy_window = QWidget()
        self.strategy_window.setWindowTitle("Strategy Parameters")
        self.strategy_window.resize(1000, 500)
        
        self.strategy_layout = QHBoxLayout()
        self.strategy_window.setLayout(self.strategy_layout)
        
        self.param1 = QComboBox()
        self.param1.addItems(["When Price is above yesterdays close by +0.5 percent:",
                              "When Price is below yesterdays close by +0.5 percent:"])
        
        self.exec1 = QComboBox()
        self.exec1.addItems(["Buy",
                             "Sell"])
        
        self.exec_button = QPushButton("Execute")
        self.exec_button.clicked.connect(self.execute_strat)
        
        self.strategy_layout.addWidget(self.param1)
        self.strategy_layout.addWidget(self.exec1)
        self.strategy_layout.addWidget(self.exec_button)
        
        self.strategy_window.show()
        
    def get_ticker(self):
            
            temp = self.ticker_selector.currentText()
            
            if temp == "Apple":
                return("AAPL")
            elif temp == "NVIDIA":
                return("NVDA")
            elif temp == "Microsoft":
                return("MSFT")
            elif temp == "Google":
                return("GOOGL")
            elif temp == "Amazon":
                return("AMZN")
            elif temp == "Tesla":
                return("TSLA")
            elif temp == "Meta":
                return("META")
        
    def execute_strat(self):

        ticker_symbol = self.get_ticker()
        print(ticker_symbol)
        
        data = yf.Ticker(ticker_symbol).history(period = "1mo", interval = "1d")
        closes = data["Close"].dropna().to_numpy()
        
        for i in range(1, len(closes)):
            previousday_close = closes[i - 1]
            currentday_close = closes[i]
            increment = (currentday_close - previousday_close) / previousday_close
            
            if self.param1.currentText() == "When Price is above yesterdays close by +0.5 percent:":
                if increment > 0.005:
                    self.investment *= (1 + increment)
                elif increment < 0:
                    self.investment *= (1 + increment)
            elif self.param1.currentText() == "When Price is below yesterdays close by +0.5 percent:":
                if increment < 0.005:
                    self.investment *= (1 + increment)
                elif increment > 0:
                    self.investment *= (1 + increment)
                    
            print(f"{self.investment:.2f}")
              
    def select_ticker(self):
        
        ticker_symbol = self.get_ticker()
        temp = self.ticker_selector.currentText()
            
        data = yf.Ticker(ticker_symbol).history(period = "1mo", interval = "1h")
        price = data["Close"].to_numpy()
        date = data.index.asi8 / 1e9
        latest_close = data["Close"].dropna().iloc[-1]
        
        self.chart.clear()
        self.chart.plot(date, price)
        
        self.signal.setText(temp)
        self.latest.setText(f"${latest_close:.2f}")
        
def main():
    
    app = QApplication()
    window = MainWindow()
    
    window.show()
    app.exec()
    
main()