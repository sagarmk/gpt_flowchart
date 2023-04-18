from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPlainTextEdit, QPushButton, QFileDialog,
                             QGraphicsView, QGraphicsScene, QVBoxLayout, QHBoxLayout, QWidget, QSplitter)
from PyQt5.QtGui import QClipboard, QPainter
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtSvg import QGraphicsSvgItem
import os
import tempfile  
from open.gpt import GPT


class MainWindow(QMainWindow):
    """
    Main window class that inherits from QMainWindow and handles the Graphviz flowchart tool's UI.
    """

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Initializes the UI components and their layout.
        """

        self.setWindowTitle("GPT Flowchart Tool")

        # Set up label for input text area
        input_label = QLabel("What is the flowchart about:")

        # Set up DOT code editor and flowchart display
        self.dot_editor = QPlainTextEdit()
        self.flowchart_view = QGraphicsView()
        self.flowchart_view.setRenderHint(QPainter.Antialiasing)

        # Set up flowchart scene and splitter for resizing
        self.flowchart_scene = QGraphicsScene(self)
        self.flowchart_view.setScene(self.flowchart_scene)
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.dot_editor)
        splitter.addWidget(self.flowchart_view)
        splitter.setSizes([200, 600])

        # Set up buttons and their layout
        self.build_button = QPushButton("Build Flowchart")
        self.build_button.clicked.connect(self.build_flowchart)
        self.copy_button = QPushButton("Copy SVG")
        self.copy_button.clicked.connect(self.copy_svg)
        self.save_button = QPushButton("Save SVG")
        self.save_button.clicked.connect(self.save_svg)
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.build_button)
        buttons_layout.addWidget(self.copy_button)
        buttons_layout.addWidget(self.save_button)

        # Set up main layout and central widget
        main_layout = QVBoxLayout()
        main_layout.addWidget(splitter)
        main_layout.addLayout(buttons_layout)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def build_flowchart(self):
            """
            Generates an SVG flowchart from the input DOT code using Graphviz.
            """

            dot_code = self.dot_editor.toPlainText()
            gptquery = GPT()
            system_message = "You are graphviz bot, who responds only with graphviz code."
            prompt = f"Based on below provided text query design a graphviz flowchart code, try to make a vertical flowchart. Query:{dot_code}"
            response = gptquery.request_gpt(system_message, prompt)
            
            if 'content' in response:
                dot_code = response['content']
            else:
                dot_code = None



            # Write DOT code to a temporary file
            with tempfile.NamedTemporaryFile('w', delete=False, suffix='.dot') as dot_temp:
                dot_temp.write(dot_code)
                dot_temp.flush()

                # Generate SVG from DOT code using Graphviz
                with tempfile.NamedTemporaryFile('w', delete=False, suffix='.svg') as svg_temp:
                    process = QProcess(self)
                    process.start("dot", ["-Tsvg", dot_temp.name, "-o", svg_temp.name])
                    process.waitForFinished()

                    # Display generated SVG in the QGraphicsView
                    self.flowchart_scene.clear()
                    svg_item = QGraphicsSvgItem(svg_temp.name)
                    self.flowchart_scene.addItem(svg_item)
                    self.flowchart_view.setSceneRect(svg_item.boundingRect())

                    # Store the SVG file name for later use
                    self.temp_svg_filename = svg_temp.name

                # Clean up the temporary DOT file
                os.unlink(dot_temp.name)

    def copy_svg(self):
        """
        Copies the generated SVG code to the clipboard.
        """

        with open("temp.svg", "r") as f:
            svg_code = f.read()

        clipboard = QApplication.clipboard()
        clipboard.setText(svg_code, QClipboard.Clipboard)

    def save_svg(self):
        """
        Saves the generated SVG to a user-selected file.
        """

        file_name, _ = QFileDialog.getSaveFileName(self, "Save SVG", "", "SVG files (*.svg)")
        if file_name:
            os.rename("temp.svg", file_name)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
