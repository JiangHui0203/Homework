from pathlib import Path
import re

DOC = Path('Agent_Knowledge_System.md')
SECTION = Path('.tmp/agent-6-2-orchestration-patterns-section.md')

text = DOC.read_text(encoding='utf-8')
section = SECTION.read_text(encoding='utf-8').rstrip() + '\n\n'

# Preserve the exact existing 6.2 heading and replace only its body up to 6.3.
pattern = re.compile(r'(?ms)^(### 6\.2[^\n]*\n).*?(?=^### 6\.3)')
matches = list(pattern.finditer(text))
if len(matches) != 1:
    raise SystemExit(f'expected exactly one 6.2 section, found {len(matches)}')
heading = matches[0].group(1)
text = pattern.sub(lambda m: heading + '\n' + section, text, count=1)

# Update Chapter 6 progress while preserving the exact chapter title used by the document.
chapter6 = re.search(r'(?m)^## (6\.[^\n]+)$', text)
if not chapter6:
    raise SystemExit('could not derive Chapter 6 heading')
progress_pattern = re.compile(r'(?m)^\| II \| 6\.[^|]+\| 进行中：6\.1 已完成 \|$')
progress_matches = list(progress_pattern.finditer(text))
if len(progress_matches) != 1:
    raise SystemExit(f'expected exactly one Chapter 6 progress row at 6.1-complete state, found {len(progress_matches)}')
chapter6_label = chapter6.group(1)
text = progress_pattern.sub(f'| II | {chapter6_label} | 进行中：6.1–6.2 已完成 |', text, count=1)

# Derive the exact 6.3 heading for the next-step pointer.
sec63 = re.search(r'(?m)^### (6\.3[^\n]*)$', text)
if not sec63:
    raise SystemExit('could not derive 6.3 heading')

# Replace only the current next-step line that points to 6.2.
footer_pattern = re.compile(r'(?m)^下一步：继续 .*6\.2[^\n]*$')
footer_matches = list(footer_pattern.finditer(text))
if len(footer_matches) != 1:
    raise SystemExit(f'expected exactly one 6.2 next-step footer, found {len(footer_matches)}')
new_footer = f'下一步：继续 **II. Capabilities & Interoperability → {chapter6_label} → {sec63.group(1)}**。'
text = footer_pattern.sub(new_footer, text, count=1)

DOC.write_text(text, encoding='utf-8')
print('PATCH_OK')
print(heading.strip())
print(new_footer)
