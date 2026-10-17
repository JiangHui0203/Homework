from pathlib import Path

DOC = Path('Agent_Knowledge_System.md')
SECTION = Path('.tmp/agent-3-4-tool-selection-section.md')

text = DOC.read_text(encoding='utf-8')
section = SECTION.read_text(encoding='utf-8').rstrip() + '\n\n'

old = '### 3.4 Tool Selection\n### 3.5 Argument Generation'
new = section + '### 3.5 Argument Generation'
if old not in text:
    raise SystemExit('3.4 placeholder not found or already replaced')
text = text.replace(old, new, 1)

old_progress = '| II | 3. Tool Use & Action | 进行中：3.1–3.3 已完成 |'
new_progress = '| II | 3. Tool Use & Action | 进行中：3.1–3.4 已完成 |'
if old_progress not in text:
    raise SystemExit('progress row not found')
text = text.replace(old_progress, new_progress, 1)

old_next = '下一步：继续 **II. Capabilities & Interoperability → 3. Tool Use & Action → 3.4 Tool Selection**。'
new_next = '下一步：继续 **II. Capabilities & Interoperability → 3. Tool Use & Action → 3.5 Argument Generation**。'
if old_next not in text:
    raise SystemExit('next-step footer not found')
text = text.replace(old_next, new_next, 1)

DOC.write_text(text, encoding='utf-8')
print('patched 3.4 Tool Selection')
