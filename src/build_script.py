import subprocess


def build():
    subprocess.check_call(["pyinstaller", "hearth-card-asset.spec"])
