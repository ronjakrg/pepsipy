import sys
import zipfile
import urllib.request

from peptidefeatures.constants import AA_LETTERS, EXTERNAL_PATH


def sanitize_sequence(seq: str) -> str:
    """
    Converts all letters to upper case and removes any character that
    does not represent an amino acid according to IUPAC-IUB standard.
    """
    seq = seq.upper()
    return "".join(res for res in seq if res in AA_LETTERS)


def get_group(name: str, groups: list) -> str:
    """
    Returns the group that is found in the prefix of the sample name.
    If no group was found, "None" will be returned.
    """
    return next((g for g in groups if name.startswith(g)), "None")


def install_ipc():
    """
    Downloads and installs IPC 2.0 in /external/ipc-2.0.1 if it doesn't exist yet.
    """
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
        print("Unexpected error: Folder 'ipc-2.0.1' could not be found.", file=sys.stderr)
        sys.exit(1)
    
    zip_path.unlink()
    print("IPC 2.0 successfully installed!")