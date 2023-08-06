import gnote
from loguru import logger
from pathlib import Path
from typing import List, Dict
import subprocess

from rich.console import Console
from gnote import repo_dir
import platform

console = Console()
root = Path(repo_dir)
cmd = ['powershell'] if 'windows' == platform.system().lower() else []


def list_note() -> Dict[str, Path]:
    paths: List[Path] = []

    def recursion_file(p: Path):
        for sub in p.iterdir():
            if sub.name.startswith('.'):
                continue
            if sub.is_dir():
                recursion_file(sub)
            else:
                paths.append(sub)

    recursion_file(gnote.repo_dir)
    return {p.name.rsplit('.md')[0]: p for p in paths}


def code(name):
    if name == '.':
        subprocess.call(cmd + (['code', '-w', root]))
    else:
        dct = list_note()
        new_p = root / name
        new_p = new_p.with_suffix('.md')
        p = dct.get(name, new_p)
        subprocess.call(cmd + (['code', '-w', p]))
    # 自动提交到远程
    g = gnote.git_repo.git
    g.add('.')
    g.commit(m='update')
    g.push()
