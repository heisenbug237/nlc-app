import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import sys

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NLC India Ltd.")
        self.setWindowIcon(qtg.QIcon('/Users/saarim/git-local/nlc-app/nlc-logo.png'))
        self.setGeometry(0, 0, 400, 300)

        self.setLayout(qtw.QVBoxLayout())

        tabs = qtw.QTabWidget()
        tabs.addTab(self.systemTabUI(), "System Names")
        tabs.addTab(self.addFileTabUI(), "Add Data File")
        self.layout().addWidget(tabs)

        h_layout = qtw.QHBoxLayout()
        preview_button = qtw.QPushButton("Preview")
        proceed_button = qtw.QPushButton("Proceed")
        h_layout.addWidget(qtw.QPushButton("Reset"))
        h_layout.addWidget(preview_button)
        h_layout.addWidget(proceed_button)
        self.layout().addLayout(h_layout)
        preview_button.clicked.connect(lambda: self.previewWindow())
        proceed_button.clicked.connect(lambda: self.proceedWindow())

        self.show()

    def addSystemEntry(self, layout: qtw.QGridLayout):
        self.count+=1
        obj_name = "System " +str(self.count)
        txt = obj_name+": "
        label = qtw.QLabel(txt)
        label.setFont(qtg.QFont('Helvetica', 14))
        layout.addWidget(label, self.count, 0)
        inp = qtw.QLineEdit()
        layout.addWidget(inp, self.count, 1)
        # self.setLayout(layout)

    def systemTabUI(self):
        systemTab = qtw.QWidget()
        self.sys_layout = qtw.QVBoxLayout()

        my_label = qtw.QLabel("Enter System Names")
        my_label.setFont(qtg.QFont('Helvetica', 18))
        self.sys_layout.addWidget(my_label)
        
        self.form_layout = qtw.QGridLayout()
        self.sys_layout.addLayout(self.form_layout)
        self.count=0
        for i in range(4):
            self.addSystemEntry(self.form_layout)

        self.button_layout = qtw.QHBoxLayout()
        add_entry_button = qtw.QPushButton("Add System")
        rem_entry_button = qtw.QPushButton("Remove System")
        self.button_layout.addWidget(rem_entry_button)
        self.button_layout.addWidget(add_entry_button)
        self.sys_layout.addLayout(self.button_layout)
        rem_entry_button.clicked.connect(lambda: self.deleteItemsofForm())
        add_entry_button.clicked.connect(lambda: self.addItemstoForm())

        systemTab.setLayout(self.sys_layout)
        return systemTab

    def deleteItemsofForm(self):
        layout = self.form_layout
        if layout.count()>2:
            item2 = layout.takeAt(2*self.count-1)
            widget2 = item2.widget()
            item1 = layout.takeAt(2*self.count-2)
            widget1 = item1.widget()
            if widget2 is not None and widget1 is not None:
                widget2.setParent(None)
                widget1.setParent(None)
                self.count-=1
        else:
            pass 

    def addItemstoForm(self):
        layout = self.form_layout
        if layout.count()<20:
            self.addSystemEntry(layout)
        else:
            pass   

    def addFileTabUI(self):
        addFileTab = qtw.QWidget()
        layout = qtw.QVBoxLayout()
        self.browse_button = qtw.QPushButton("Browse File")
        self.file_label = qtw.QLabel("")
        layout.addWidget(self.browse_button)
        layout.addWidget(self.file_label)
        self.browse_button.clicked.connect(self.fileBrowser)
        addFileTab.setLayout(layout)
        return addFileTab

    def fileBrowser(self):
        # self.file_label.setText("test passed")
        fname = qtw.QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if fname:
            self.file_label.setText(str(fname[0]))

    def previewWindow(self):
        pass 


    def proceedWindow(self):
        pass
      


app = qtw.QApplication(sys.argv)
mw = MainWindow()


# run the app
app.exec_()