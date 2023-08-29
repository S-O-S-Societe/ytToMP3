import sys 
from PyQt5.QtWidgets import *
from MusicNamer import MusicNamer



class GUI(QDialog):

    def __init__(self, parent: QWidget = None) -> None:

        super().__init__(parent)
        self.setWindowTitle('Youtube To MP3')
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.mnamer = MusicNamer()
        self.create_fetch_box(position=(0,0))
        self.create_rename_box(position=(0,1))
        self.create_target_box(position=(1,0))
        self.create_table_box(position=(1,1))
        self.create_progress_bar(position=(2,0,1,2))


    def create_fetch_box(self, position):

        box = QVBoxLayout()
        fetch_group = QGroupBox('Fetch the mp3 files')
        fetch_group.setLayout(box)
        fetch_button = QPushButton('Fetch local mp3 files')
        fetch_button.clicked.connect(self.folder_dialog)
        self.folder_label = QLabel(self)
        box.addWidget(fetch_button)
        box.addWidget(self.folder_label)
        self.layout.addWidget(fetch_group, *position)

    def create_rename_box(self, position):

        box = QVBoxLayout()
        rename_group = QGroupBox('Rename the mp3 files')
        rename_group.setLayout(box)
        rename_button = QPushButton('Rename local mp3 files')
        rename_button.clicked.connect(self.mnamer.renameFiles)
        box.addWidget(rename_button)
        self.layout.addWidget(rename_group, *position)


    def create_target_box(self, position):

        box = QVBoxLayout()
        target_group = QGroupBox('Where to move the processed files')
        target_group.setLayout(box)
        target_button = QPushButton('Target folder')
        target_button.clicked.connect(self.target_dialog)
        self.target_label = QLabel(self)
        box.addWidget(target_button)
        box.addWidget(self.target_label)
        self.layout.addWidget(target_group, *position)

    def create_table_box(self, position):

        widget = QTabWidget()
        widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
        tab = QWidget()
        self.tableWidget = QTableWidget(10, 10)
        tabhbox = QHBoxLayout()
        tabhbox.setContentsMargins(5,5,5,5)
        tabhbox.addWidget(self.tableWidget)
        tab.setLayout(tabhbox)
        widget.addTab(tab, 'Content')
        self.layout.addWidget(widget, *position)

    def target_dialog(self):

        response = QFileDialog.getExistingDirectory(
            parent=self,
            caption='Select a folder',
        )
        self.mnamer.target_path = response
        self.target_label.setText(response)

    def folder_dialog(self):

        response = QFileDialog.getExistingDirectory(
            parent=self,
            caption='Select a folder',
        )
        self.mnamer.folder = response 
        self.folder_label.setText(response)
        self.mnamer.listMP3Files()
        self.tableWidget.setRowCount(len(self.mnamer.files))
        files_dict = [{'original':path} for path in self.mnamer.files]
        row = 0
        for file in files_dict:
            self.tableWidget.setItem(row, 0 , QTableWidgetItem(file['original']))
            row = row + 1

    
    def create_progress_bar(self, position):

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)
        self.layout.addWidget(self.pbar, *position)


app = QApplication([])
screen = GUI()
screen.show()
sys.exit(app.exec_())
