from pathlib import Path

repo = Path('.')
doc_path = repo / 'Agent_Knowledge_System.md'
section_path = repo / '.tmp/agent-3-2-tool-schema-section.md'

text = doc_path.read_text(encoding='utf-8')
section = section_path.read_text(encoding='utf-8').rstrip()

old = '### 3.2 Tool Schema\n### 3.3 Tool Description'
new = section + '\n\n### 3.3 Tool Description'
if old not in text:
    raise SystemExit('3.2 placeholder not found or already replaced')
text = text.replace(old, new, 1)

old_progress = '| II | 3. Tool Use & Action | 进行中：3.1 已完成 |'
new_progress = '| II | 3. Tool Use & Action | 进行中：3.1–3.2 已完成 |'
if old_progress not in text:
    raise SystemExit('progress marker not found')
text = text.replace(old_progress, new_progress, 1)

old_next = '下一步：继续 **II. Capabilities & Interoperability → 3. Tool Use & Action → 3.2 Tool Schema**。'
new_next = '下一步：继续 **II. Capabilities & Interoperability → 3. Tool Use & Action → 3.3 Tool Description**。'
if old_next not in text:
    raise SystemExit('next-step marker not found')
text = text.replace(old_next, new_next, 1)

doc_path.write_text(text, encoding='utf-8')
