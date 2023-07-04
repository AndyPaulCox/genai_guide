from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit
import sys


class DataFrameViewer(QWidget):
    def __init__(self, df1, df2):
        super().__init__()

        self.df1 = df1
        self.df2 = df2

        self.index = 0

        self.layout = QVBoxLayout()

        self.df1_label = QLabel("DataFrame 1")
        self.df1_text = QTextEdit()
        self.df1_text.setReadOnly(True)

        self.df2_label = QLabel("DataFrame 2")
        self.df2_text = QTextEdit()
        self.df2_text.setReadOnly(True)

        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.show_prev)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.show_next)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)

        self.layout.addWidget(self.df1_label)
        self.layout.addWidget(self.df1_text)
        self.layout.addWidget(self.df2_label)
        self.layout.addWidget(self.df2_text)
        self.layout.addWidget(self.prev_button)
        self.layout.addWidget(self.next_button)
        self.layout.addWidget(self.close_button)

        self.setLayout(self.layout)

        self.show_current()

    def show_current(self):
        if 0 <= self.index < len(self.df1):
            self.df1_text.setPlainText(str(self.df1.iloc[self.index]))
        else:
            self.df1_text.setPlainText("")

        if 0 <= self.index < len(self.df2):
            self.df2_text.setPlainText(str(self.df2.iloc[self.index]))
        else:
            self.df2_text.setPlainText("")

    def show_prev(self):
        self.index -= 1
        self.show_current()

    def show_next(self):
        self.index += 1
        self.show_current()


def main(df1, df2):
    app = QApplication([])

    viewer = DataFrameViewer(df1, df2)
    viewer.show()

    sys.exit(app.exec_())

# Replace df1 and df2 with your actual dataframes
# main(df1, df2)
