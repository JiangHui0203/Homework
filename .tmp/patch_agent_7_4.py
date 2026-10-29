from pathlib import Path
import re

DOC = Path('Agent_Knowledge_System.md')
SECTION = Path('.tmp/agent-7-4-context-policy-section.md')

text = DOC.read_text(encoding='utf-8')
section = SECTION.read_text(encoding='utf-8').rstrip() + '\n\n'

# Preserve the exact existing 7.4 heading and replace only its body up to 7.5.
pattern = re.compile(r'(?ms)^(### 7\.4[^\n]*\n).*?(?=^### 7\.5)')
matches = list(pattern.finditer(text))
if len(matches) != 1:
    raise SystemExit(f'expected exactly one 7.4 section, found {len(matches)}')
heading = matches[0].group(1)
text = pattern.sub(lambda m: heading + '\n' + section, text, count=1)

# Update Chapter 7 progress while preserving phase/chapter labels already used by the document.
chapter7 = re.search(r'(?m)^## (7\.[^\n]+)$', text)
if not chapter7:
    raise SystemExit('could not derive Chapter 7 heading')
progress_pattern = re.compile(r'(?m)^\| ([^|]+) \| (7\.[^|]+) \|.*\|$')
progress_matches = list(progress_pattern.finditer(text))
if len(progress_matches) != 1:
    raise SystemExit(f'expected exactly one Chapter 7 progress row, found {len(progress_matches)}')
phase = progress_matches[0].group(1).strip()
chapter_label = progress_matches[0].group(2).strip()
text = progress_pattern.sub(f'| {phase} | {chapter_label} | 进行中：7.1–7.4 已完成 |', text, count=1)

# Derive the exact 7.5 heading for the next-step pointer.
sec75 = re.search(r'(?m)^### (7\.5[^\n]*)$', text)
if not sec75:
    raise SystemExit('could not derive 7.5 heading')

# Match the single canonical next-step line containing the current breakpoint, regardless of older wording style.
footer_pattern = re.compile(r'(?m)^.*下一步.*7\.4[^\n]*$')
footer_matches = list(footer_pattern.finditer(text))
if len(footer_matches) != 1:
    raise SystemExit(f'expected exactly one 7.4 next-step footer, found {len(footer_matches)}')
new_footer = f'下一步：继续 **{phase}. Harness & Agent System → {chapter_label} → {sec75.group(1)}**。'
text = footer_pattern.sub(new_footer, text, count=1)

DOC.write_text(text, encoding='utf-8')
print('PATCH_OK')
print(heading.strip())
print(new_footer)
