from pathlib import Path


PROJECT_PATH = Path(__file__).resolve().parent.parent.parent

USER_FILES_PATH = PROJECT_PATH / "user_files"
USER_CONFIGS_PATH = USER_FILES_PATH / "configs"
USER_COLORS_PATH = USER_CONFIGS_PATH / "colors.yaml"

COLOR_SCHEME_1 = [
    "#CE5A5A",
    "#4A536A",
    "#87A8B9",
    "#F1A765",
    "#A7A1B2",
    "#8E3F25",
    "#511D43",
]
COLOR_SCHEME_2 = [
    "#a2191f",
    "#8a3800",
    "#684e00",
    "#0e6027",
    "#005d5d",
    "#0043ce",
    "#6929c4",
]
