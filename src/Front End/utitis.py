import icoextract
from PIL import Image
import json
from pathlib import Path

src = Path(__file__).resolve().parent.parent
icons_folder = src / "assets" / "icons"
json_path = src / "assets" / "database"

def extract_icon_from_exe(exe_path, app_name=None):
    try:
        icoextract.IconExtractor(exe_path).export_icon(icons_folder / f"{app_name}.ico")
        return Image.open(icons_folder / f"{app_name}.ico")
    except icoextract.NoIconsAvailableError:
        print(f"لا توجد أيقونات متاحة في {exe_path}")
        return None

def load_allowed_apps():
    if not (json_path / "allowed_apps.json").exists():
        return []
    with open(json_path / "allowed_apps.json", "r") as f:
        return json.load(f)