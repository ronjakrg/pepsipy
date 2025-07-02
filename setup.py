from setuptools import setup
from setuptools.command.install import install as _install
from setuptools.command.build_py import build_py as _build_py

import sys
import zipfile
import urllib.request
from pathlib import Path


def install_ipc():
    """
    Downloads and installs IPC 2.0 in /external/ipc-2.0.1 if it doesn't exist yet.
    """

    print("Warning: This script is currently disabled to decrease the project's size.")
    return

    EXTERNAL_PATH = Path(__file__).resolve().parent / "src" / "pepsi" / "external"
    ipc_path = EXTERNAL_PATH / "ipc-2.0.1"

    print("Checking if IPC 2.0 is installed ...")
    if ipc_path.exists() and ipc_path.is_dir():
        print("IPC 2.0 is already installed.")
        return
    ipc_url = "https://ipc2.mimuw.edu.pl/ipc-2.0.1.zip"

    print("Downloading IPC 2.0 ...")
    EXTERNAL_PATH.mkdir(parents=True, exist_ok=True)
    zip_path = EXTERNAL_PATH / "ipc2.zip"
    try:
        urllib.request.urlretrieve(ipc_url, zip_path)
    except Exception as e:
        print(f"ERROR while downloading: {e}", file=sys.stderr)
        sys.exit(1)
    print("Done")

    print("Unpacking zip file ...")
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(EXTERNAL_PATH)
    except zipfile.BadZipFile as e:
        print(f"Invalid zip file: {e}", file=sys.stderr)
        sys.exit(1)
    print("Done")

    if ipc_path.exists() and ipc_path.is_dir():
        pass
    else:
        print(
            "Unexpected error: Folder 'ipc-2.0.1' could not be found.", file=sys.stderr
        )
        sys.exit(1)

    zip_path.unlink()
    print("IPC 2.0 successfully installed!")


class buildPy(_build_py):
    def run(self):
        install_ipc()
        super().run()


class install(_install):
    def run(self):
        install_ipc()
        super().run()


setup(
    cmdclass={
        "build_py": buildPy,
        "install": install,
    }
)
