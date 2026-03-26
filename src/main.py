import os 
import sys

import io

import qrcode
from PIL import Image

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QFileDialog, QMessageBox, QSpinBox)
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtCore import Qt


class QRCodeGenerator(QMainWindow):
    """Main window for QR code generator application"""
    
    def __init__(self):
        super().__init__()
        self.current_qr_image = None
        self.initUI()
        
    def initUI(self):
        """Initialize the user interface"""
        self.setWindowTitle("QR code generator")
        self.setGeometry(300, 300, 800, 800)
        
       # Set application icon if exists
        if os.path.exists("resources/icon.ico"):
            self.setWindowIcon(QIcon("resources/icon.ico"))

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title_label = QLabel("QR code generator")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Input section
        input_section = self.create_input_section()
        main_layout.addLayout(input_section)
        
        # Controls section
        controls_layout = self.create_controls_section()
        main_layout.addLayout(controls_layout)
        
        # Display section
        display_section = self.create_display_section()
        main_layout.addLayout(display_section)
        
        # Status bar
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #666; padding: 5px;")
        main_layout.addWidget(self.status_label)
        
        # Apply styles
        self.apply_styles()
    
    def create_input_section(self):
        """Create input section layout"""
        layout = QVBoxLayout()
        
        text_label = QLabel("Enter text or URL:")
        text_label.setFont(QFont("Arial", 10))
        layout.addWidget(text_label)
        
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Enter text, URL or any data to generate QR code...")
        self.text_input.setMaximumHeight(100)
        layout.addWidget(self.text_input)
        
        # Size settings
        size_layout = QHBoxLayout()
        size_label = QLabel("QR code size (pixels):")
        size_label.setFont(QFont("Arial", 10))
        size_layout.addWidget(size_label)
        
        self.size_spinbox = QSpinBox()
        self.size_spinbox.setRange(100, 1000)
        self.size_spinbox.setValue(600)
        self.size_spinbox.setSuffix(" px")
        size_layout.addWidget(self.size_spinbox)
        size_layout.addStretch()
        
        layout.addLayout(size_layout)
        
        return layout
    
    def create_controls_section(self):
        """Create controls section layout"""
        layout = QHBoxLayout()
        
        self.generate_btn = QPushButton("Generate QR code")
        self.generate_btn.clicked.connect(self.generate_qr)
        layout.addWidget(self.generate_btn)
        
        self.save_btn = QPushButton("Save QR code")
        self.save_btn.clicked.connect(self.save_qr)
        self.save_btn.setEnabled(False)
        layout.addWidget(self.save_btn)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_all)
        layout.addWidget(self.clear_btn)
        
        return layout
    
    def create_display_section(self):
        """Create display section layout"""
        layout = QVBoxLayout()
        
        qr_label = QLabel("QR code preview:")
        qr_label.setFont(QFont("Arial", 10))
        layout.addWidget(qr_label)
        
        self.qr_display = QLabel()
        self.qr_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_display.setStyleSheet("""
            QLabel {
                border: 2px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                background-color: white;
                min-height: 600px;
            }
        """)
        layout.addWidget(self.qr_display)
        
        return layout
    
    def apply_styles(self):
        """Apply custom styles to buttons"""
        button_style = """
            QPushButton {
                padding: 10px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 5px;
                border: none;
            }
        """
        
        self.generate_btn.setStyleSheet(button_style + """
            QPushButton {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        self.save_btn.setStyleSheet(button_style + """
            QPushButton {
                background-color: #008CBA;
                color: white;
            }
            QPushButton:hover {
                background-color: #0077a3;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        
        self.clear_btn.setStyleSheet(button_style + """
            QPushButton {
                background-color: #f44336;
                color: white;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
    
    def generate_qr(self):
        """Generate QR code from input text"""
        text = self.text_input.toPlainText().strip()
        
        if not text:
            QMessageBox.warning(self, "Warning", "Please enter text to generate QR code!")
            return
        
        try:
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(text)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Resize
            size = self.size_spinbox.value()
            img = img.resize((size, size), Image.Resampling.LANCZOS)
            
            # Store current image
            self.current_qr_image = img
            
            # Convert to QPixmap for display
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            
            pixmap = QPixmap()
            pixmap.loadFromData(buffer.getvalue())
            
            # Display
            self.qr_display.setPixmap(pixmap.scaled(
                size, size, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            ))
            
            self.save_btn.setEnabled(True)
            self.update_status(f"QR code generated successfully! Size: {size}x{size} pixels", "success")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating QR code:\n{str(e)}")
            self.update_status("Error generating QR code", "error")
    
    def save_qr(self):
        """Save QR code to file"""
        if self.current_qr_image is None:
            QMessageBox.warning(self, "Warning", "Please generate QR code first!")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Save QR code", 
            "qrcode.png", 
            "PNG Images (*.png);;All Files (*)"
        )
        
        if file_path:
            try:
                self.current_qr_image.save(file_path, "PNG")
                QMessageBox.information(self, "Success", f"QR code saved successfully:\n{file_path}")
                self.update_status(f"QR code saved: {file_path}", "success")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error saving file:\n{str(e)}")
                self.update_status("Error saving file", "error")
    
    def clear_all(self):
        """Clear all input and output"""
        self.text_input.clear()
        self.qr_display.clear()
        self.current_qr_image = None
        self.save_btn.setEnabled(False)
        self.size_spinbox.setValue(600)
        self.update_status("Cleared. Ready to work", "info")
    
    def update_status(self, message, status_type="info"):
        """Update status bar with message"""
        colors = {
            "success": "#4CAF50",
            "error": "#f44336",
            "info": "#666"
        }
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {colors.get(status_type, '#666')}; padding: 5px;")


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = QRCodeGenerator()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()