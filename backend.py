from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QAction, qApp,  QMainWindow, QRadioButton,
    QCheckBox, QMenu, QLabel,QProgressBar, QGridLayout, QSizePolicy, QWidget,QToolBar,QStatusBar,
    QFileDialog, QPushButton, QLineEdit, QMessageBox)
from PyQt5.QtGui import QIcon
from oddt_funcs import *
import re
import os
import oddt
import subprocess
import numpy as np 
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as shc
import  pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

# writing finger generate on thread
# class MyThread(QThread):
    # # Create a counter thread
    # change_value = pyqtSignal(int)

    # def __init__(self,pr,ligs):
        # self.protein=pr
        # self.ligFiles=ligs
        # super().__init__()
    # def run(self):
        # protein=self.protein
        # list_of_ligs=self.ligFiles
        # t=np.zeros((len(list_of_ligs),168))
        # for i in enumerate(list_of_ligs):
            # self.change_value.emit(i[0])
            # #self.progressbar.setValue(i[0]) 
            # try:
                # ligand = next(oddt.toolkit.readfile('sdf', list_of_ligs[i[0]]))
                # SIFP = SimpleInteractionFingerprint(ligand, protein)
                # t[i[0],:]=SIFP
            # except:
                # print(i[1]+ " led to error")
                # pass
        # df=pd.DataFrame(t,index=list_of_ligs)
        # df=df.drop(df.index[df.sum(axis=1,numeric_only=True)==0].tolist())   # here we delete the compounds with no interactions
        # self.data_f=df

class pyclust_funcs():
            
    # def startProgressBar(self):
        
        # self.thread = MyThread(self.protein,self.ligFiles)
        # self.thread.change_value.connect(self.setProgressVal)
        # self.thread.start()
        # self.data_f=self.thread.data_f.connect()
        # print(self.thread.ligFiles)
        
    # def setProgressVal(self, val):
        # self.progressbar.setValue(val) 
        
    def lig_preprocess(self):
        self.progressbar.setValue(1)
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            self.ligFiles, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","PDBQT Files (*.PDBQT);;pdbqt out Files (*.pdbqt)", options=options)
            lig_path_to_file=os.path.split(self.ligFiles[0])
            self.lig_path_to_file=lig_path_to_file[0]
            for i,name in enumerate(self.ligFiles):
                self.vina_split(name)
                self.ligFiles[i]=name+'0.sdf'
            print(self.ligFiles)
            command_lig="babel -i pdbqt *0.pdbqt -o sdf *.sdf"
            self.convert_sdf(self.lig_path_to_file,command_lig)
            self.progressbar.setValue(100)
        except:
            pass

    def protein_preprocess(self):
        self.progressbar.setValue(1)
        try:
            options = QFileDialog.Options()
            proteinf, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","pdbqt Files (*.pdbqt);;pdbqt Files (*.pdbqt)", options=options)
            protein_path_to_file=os.path.split(proteinf)
            self.protein_path_to_file=protein_path_to_file[0]
            self.proteinf=proteinf.replace(".pdbqt",".sdf")
            command_p="babel -i pdbqt " + '"'+ proteinf + '"' + " -o sdf " + '"'+ self.proteinf + '"'
            self.convert_sdf(self.protein_path_to_file,command_p)
            print(self.proteinf)
            protein = next(oddt.toolkit.readfile('sdf', self.proteinf))
            protein.protein=True
            self.protein=protein
            self.progressbar.setValue(100) 
        except:
            QMessageBox.about(self,"Protein","Error in protein reading")
      
    def convert_sdf(self,pathtof,command):
        filename=os.path.join(pathtof,'pdbqt_to_sdf.bat')
        myBat = open(filename,'w+')
        myBat.write(command)
        myBat.close()
        curpath=os.getcwd()
        os.chdir(pathtof)
        subprocess.run([filename])
        os.chdir(curpath)
                     
    def fingerGenerate(self):
        self.progressbar.setValue(1)
        protein=self.protein
        list_of_ligs=self.ligFiles
        t=np.zeros((len(list_of_ligs),168))
        for i in enumerate(list_of_ligs):
            self.progressbar.setValue(int(((i[0]+1)/len(list_of_ligs))*100)) 
            try:
                ligand = next(oddt.toolkit.readfile('sdf', list_of_ligs[i[0]]))
                SIFP = SimpleInteractionFingerprint(ligand, protein)
                t[i[0],:]=SIFP
            except:
                print(i[1]+ " led to error")
                pass
        df=pd.DataFrame(t,index=list_of_ligs)
        df=df.drop(df.index[df.sum(axis=1,numeric_only=True)==0].tolist())   # here we delete the compounds without interactions
        self.data_f=df
        QMessageBox.about(self,"Fingerprint","processed")
        
    def export_finger(self):
        try:
            name,_ = QFileDialog.getSaveFileName(self, 'Save File')
            self.data_f.to_csv(name)
            QMessageBox.about(self,"Fingerprint","Saved")
        except:
            pass
            
    def import_finger(self):
        try:
            options = QFileDialog.Options()
            fingerfile, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","csv Files (*.csv);;csv Files (*.CSV)", options=options)
            df = pd.read_csv(fingerfile,index_col=0)
            self.data_f=df
            self.lig_path_to_file=""
            QMessageBox.about(self,"Fingerprint","Imported")
        except:
            pass
            
    def plshow(self):
        try:
            plt.title("Ligand Interaction Dendrograms") 
            lbls=list(self.data_f.index)
            lbls=[x.replace(self.lig_path_to_file,"") for x in lbls ]
            lbls=[x.replace("_out.pdbqt0.sdf","") for x in lbls]
            lbls=[x.replace("/","") for x in lbls]
            lbls=[x.replace("\\","") for x in lbls]
            dend=shc.dendrogram(shc.linkage(self.data_f, method='ward'),labels=lbls,leaf_rotation=90)
            self.canvas.draw()
        except:
            QMessageBox.about(self,"Plot","No data to show")            
   
    # breaking to True will extract only the best pose 
    def vina_split(self,name_file,breaking=True):
        SECTION_END = re.compile(r'^ENDMDL')
        bas_name=os.path.basename(name_file)
        with open(name_file, 'r') as fh:
            t=fh.readlines()
        ind=0
        filename=os.path.join(self.lig_path_to_file,bas_name)+str(ind)+'.pdbqt'
        f= open(filename,"w+")
        for line in t:
            f.write(line)
            if SECTION_END.match(line):
                f.close()
                if breaking:
                    break
                ind+=1
                filename=os.path.join(self.lig_path_to_file,bas_name)+str(ind)+'.pdbqt'
                f= open(filename,"w+")      
                print(ind)
    def help(self):
        QMessageBox.about(self,"About","Developed at school of pharmacy, Shiraz University of Medical Sciences")
    # methods on GUI
    def our_methods(self):
        self.actionOpen_Protein.triggered.connect(self.protein_preprocess)  #open protein
        self.actionOpen_Ligand.triggered.connect(self.lig_preprocess)    # open ligand
        self.actionGenerate_FingerPrint_SIFP.triggered.connect(self.fingerGenerate) #SIFP
        self.actionPlot.triggered.connect(self.plshow)                             #plot show
        self.actionExport_Fingerprint.triggered.connect(self.export_finger)                             #plot show
        self.actionImport_Fingerprint.triggered.connect(self.import_finger)
        self.actionAbout.triggered.connect(self.help)
        

    
