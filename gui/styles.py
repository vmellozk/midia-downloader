MINIMAL_STYLE = """
QWidget {
    background-color: #1e1e1e;
    color: #f0f0f0;
    font-family: "Segoe UI", sans-serif;
}

QPushButton {
    background-color: #007acc;
    border: none;
    padding: 0.5em 1em;
    border-radius: 6px;
    color: white;
    font-size: 1em;
}

QPushButton:hover {
    background-color: #005f9e;
}

QGroupBox {
    border: 1px solid #444;
    border-radius: 8px;
    margin-top: 1.2em;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
    color: #aaa;
    font-weight: bold;
}

QLineEdit, QLabel {
    font-size: 1em;
}

QProgressBar {
    background-color: #333;
    color: white;
    border: none;
    border-radius: 5px;
    text-align: center;
    font-size: 0.9em;
}

QProgressBar::chunk {
    background-color: #00bcd4;
    width: 20px;
}
"""
