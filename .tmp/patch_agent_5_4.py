from pathlib import Path
import re

DOC = Path('Agent_Knowledge_System.md')
SECTION = Path('.tmp/agent-5-4-capability-discovery-section.md')

text = DOC.read_text(encoding='utf-8')
section = SECTION.read_text(encoding='utf-8').rstrip() + '\n\n'

# Replace the complete 5.4 placeholder/body up to the next top-level chapter.
pattern = re.compile(r'(?ms)^### 5\.4 Capability Discovery\s*\n.*?(?=^## 6\.)')
matches = list(pattern.finditer(text))
if len(matches) != 1:
    raise SystemExit(f'expected exactly one 5.4 section, found {len(matches)}')
text = pattern.sub(lambda m: '### 5.4 Capability Discovery\n\n' + section, text, count=1)

# Mark Chapter 5 complete without depending on the previous status wording.
progress_pattern = re.compile(r'(?m)^\| II \| 5\. Capability Extension & Protocols \|.*\|$')
progress_matches = list(progress_pattern.finditer(text))
if len(progress_matches) != 1:
    raise SystemExit(f'expected exactly one Chapter 5 progress row, found {len(progress_matches)}')
text = progress_pattern.sub('| II | 5. Capability Extension & Protocols | 已完成：5.1–5.4 |', text, count=1)

# Derive the exact next heading from the document itself.
chapter6 = re.search(r'(?m)^## (6\.[^\n]+)$', text)
sec61 = re.search(r'(?m)^### (6\.1[^\n]*)$', text)
if not chapter6 or not sec61:
    raise SystemExit('could not derive Chapter 6 / 6.1 headings')

footer_pattern = re.compile(r'(?m)^下一步：继续 \*\*II\. Capabilities & Interoperability → 5\. Capability Extension & Protocols → 5\.4 Capability Discovery\*\*。$')
footer_matches = list(footer_pattern.finditer(text))
if len(footer_matches) != 1:
    raise SystemExit(f'expected exactly one 5.4 next-step footer, found {len(footer_matches)}')
new_footer = f'下一步：继续 **II. Capabilities & Interoperability → {chapter6.group(1)} → {sec61.group(1)}**。'
text = footer_pattern.sub(new_footer, text, count=1)

DOC.write_text(text, encoding='utf-8')
print('PATCH_OK')
print(new_footer)
