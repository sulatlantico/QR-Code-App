import sys
import qrcode
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PIL import Image


class QRCodeApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gerador de QR Code")
        self.setGeometry(100, 100, 500, 500)

        self.qr_image_pil = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Texto / URL para o QR Code:")
        layout.addWidget(self.label)

        self.text_input = QTextEdit(self)
        self.text_input.setPlaceholderText("Digite um texto ou URL aqui...")
        layout.addWidget(self.text_input)

        button_layout = QHBoxLayout()

        self.generate_button = QPushButton("Gerar", self)
        self.generate_button.clicked.connect(self.generate_qr)
        button_layout.addWidget(self.generate_button)

        self.save_button = QPushButton("Salvar PNG", self)
        self.save_button.clicked.connect(self.save_qr)
        button_layout.addWidget(self.save_button)

        self.clear_button = QPushButton("Limpar", self)
        self.clear_button.clicked.connect(self.clear)
        button_layout.addWidget(self.clear_button)

        layout.addLayout(button_layout)

        self.preview_label = QLabel(self)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.preview_label)

        self.setLayout(layout)

    def generate_qr(self):
        data = self.text_input.toPlainText().strip()
        if not data:
            QMessageBox.warning(self, "Atenção", "Digite algum texto ou URL para gerar o QR Code.")
            return

        qr = qrcode.QRCode(
            version=None,  # auto
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill="black", back_color="white").convert("RGB")
        self.qr_image_pil = img

        # Prévia redimensionada
        preview = img.resize((380, 380), Image.Resampling.NEAREST)
        preview.save("temp_preview.png")

        pixmap = QPixmap("temp_preview.png")
        self.preview_label.setPixmap(pixmap)
        self.preview_label.setScaledContents(True)

    def save_qr(self):
        if self.qr_image_pil is None:
            QMessageBox.information(self, "Info", "Gere um QR Code antes de salvar.")
            return

        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getSaveFileName(self, "Salvar QR Code", "", "PNG Files (*.png)")
        if not file_path:
            return

        try:
            self.qr_image_pil.save(file_path, format="PNG")
            QMessageBox.information(self, "Sucesso", f"QR Code salvo em: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao salvar o QR Code:\n{e}")

    def clear(self):
        self.text_input.clear()
        self.preview_label.clear()
        self.qr_image_pil = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRCodeApp()
    window.show()
    sys.exit(app.exec())