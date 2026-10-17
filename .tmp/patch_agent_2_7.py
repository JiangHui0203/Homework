from pathlib import Path

DOC = Path('Agent_Knowledge_System.md')
SECTION = Path('.tmp/agent-2-7-routing-section.md')

text = DOC.read_text(encoding='utf-8')
section = SECTION.read_text(encoding='utf-8').rstrip() + '\n'

old = '### 2.7 Routing\n\n待补充。\n'
if old not in text:
    raise SystemExit('2.7 placeholder not found')
text = text.replace(old, section, 1)

old_progress = '| I | 2. Agent Decision Loop | 进行中：2.1–2.6 已完成 |'
new_progress = '| I | 2. Agent Decision Loop | 进行中：2.1–2.7 已完成 |'
if old_progress not in text:
    raise SystemExit('progress marker not found')
text = text.replace(old_progress, new_progress, 1)

old_next = '下一步：继续 **I. Model & Decision Core → 2. Agent Decision Loop → 2.7 Routing**。'
new_next = '下一步：继续 **I. Model & Decision Core → 2. Agent Decision Loop → 2.8 Agent vs Workflow**。'
if old_next not in text:
    raise SystemExit('next-step marker not found')
text = text.replace(old_next, new_next, 1)

DOC.write_text(text, encoding='utf-8')
