set -e
IPC_DIR="external/ipc-2.0.1"
echo "Checking if IPC 2.0 is installed ..."
if [ -d "$IPC_DIR" ]; then
    echo "IPC 2.0 is already installed."
    exit 0
fi
echo "Downloading IPC 2.0 ..."
mkdir -p external
cd external
wget -O ipc2.zip https://ipc2.mimuw.edu.pl/ipc-2.0.1.zip
upzip ipc2.zip
rm ipc2.zip
echo "IPC 2.0 successfully installed."