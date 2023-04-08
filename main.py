import sys
import csv
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QFileDialog, QMessageBox,QWidgetAction
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QMainWindow, QTabWidget, QHBoxLayout, QSizePolicy,QToolBar
from PyQt6 import uic, QtCore, QtGui,QtWidgets
from calc.calc import data_plot, calc, pred
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
matplotlib.use('Qt5Agg')

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
class WindowPlot(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(400, 300)
class WindowStart(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("/Users/themdq/Desktop/Diana/Журавлев/GUI/ui/open.ui", self)
        self.openButton.clicked.connect(self.open_file_dialog)
        self.actionOpen.triggered.connect(self.open_file_dialog)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите csv файл")
        self.path = file_path
        if self.path !='':
            self.wind = MainWindow(self.path)
            self.wind.show()
            self.close()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, path):
        super().__init__()
        uic.loadUi("/Users/themdq/Desktop/Diana/Журавлев/GUI/ui/main.ui", self)
        self.path = path
        self.initUI()

    def initUI(self):
        self.buildPlot.pressed.connect(self.build_plot)
        self.statusBar.showMessage(self.path)
        self.fitButton.clicked.connect(self.predict)

    def build_plot(self):
        if self.path == '':
            self.show_warning()
            return
        plot_type = self.plotCombo.currentText()
        data = data_plot(plot_type, self.path)
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot(data)
        toolbar = NavigationToolbar2QT(sc, self)
        self.window = WindowPlot(self)
        self.window.layout = QtWidgets.QVBoxLayout()
        self.window.layout.addWidget(toolbar)
        self.window.layout.addWidget(sc)
        self.window.widget = QtWidgets.QWidget()
        self.window.widget.setLayout(self.window.layout)
        self.window.setCentralWidget(self.window.widget)
        self.window.setWindowTitle(plot_type)
        self.window.show()

    def show_warning(self):
        msg = QMessageBox()
        msg.setWindowTitle("Файл не выбран")
        msg.setText("Файл не выбран! Выберите файл при помощи меню.")
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.exec()

    def predict(self):
        self.pred = PredictWindow(self.path, self.percentBox.value())
        self.pred.show()
        self.close()

class PredictWindow(QtWidgets.QMainWindow):
    def __init__(self, path, percent):
        super().__init__()
        uic.loadUi("/Users/themdq/Desktop/Diana/Журавлев/GUI/ui/prediction.ui", self)
        self.path = path
        self.percent = percent
        self.initUI()
        self.calculate()


    def initUI(self):
        self.buildPlot.pressed.connect(self.build_plot)
        self.predictButton.pressed.connect(self.predict)
        self.actionSave.triggered.connect(self.save_file)


    def build_plot(self):
        if self.path == '':
            self.show_warning()
            return
        plot_type = self.plotCombo.currentText()
        #data = data_plot(plot_type, self.path)
        data = self.output_data
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot(data)
        toolbar = NavigationToolbar2QT(sc, self)
        self.window = WindowPlot(self)
        self.window.layout = QtWidgets.QVBoxLayout()
        self.window.layout.addWidget(toolbar)
        self.window.layout.addWidget(sc)
        self.window.widget = QtWidgets.QWidget()
        self.window.widget.setLayout(self.window.layout)
        self.window.setCentralWidget(self.window.widget)
        self.window.setWindowTitle(plot_type)
        self.window.show()

    def show_warning(self):
        msg = QMessageBox()
        msg.setWindowTitle("Файл не выбран")
        msg.setText("Файл не выбран! Выберите файл при помощи меню.")
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.exec()

    def calculate(self):
        result = self.path
        res, self.output_data,self.neigh = calc(result,self.percent)
        self.statusBar.showMessage('Оценка эффективности(СКО): '+str(round(res,6)))

    def predict(self):
        lat = float(self.latLabel.text())
        long = float(self.longLabel.text())
        depth = float(self.depthLabel.text())
        res = pred(lat,long,depth,self.neigh)[0]
        self.resLabel.setText(f'Результат: {round(res,6)}')

    def save_file(self):
        save_path = QFileDialog.getSaveFileName(self,'Выберите место для сохранения файла',"","All Files (*);;Comma-separated values (*.csv)","Comma-separated values (*.csv)",)
        if save_path != '':
            with open(save_path[0], 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(map(lambda x: [x], self.output_data))

app = QtWidgets.QApplication(sys.argv)
window = WindowStart()
window.show()
app.exec()
