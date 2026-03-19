from pathlib import Path

class ThemeManager:
    def __init__(self, app):
        self.app = app

    def handle_theme_change(self, is_dark):
        mode = "dark" if is_dark else "light"
        self.apply_theme(mode)

    def apply_theme(self, mode):
        style_dir = Path(__file__).parent.parent / "resources" / "styles"
        theme_file = f"{mode}.qss"
        structure_file = "style.qss"

        try:
            with open(style_dir / theme_file, "r", encoding="utf-8") as f:
                theme_content = f.read()
            with open(style_dir / structure_file, "r", encoding="utf-8") as f:
                structure_content = f.read()
            
            self.app.setStyleSheet(theme_content + "\n" + structure_content)
        except Exception as e:
            print(f"❌ Erreur de thème : {e}")