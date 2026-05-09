"""UI themes for the GUI: Light, Dark, Sepia.

Each theme defines:
  - `qss`: Qt stylesheet applied to the QApplication (widgets, scrollbars, etc.)
  - `html`: a dict of CSS color values consumed by render_html.CSS_TEMPLATE
"""
from __future__ import annotations


THEMES = {
    "light": {
        "name_en": "Light",
        "name_ne": "उज्यालो",
        "qss": "",  # default Fusion palette is fine
        "html": {
            "bg": "#ffffff",
            "text": "#222222",
            "accent": "#4a148c",        # deep purple — h2 headings
            "accent_light": "#6a1b9a",  # h3
            "accent_lighter": "#7b1fa2",  # h4
            "accent_pale": "#ce93d8",   # h2 underline
            "border": "#d1c4e9",
            "border_light": "#e1bee7",
            "panel_bg": "#f3e5f5",
            "panel_border": "#8e24aa",
            "alt_row": "#faf5ff",
            "th_bg": "#ede7f6",
            "th_text": "#4a148c",
            "highlight": "#fff8e1",
            "lagna": "#fff3e0",
            "lagna_text": "#bf360c",
            "small": "#666666",
            "retro": "#c62828",
            "delta_pos": "#2e7d32",
            "delta_neg": "#c62828",
            "footer": "#888888",
            "era_bg": "#f8f5fc",
            "era_border": "#e1bee7",
            "block_bg": "#faf5ff",
            "edu_bg": "#fff8e1",
            "edu_border": "#fbc02d",
            "bs_date": "#6a1b9a",
        },
    },

    "dark": {
        "name_en": "Dark",
        "name_ne": "अँध्यारो",
        "qss": """
            QWidget { background: #1e1e1e; color: #e0e0e0; }
            QGroupBox { border: 1px solid #444; border-radius: 4px;
                        margin-top: 12px; padding-top: 12px; }
            QGroupBox::title { color: #ce93d8; subcontrol-origin: margin;
                               left: 10px; padding: 0 4px; }
            QLineEdit, QDateEdit, QTimeEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                background: #2a2a2a; color: #e0e0e0; border: 1px solid #555;
                padding: 4px; border-radius: 3px; }
            QListWidget { background: #2a2a2a; color: #e0e0e0; border: 1px solid #555; }
            QListWidget::item:selected { background: #5a2d80; }
            QPushButton { background: #3a3a3a; color: #e0e0e0; border: 1px solid #666;
                          padding: 6px 12px; border-radius: 3px; }
            QPushButton:hover { background: #4a4a4a; }
            QTabWidget::pane { border: 1px solid #555; }
            QTabBar::tab { background: #2a2a2a; color: #ccc; padding: 6px 14px;
                           border: 1px solid #555; }
            QTabBar::tab:selected { background: #5a2d80; color: white; }
            QTextBrowser { background: #252525; color: #e0e0e0; border: 1px solid #555; }
            QStatusBar { background: #2a2a2a; color: #ccc; }
            QMenuBar { background: #2a2a2a; color: #e0e0e0; }
            QCheckBox { color: #e0e0e0; }
            QLabel { color: #e0e0e0; background: transparent; }
        """,
        "html": {
            "bg": "#252525",
            "text": "#e0e0e0",
            "accent": "#ce93d8",
            "accent_light": "#ba68c8",
            "accent_lighter": "#ab47bc",
            "accent_pale": "#7b1fa2",
            "border": "#5a3a70",
            "border_light": "#4a2a60",
            "panel_bg": "#3a2a4a",
            "panel_border": "#ab47bc",
            "alt_row": "#2e2538",
            "th_bg": "#3a2a4a",
            "th_text": "#ce93d8",
            "highlight": "#5a4a20",
            "lagna": "#5a4a20",
            "lagna_text": "#ffcc80",
            "small": "#aaaaaa",
            "retro": "#ef5350",
            "delta_pos": "#81c784",
            "delta_neg": "#ef5350",
            "footer": "#888",
            "era_bg": "#2a2238",
            "era_border": "#5a3a70",
            "block_bg": "#2a2238",
            "edu_bg": "#3a3520",
            "edu_border": "#ffb300",
            "bs_date": "#ce93d8",
        },
    },

    "sepia": {
        "name_en": "Sepia",
        "name_ne": "सेपिया (न्यानो)",
        "qss": """
            QWidget { background: #f4ecd8; color: #5b4636; }
            QGroupBox { border: 1px solid #c4ad8b; border-radius: 4px;
                        margin-top: 12px; padding-top: 12px; background: #f4ecd8; }
            QGroupBox::title { color: #7a3e3e; subcontrol-origin: margin;
                               left: 10px; padding: 0 4px; }
            QLineEdit, QDateEdit, QTimeEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                background: #fbf6e8; color: #5b4636; border: 1px solid #b89b75;
                padding: 4px; border-radius: 3px; }
            QListWidget { background: #fbf6e8; color: #5b4636; border: 1px solid #b89b75; }
            QListWidget::item:selected { background: #d2bc94; }
            QPushButton { background: #e8d8b0; color: #5b4636; border: 1px solid #b89b75;
                          padding: 6px 12px; border-radius: 3px; }
            QPushButton:hover { background: #d4c094; }
            QTabWidget::pane { border: 1px solid #b89b75; }
            QTabBar::tab { background: #e8d8b0; color: #5b4636; padding: 6px 14px;
                           border: 1px solid #b89b75; }
            QTabBar::tab:selected { background: #7a3e3e; color: #fbf6e8; }
            QTextBrowser { background: #fbf6e8; color: #5b4636; border: 1px solid #b89b75; }
            QStatusBar { background: #e8d8b0; color: #5b4636; }
            QCheckBox { color: #5b4636; }
            QLabel { color: #5b4636; background: transparent; }
        """,
        "html": {
            "bg": "#fbf6e8",
            "text": "#5b4636",
            "accent": "#7a3e3e",
            "accent_light": "#8c4a4a",
            "accent_lighter": "#9c5e5e",
            "accent_pale": "#c4ad8b",
            "border": "#c4ad8b",
            "border_light": "#d8c5a0",
            "panel_bg": "#ede0c4",
            "panel_border": "#7a3e3e",
            "alt_row": "#f4ecd8",
            "th_bg": "#ede0c4",
            "th_text": "#7a3e3e",
            "highlight": "#f8e8b0",
            "lagna": "#f8e0b8",
            "lagna_text": "#7a3e1e",
            "small": "#7a6a55",
            "retro": "#a83232",
            "delta_pos": "#3e7a3e",
            "delta_neg": "#a83232",
            "footer": "#9a8a73",
            "era_bg": "#f4e8c8",
            "era_border": "#c4ad8b",
            "block_bg": "#f4e8c8",
            "edu_bg": "#fff0c0",
            "edu_border": "#c89b3c",
            "bs_date": "#7a3e3e",
        },
    },
}


def get_theme(name: str) -> dict:
    return THEMES.get(name, THEMES["light"])
