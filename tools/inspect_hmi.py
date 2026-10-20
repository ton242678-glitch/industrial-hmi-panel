"""Validate this public XJP archive as plain ZIP/JSON data. Python 3.10+."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent.parent


def walk(value):
    if isinstance(value, dict):
        yield value
        for item in value.values(): yield from walk(item)
    elif isinstance(value, list):
        for item in value: yield from walk(item)


def inspect(path):
    with ZipFile(path) as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        if len(infos) > 5000 or sum(i.file_size for i in infos) > 128 * 1024 * 1024:
            raise ValueError('Archive exceeds inspection limits')
        if len(names) != len(set(names)):
            raise ValueError('Duplicate ZIP member')
        for info in infos:
            member = PurePosixPath(info.filename.replace('\\', '/'))
            if member.is_absolute() or '..' in member.parts or ':' in member.parts[0] or info.file_size > 32 * 1024 * 1024:
                raise ValueError('Invalid ZIP member')
            if info.filename.endswith('.lock'):
                raise ValueError('Editor lock present in public archive')
        data = {name: json.loads(archive.read(name).decode('utf-8-sig')) for name in names}
    problems = []
    for name, value in data.items():
        for node in walk(value):
            for key, item in node.items():
                if isinstance(item, str) and (re.search(r'(?<!\w)[A-Za-z]:[\\/]', item) or item.startswith('\\\\')):
                    problems.append('Local path in ' + name)
                if isinstance(item, (str, int, float)) and not isinstance(item, bool) and any(t in key.lower() for t in ['pwd', 'password', 'secret', 'token']):
                    allowed = ['', 0] + (['000000'] if key == 'PreSetPwd' else [])
                    if item not in allowed:
                        problems.append('Non-demo credential in ' + name)
    pages = sorted([value for name,value in data.items() if name.startswith('PageScreens/') and 1 <= value.get('WinId',0) <= 13], key=lambda page:page['WinId'])
    if [page['WinId'] for page in pages] != list(range(1,14)):
        problems.append('Main page IDs do not match 1–13')
    alarms = sum('ReadAddress' in node and 'Res' in node for node in walk(data['PagesGroup/Pages']))
    if alarms != 14: problems.append('Unexpected alarm definition count')
    if problems: raise ValueError('; '.join(sorted(set(problems))))
    return {'file':path.name, 'sha256':hashlib.sha256(path.read_bytes()).hexdigest(), 'main_pages':len(pages), 'alarm_definitions':alarms, 'members':len(data), 'public_archive_check':'passed'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', nargs='?', type=Path, default=ROOT / 'engineering/industrial-panel-demo.xjp')
    args = parser.parse_args()
    report = inspect(args.project)
    expected = json.loads((ROOT / 'docs/project-summary.json').read_text(encoding='utf-8'))
    if report['sha256'] != expected['archive_sha256']:
        raise ValueError('Archive does not match the documented SHA-256')
    for page in expected['pages_data']:
        if not (ROOT / page['image']).is_file(): raise ValueError('Missing preview image')
    print(json.dumps(report))
