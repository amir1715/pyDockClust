from backend import *

 
class Ui_MainWindow(QMainWindow,pyclust_funcs):


    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(797, 600)
        MainWindow.setMinimumSize(QtCore.QSize(797, 600))
        MainWindow.setMaximumSize(QtCore.QSize(797, 600))
        MainWindow.setBaseSize(QtCore.QSize(797, 600))
        #
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(MainWindow)
        self.canvas.resize(797, 600)
        #
        toolbar = NavigationToolbar(self.canvas, self)  #
        layout = QtWidgets.QVBoxLayout()        #
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)    #
        self.centralwidget = QtWidgets.QWidget(MainWindow) #
        self.centralwidget.setLayout(layout)  #
        self.progressbar = QProgressBar()
        layout.addWidget(self.progressbar)
        
        
        #self.progressbar.setOrientation(Qt.Vertical)
        self.progressbar.setMaximum(100)
        self.progressbar.setStyleSheet("QProgressBar {border: 2px solid grey;border-radius:8px;padding:1px}"
                                       "QProgressBar::chunk {background:yellow}")
        
        
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 797, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_Protein = QtWidgets.QAction(MainWindow)
        self.actionOpen_Protein.setObjectName("actionOpen_Protein")
        self.actionOpen_Ligand = QtWidgets.QAction(MainWindow)
        self.actionOpen_Ligand.setObjectName("actionOpen_Ligand")
        self.actionGenerate_FingerPrint_IFP = QtWidgets.QAction(MainWindow)
        self.actionGenerate_FingerPrint_IFP.setObjectName("actionGenerate_FingerPrint_IFP")
        self.actionGenerate_FingerPrint_SIFP = QtWidgets.QAction(MainWindow)
        self.actionGenerate_FingerPrint_SIFP.setObjectName("actionGenerate_FingerPrint_SIFP")
        self.actionPlot = QtWidgets.QAction(MainWindow)
        self.actionPlot.setObjectName("actionPlot")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionExport_Fingerprint = QtWidgets.QAction(MainWindow)
        self.actionExport_Fingerprint.setObjectName("actionExport_Fingerprint")
        self.actionImport_Fingerprint = QtWidgets.QAction(MainWindow)
        self.actionImport_Fingerprint.setObjectName("actionImport_Fingerprint")
        self.menuFile.addAction(self.actionOpen_Protein)
        self.menuFile.addAction(self.actionOpen_Ligand)
        self.menuFile.addAction(self.actionGenerate_FingerPrint_SIFP)
        self.menuFile.addAction(self.actionPlot)
        self.menuFile.addAction(self.actionExport_Fingerprint)
        self.menuFile.addAction(self.actionImport_Fingerprint)
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #
        self.our_methods()
        self.actionExit.triggered.connect(MainWindow.close)
        #

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "pyDockCluster"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionOpen_Protein.setText(_translate("MainWindow", "Open Protein"))
        self.actionOpen_Ligand.setText(_translate("MainWindow", "Open Ligand"))
        self.actionGenerate_FingerPrint_IFP.setText(_translate("MainWindow", "Generate FingerPrint IFP"))
        self.actionGenerate_FingerPrint_SIFP.setText(_translate("MainWindow", "Generate FingerPrint SIFP"))
        self.actionPlot.setText(_translate("MainWindow", "Plot Dendrogram"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExport_Fingerprint.setText(_translate("MainWindow", "Export Fingerprint"))
        self.actionImport_Fingerprint.setText(_translate("MainWindow", "Import Fingerprint"))


         
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())