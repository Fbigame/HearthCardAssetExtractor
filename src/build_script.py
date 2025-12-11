import os
import subprocess
import sys
from pathlib import Path


def build():
    project_root = Path(__file__).resolve().parent.parent
    entry = project_root / "src" / "cli.py"
    os.chdir(project_root)
    
    # 虚拟环境的 Python
    python_exe = Path(sys.executable)
    
    # Nuitka 打包参数
    output_dir = project_root / 'dist'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        python_exe.as_posix(),
        "-m", "nuitka",
        "--standalone",
        "--onefile",
        "--follow-imports",
        "--include-package=UnityPy.resources",
        "--onefile-tempdir-spec={CACHE_DIR}/hearthstone-card-asset-extractor",
        "--user-package-configuration-file=card-asset.nuitka-package.config.yml",
        "--output-dir=" + output_dir.as_posix(),
        "--output-filename=card-asset",
        entry.as_posix()
    ]
    
    subprocess.check_call(cmd)


if __name__ == "__main__":
    build()
