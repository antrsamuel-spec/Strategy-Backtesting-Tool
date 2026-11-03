from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QComboBox, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import pyqtgraph as pg
import yfinance as yf
import numpy as np

signal = yf.Ticker("AAPL")
data = signal.history(period = "1mo", interval = "1h")
price = data["Close"].to_numpy()
date = data.index.asi8 / 1e9
latest_close = data["Close"].dropna().iloc[-1]

font = QFont("Arial", 40)

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Strategy Backtesting Tool")
        self.resize(1400, 800)
        
        self.layout = QHBoxLayout()
        self.sidebar_layout = QVBoxLayout()
        
        self.sidebar = QWidget()
        self.sidebar.setLayout(self.sidebar_layout)
        
        self.signal = QLabel("AAPL")
        self.signal.setFont(font)
        
        self.latest = QLabel(f"${latest_close:.2f}")
        self.latest.setFont(QFont("Arial", 40))
        
        self.chart = pg.PlotWidget()
        self.chart.plot(date, price)
        self.chart.setFixedWidth(1050)
        
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        
        self.layout.addWidget(self.sidebar)
        self.sidebar_layout.addWidget(self.signal, alignment = Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.sidebar_layout.addWidget(self.latest, alignment = Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.chart)
        
def main():
    
    app = QApplication()
    window = MainWindow()
    
    window.show()
    app.exec()
    
main()