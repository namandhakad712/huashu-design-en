#!/usr/bin/env python3
"""
learn.py — lets huashu-design know this user a little better with every project it does.

Experience comes in two layers:
  Shipped with the skill   references/experience.md — general findings (reproduced across two projects or measured), true for everyone;
                           edited by hand in the repo; this command never writes it.
  Private to this machine  ~/.huashu-design/experience.md (HUASHU_DESIGN_HOME can relocate it) — this machine's user:
                           their verbatim quotes, their taste, observations seen in only one project. Never distributed.

Usage:
  python3 scripts/learn.py [topics…]            before starting: this user's preferences + experience relevant to the topics
  python3 scripts/learn.py add "…" --kind preference|observed|verified|superseded \
          --topics deck,color --evidence "verbatim quote/project/file/measurement" [--do "what to do next time"] [--project name]
  python3 scripts/learn.py harvest <project dir>   after wrapping up: list what in the project can serve as evidence, plus the bar for what deserves recording
  python3 scripts/learn.py status
  python3 scripts/learn.py -- status            when a topic word happens to be add/harvest/status, separate it with --

Ported from huashu-motion's `om learn` (same author, MIT), with the dependency on studio comments removed.
"""

import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

KINDS = {
    'preference': 'said by the user in their own words — must quote them verbatim; holds for this user until they say otherwise',
    'observed': 'seen in only one project — a clue, not a rule',
    'verified': 'reproduced in two or more projects, or measured — the general ones eventually land in references/experience.md',
    'superseded': 'no longer true — keep the entry, state clearly what superseded it',
}

SKILL_ROOT = Path(__file__).resolve().parent.parent
SHIPPED = SKILL_ROOT / 'references' / 'experience.md'

HEAD = """# Experience on this machine (huashu-design)

What projects on this machine have taught us. Written by `learn.py add`; hand edits are fine too: if an entry is wrong, fix it in place,
and when it stops holding, change its kind to superseded and say why. Not distributed with the skill.
"""


def home() -> Path:
    return Path(os.environ.get('HUASHU_DESIGN_HOME') or Path.home() / '.huashu-design')


def local_file() -> Path:
    return home() / 'experience.md'


class LearnError(Exception):
    pass


def entries(path: Path, layer: str):
    """In the markdown file, each "## …" heading plus its body is one entry."""
    if not path.exists():
        return []
    out = []
    for block in re.split(r'\n(?=## )', path.read_text(encoding='utf-8')):
        if not block.startswith('## '):
            continue
        head = block.split('\n', 1)[0][3:].strip()
        m = re.search(r'·\s*(preference|observed|verified|superseded)\b', head)   # still recognized when a hand edit dropped the closing "·"
        kind = m.group(1) if m else ('shipped' if layer == 'shipped' else 'observed')
        t = re.search(r'topics?:\s*([^\n·]+)', head, re.I)
        tags = [x for x in re.split(r'[,，\s]+', t.group(1) if t else '') if x]
        idm = re.match(r'(L\d+)', head)
        out.append({'layer': layer, 'head': head, 'kind': kind, 'tags': tags,
                    'body': block.strip(), 'id': idm.group(1) if idm else None})
    return out


def recall(topics):
    want = [t.lower() for t in topics]

    def match(e):
        return not want or any(t in [x.lower() for x in e['tags']] or t in e['body'].lower() for t in want)

    local = entries(local_file(), 'local')
    shipped = entries(SHIPPED, 'shipped')
    prefs = [e for e in local if e['kind'] == 'preference']
    rest = [e for e in local if e['kind'] not in ('preference', 'superseded') and match(e)] + \
           [e for e in shipped if match(e)]
    on = f' ({", ".join(want)})' if want else ''
    parts = []
    if prefs:
        parts.append(f"## This user's preferences ({len(prefs)} entries) — their verbatim words, holding until they say otherwise. "
                     f'Note: preferences have a scope. One stated as only for a certain kind of deliverable must not spill over into a default for all designs\n\n'
                     + '\n\n'.join(e['body'] for e in prefs))
    else:
        parts.append(f"## This user's preferences: nothing recorded yet ({local_file()})")
    if rest:
        parts.append(f'## Experience from past projects{on} ({len(rest)} entries) — when the project at hand conflicts with an entry, the project wins; then go update the entry\n\n'
                     + '\n\n'.join(('[this machine] ' if e['layer'] == 'local' else '') + e['body'] for e in rest))
    else:
        parts.append(f'## Experience from past projects{on}: no matches')
    return '\n\n'.join(parts)


