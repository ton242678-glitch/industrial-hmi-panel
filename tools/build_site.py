"""Build the static gallery without publishing engineering files as a website."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent.parent
out = root / 'site'
out.mkdir(exist_ok=True)
shutil.copy2(root / 'index.html', out / 'index.html')
shutil.copytree(root / 'assets', out / 'assets', dirs_exist_ok=True)
shutil.copytree(root / 'docs/images', out / 'docs/images', dirs_exist_ok=True)
(out / '.nojekyll').touch()
print('Static gallery built in site/')
