from PyQt5 import QtGui
import matplotlib , time
from functions import *
from matplotlib.figure import Figure
from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

matplotlib.use('Qt5Agg')


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(993, 626)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1001, 631))
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_0 = QtWidgets.QWidget()
        self.tab_0.setObjectName("tab_0")
        self.tab_0.setStyleSheet("background-color:#6096B4")
        self.LE_Target = QtWidgets.QLineEdit(self.tab_0)
        self.LE_Target.setGeometry(QtCore.QRect(20, 20, 401, 71))
        self.LE_Target.setStyleSheet("background-color:#C9EEFF")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.LE_Target.setFont(font)
        self.LE_Target.setObjectName("LE_Target")

        self.PTE_Conditions = QtWidgets.QPlainTextEdit(self.tab_0)
        self.PTE_Conditions.setGeometry(QtCore.QRect(20, 110, 401, 361))
        self.PTE_Conditions.setStyleSheet("background-color:#C9EEFF")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.PTE_Conditions.setFont(font)
        self.PTE_Conditions.setObjectName("PTE_Conditions")

        self.PB_Calculate = QtWidgets.QPushButton(self.tab_0)
        self.PB_Calculate.setGeometry(QtCore.QRect(20, 490, 401, 91))
        self.PB_Calculate.setStyleSheet("background-Color:#62CDFF")
        font = QtGui.QFont()
        font.setPointSize(16)
        self.PB_Calculate.setFont(font)
        self.PB_Calculate.setObjectName("PB_Calculate")
        self.PB_Calculate.clicked.connect(self.get_text)

        self.tabWidget.addTab(self.tab_0, "")
        self.tabWidget.setStyleSheet("background-color:#FFEAD2")

        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.tab_1.setStyleSheet("background-color:#6096B4")
        self.tableWidget = QtWidgets.QTableWidget(self.tab_1)
        self.tableWidget.setGeometry(QtCore.QRect(10, 70, 971, 521))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)


        self.counter = 0
        self.played = False
        

        
        

        
        font = QtGui.QFont()
        font.setPointSize(12)
     
        
        font = QtGui.QFont()
        font.setPointSize(12)
        

        self.PB_Pre = QtWidgets.QPushButton(self.tab_1)
        self.PB_Pre.setGeometry(QtCore.QRect(130, 10, 111, 51))
        self.PB_Pre.setStyleSheet("background-color:#62CDFF")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.PB_Pre.setFont(font)
        self.PB_Pre.setObjectName("PB_Pre")

        self.PB_next = QtWidgets.QPushButton(self.tab_1)
        self.PB_next.setGeometry(QtCore.QRect(700, 10, 111, 51))
        self.PB_next.setStyleSheet("background-color:#62CDFF")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.PB_next.setFont(font)
        self.PB_next.setObjectName("PB_next")
        self.tabWidget.addTab(self.tab_1, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.lb = QtWidgets.QLabel(self.tab_1)
        self.lb.setGeometry(QtCore.QRect(245, 5, 450, 50))
        self.lb.setAlignment(QtCore.Qt.AlignCenter)
        self.lb.setText("Step 1")
        self.lb.setStyleSheet("color:#EEE9DA; font-size: 20px;")



        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.PB_next.clicked.connect(self.next)
        self.PB_Pre.clicked.connect(self.prev)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def get_text(self):
        self.counter = 0
        iterations.clear()
        self.tabWidget.setCurrentIndex(1)

        st = self.PTE_Conditions.toPlainText().split('\n')
        
        target = self.LE_Target.text().split(" ")
        target , target_var_count = target_func(target)

        s ,  canvas = load_st(st , target_var_count)

        in_target = inverse_target(target,s.shape[1])

        
        self.tableWidget.setColumnCount(1 + s.shape[1])
        self.tableWidget.setRowCount(1 + s.shape[0])

        # Creating table indexes
        for i in range(self.tableWidget.rowCount()):
            for j in range(s.shape[1] + 1):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(i, j, item)

        # Writing Basic variables     
        basics = id_matrix(s)
        
        if basics != False:
            for i in range(len(basics)):
                row_num = i + 1
                item = self.tableWidget.item(row_num,0 )
                item.setBackground(QtGui.QColor(189, 205, 214))
                item.setText(f"X{basics[i]+1}")
        else:
            self.lb.setText("Problem cannot be solved")

        # Inserting Target row
        for j in range(len(in_target)):
            item = self.tableWidget.item(0,j+1 )
            item.setBackground(QtGui.QColor(238, 233, 218))
            item.setText(f"{in_target[j]}")
        
        # Write پایه
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setBackground(QtGui.QColor(189, 205, 214))
        item.setText("پایه")

        
        # Write RHS
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(s.shape[1], item)
        item = self.tableWidget.horizontalHeaderItem(s.shape[1])
        item.setBackground(QtGui.QColor(189, 205, 214))
        item.setText("RHS")

       
        

        
        
        


        # Writing variables as columns
        for i in range(s.shape[1]-1):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i + 1, item)
            item = self.tableWidget.horizontalHeaderItem(i + 1)
            item.setBackground(QtGui.QColor(189, 205, 214))
            item.setText(f"X{i + 1}")
        
        # Write Z
        item = self.tableWidget.item(0, 0)
        item.setBackground(QtGui.QColor(189, 205, 214))
        item.setText("Z")
        
        

        # Write 0
        item = self.tableWidget.item(0, s.shape[1])
        item.setBackground(QtGui.QColor(238, 233, 218))
        item.setText("0")

        # Inserting matrix values
        for i in range(s.shape[0]):
            for j in range(s.shape[1]):
                item = self.tableWidget.item(i+1,j+1)
                item.setBackground(QtGui.QColor(238, 233, 218))
                item.setText(f"{s[i,j]}")

        # Copy all values in iterations list

        iter = combine(in_target, s)
        iterations.append([iter,basics])
        ans = True
        while type(ans)!=str:
            m = iterations[-1][0]
            b = iterations[-1][1]
            ans = simplex(m,b)
            iterations.append(ans)


    
    def next(self):
        if self.counter < (len(iterations)-2):
            self.counter += 1
            m , b = iterations[self.counter]

            # Set Label

            self.lb.setText(f"Step {self.counter + 1}")

            # Inserting matrix values
            for i in range(m.shape[0]):
                for j in range(m.shape[1]):
                    item = self.tableWidget.item(i,j+1)
                    item.setText(f"{m[i,j]}")
            
            # Inserting Basic values
            for i in range(len(b)):
                index = b[i]
                # Find basic variable from header
                item = self.tableWidget.horizontalHeaderItem(index+1)
                header_text = item.text()
                

                # Replace basic variables
                item = self.tableWidget.item(i+1,0 )
                item.setText(f"{header_text}")
        else:
            message = iterations[self.counter+1]
            self.lb.setText(f"{message}")
            


    def prev(self):
        if self.counter > 0:
            self.counter -= 1
            m , b = iterations[self.counter]
          
            self.lb.setText(f"Step {self.counter + 1}")

            # Inserting matrix values
            for i in range(m.shape[0]):
                for j in range(m.shape[1]):
                    item = self.tableWidget.item(i,j+1)
                    item.setText(f"{m[i,j]}")
            
            # Inserting Basic values
            for i in range(len(b)):
                index = b[i]
                # Find basic variable from header
                item = self.tableWidget.horizontalHeaderItem(index+1)
                header_text = item.text()
                

                # Replace basic variables
                item = self.tableWidget.item(i+1,0 )
                item.setText(f"{header_text}")

    

        








        

        


    




        
        
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        

        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.PB_Calculate.setText(_translate("MainWindow", "Calculate"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_0), _translate("MainWindow", "Plot"))
       



        

        

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)


        

        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.PB_Pre.setText(_translate("MainWindow", "pre"))
        self.PB_next.setText(_translate("MainWindow", "next"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "Simplex"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())