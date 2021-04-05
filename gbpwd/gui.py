import os

from PySide2.QtWidgets import *
from PySide2.QtCore import Qt

from . import generator

class CompleteMainGui(QWidget):
    
    file = None
    binary = b''
    lenght = 20

    def __init__(self, width=300, height=200):
        super().__init__()

        self.master_key_label = QLabel('Master key type:')
        self.master_key_combo = QComboBox()
        self.master_key_combo.insertItems(0, ('Password', 'File (first 256 bits)'))
        self.master_key_combo.currentIndexChanged.connect(self.comboboxChange)

        master_key = QHBoxLayout()
        master_key.addWidget(self.master_key_label)
        master_key.addWidget(self.master_key_combo)

        self.file_label = QLabel('Select your file:')
        self.file_name_label = QLabel('no file selected')
        self.file_name_label.setAlignment(Qt.AlignRight|Qt.AlignBottom)
        self.file_button = QPushButton('Select')
        self.file_button.clicked.connect(self.file_btn)
        self.file_button.setEnabled(False)

        file = QHBoxLayout()
        file.addWidget(self.file_label)
        file.addWidget(self.file_name_label)
        file.addWidget(self.file_button)

        self.password_label = QLabel('Password:')
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        
        password = QHBoxLayout()
        password.addWidget(self.password_label)
        password.addWidget(self.password_edit, stretch=1)

        self.token_label = QLabel('Token:')
        self.token_edit = QLineEdit()

        token = QHBoxLayout()
        token.addWidget(self.token_label)
        token.addWidget(self.token_edit, stretch=1)

        self.func_label = QLabel('Select the function:')
        self.func_combo = QComboBox()
        self.func_combo.addItems(('scrypt()', 'PBKDF2()'))

        func = QHBoxLayout()
        func.addWidget(self.func_label)
        func.addWidget(self.func_combo)

        self.copy_checkbox = QCheckBox('Copy to clipboard')
        self.extra_char_checkbox = QCheckBox('Extra chars')

        checkboxes = QHBoxLayout()
        checkboxes.addWidget(self.copy_checkbox)
        checkboxes.addWidget(self.extra_char_checkbox)

        self.generate_btn = QPushButton('Generate')
        self.close_btn = QPushButton('Close')
        self.generate_btn.clicked.connect(self.generateClick)
        self.close_btn.clicked.connect(exit)

        buttons = QHBoxLayout()
        buttons.addWidget(self.generate_btn, stretch=1)
        buttons.addWidget(self.close_btn, stretch=1)

        main_layout = QVBoxLayout()

        main_layout.addLayout(master_key)
        main_layout.addLayout(file)
        main_layout.addLayout(password)
        main_layout.addLayout(token)
        main_layout.addLayout(func)
        main_layout.addLayout(checkboxes)
        main_layout.addLayout(buttons)

        self.setLayout(main_layout)
        self.setWindowTitle('GBpwd')

        self.setFixedSize(width, height)
    
    def file_btn(self):
        self.file_gui = QFileDialog()

        file_path, _ = self.file_gui.getOpenFileName(self, options=QFileDialog.DontUseNativeDialog)

        if file_path:
            self.file_name_label.setText(os.path.basename(file_path))
            self.file = open(file_path, 'rb')

    def comboboxChange(self, i):
        if i == 0:
            if self.file:
                self.file.close()
                self.file = None
            self.file_name_label.setText('no file selected')
            self.file_button.setEnabled(False)
            self.password_edit.setEnabled(True)
        elif i == 1:
            self.file_button.setEnabled(True)
            self.password_edit.setEnabled(False)

    def generateClick(self):
        if self.master_key_combo.currentIndex() == 0:
            password = self.password_edit.text().encode('utf8')
        else:
            password = b''

        if self.master_key_combo.currentIndex() == 1:
            binary = self.file.read(16)
        else:
            binary = b''

        token = self.token_edit.text()

        if self.func_combo.currentIndex() == 0:
            func = generator.ScryptGen(token, password, binary, self.lenght)
        elif self.func_combo.currentIndex() == 1:
            func = generator.PBKDF2Gen(token, password, binary, self.lenght)

        self.sucess_gui = SucessGui(func.derive())
        self.sucess_gui.show()

    def closeEvent(self, event):
        exit()

class SucessGui(QWidget):

    def __init__(self, pwd='', width=150, height=150):
        super().__init__()
        
        main_layout = QVBoxLayout()

        self.label = QLabel('You password has been generated!')
        
        main_layout.addWidget(self.label)

        self.pwd_edit = QLineEdit(pwd, readOnly=True)
        self.pwd_edit.setEchoMode(QLineEdit.NoEcho)
        
        main_layout.addWidget(self.pwd_edit)

        self.show_btn = QPushButton('Show')
        self.close_btn = QPushButton('Close')
        self.show_btn.clicked.connect(self.show_btn_clicked)
        self.close_btn.clicked.connect(self.close)

        btns_layout = QHBoxLayout()
        btns_layout.addWidget(self.show_btn)
        btns_layout.addWidget(self.close_btn)

        main_layout.addLayout(btns_layout)

        self.setLayout(main_layout)
        self.resize(width, height)
        self.setWindowTitle('Sucess!')

        self.setWindowFlag(Qt.WindowStaysOnTopHint)

    def show_btn_clicked(self):
        if self.show_btn.text() == 'Show':
            self.show_btn.setText('Hide')
            self.pwd_edit.setEchoMode(QLineEdit.Normal)
        else:
            self.show_btn.setText('Show')
            self.pwd_edit.setEchoMode(QLineEdit.NoEcho)