def add_entry(kind, topics, text, evidence, todo=None, project=None):
    if kind not in KINDS:
        raise LearnError('learn.py add needs --kind ' + '|'.join(KINDS) + '\n' +
                         '\n'.join(f'  {k:<11} {v}' for k, v in KINDS.items()))
    tags = [x for x in re.split(r'[,，\s]+', topics or '') if x]
    if not tags:
        raise LearnError('learn.py add needs --topics (e.g. deck,color,direction), otherwise it can never be found again')
    if not (text or '').strip():
        raise LearnError('learn.py add needs the finding written out as text: learn.py add "…" --kind … --topics … --evidence …')
    if not (evidence or '').strip():
        raise LearnError('learn.py add needs --evidence: a verbatim quote, a project and file, a measurement — an entry nobody can verify is only hearsay')
    if kind == 'preference' and not re.search(r'[「“"]', text):
        raise LearnError('preference must quote the user verbatim: wrap it in 「…」 or "…"')
    f = local_file()
    f.parent.mkdir(parents=True, exist_ok=True)
    prev = f.read_text(encoding='utf-8') if f.exists() else HEAD
    n = 1 + max([0] + [int(e['id'][1:]) for e in entries(f, 'local') if e['id']])
    block = [f'## L{n} · {date.today().isoformat()} · {kind} · topics: {", ".join(tags)}', '',
             f'- {"Verbatim quote" if kind == "preference" else "Finding"}: {text.strip()}']
    if todo:
        block.append(f'- Next time: {todo.strip()}')
    block.append(f'- Evidence: {evidence.strip()}' + (f' ({project})' if project else ''))
    f.write_text(prev.rstrip() + '\n\n' + '\n'.join(block) + '\n', encoding='utf-8')
    return f'Recorded  L{n} → {f}'


def harvest(project: Path):
    if not project.is_dir():
        raise LearnError(f'Not a directory: {project}')
    lines = [f'Harvest  {project}']
    approved = project / 'direction-approved.md'
    if approved.exists():
        lines += ['', 'direction-approved.md (which of the three directions they picked and how they put it — the most direct evidence of taste):',
                  approved.read_text(encoding='utf-8').strip()[:3000]]
    directions = project / 'directions.md'
    if directions.exists():
        lines += ['', f'directions.md at: {directions} (direction cards; against their picks, see which logic and what intensity they lean toward, not just which colors)']
    demos = sorted((project / 'design-demos').glob('dir-*.html')) if (project / 'design-demos').is_dir() else []
    if demos:
        lines.append(f'design-demos: {len(demos)} complete directions' + (' (thumbnails in thumbs.html too)' if (project / 'design-demos' / 'thumbs.html').exists() else ''))
    ledger = home() / 'ledger.jsonl'
    if ledger.exists():
        mine = [l for l in ledger.read_text(encoding='utf-8').splitlines()
                if l.strip() and json.loads(l).get('project_dir') == str(project.resolve())]
        lines.append(f'Look ledger: {len(mine)} entries for this project' + ('' if mine else ' — delivered but no entries recorded? Run design_lint.py ledger add'))
    lines += ['', 'Then dig out what the user said during the conversation — quote it verbatim.', '',
              'Record only when all three hold at once: not obvious; saves time or avoids detours on the next project; this project produced evidence. Then, in order:',
              '  1. Does some entry say the opposite? Fix that entry first (learn.py will list them; edit the file directly).',
              "  2. Can a tool catch it (a design_lint.py check)? Change the tool and its tests rather than writing it down.",
              '  3. Otherwise: learn.py add "…" --kind preference|observed --topics … --evidence "…" [--do "…"].',
              '     Their verbatim words are a preference, with its scope spelled out ("only for their own covers"); what you saw once in one project is observed.',
              "  4. Seen in two projects, or measured, and true for anyone (not only this user's taste)? On the dev machine,",
              '     write it into references/experience.md shipped with the skill; fold the settled parts into the reference it belongs to.',
              f'Experience on this machine: {local_file()}']
    return '\n'.join(lines)


def status():
    f = local_file()
    local = entries(f, 'local')
    shipped = entries(SHIPPED, 'shipped')
    by = {k: sum(1 for e in local if e['kind'] == k) for k in KINDS}
    s = (f'On this machine: {f}' + (f' ({len(local)} entries: {by["preference"]} preferences, {by["observed"]} observed, '
                                    f'{by["verified"]} verified, {by["superseded"]} superseded)' if f.exists() else ' (none yet)'))
    return s + f'\nShipped with the skill: {len(shipped)} entries, in references/experience.md'


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):   # the Windows console is not UTF-8 by default
        try:
            stream.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        if argv and argv[0] == '--':
            print(recall(argv[1:]))
        elif argv and argv[0] == 'add':
            p = argparse.ArgumentParser(prog='learn.py add')
            p.add_argument('text')
            p.add_argument('--kind', required=True)
            p.add_argument('--topics', required=True)
            p.add_argument('--evidence', default='')
            p.add_argument('--do', dest='todo')
            p.add_argument('--project')
            a = p.parse_args(argv[1:])
            print(add_entry(a.kind, a.topics, a.text, a.evidence, a.todo, a.project))
        elif argv and argv[0] == 'harvest':
            if len(argv) < 2:
                raise LearnError('Usage: learn.py harvest <project directory>')
            print(harvest(Path(argv[1])))
        elif argv and argv[0] == 'status':
            print(status())
        else:
            print(recall(argv))
    except LearnError as e:
        print(str(e), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
