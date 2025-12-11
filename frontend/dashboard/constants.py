from pathlib import Path


PROJECT_PATH = Path(__file__).resolve().parent.parent.parent

USER_FILES_PATH = PROJECT_PATH / "user_files"
USER_CONFIGS_PATH = USER_FILES_PATH / "configs"
USER_COLORS_PATH = USER_CONFIGS_PATH / "colors.yaml"
