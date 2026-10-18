from pathlib import Path
import re

path = Path('Agent_Knowledge_System.md')
text = path.read_text(encoding='utf-8')
new_section = Path('tmp_agent_4_4_section.md').read_text(encoding='utf-8').rstrip('\n')

section_pattern = re.compile(r'### 4\.4 Long-term Memory\n.*?(?=\n### 4\.5 Persistence)', re.DOTALL)
matches = section_pattern.findall(text)
assert len(matches) == 1, f'expected one 4.4 section, got {len(matches)}'
text = section_pattern.sub(lambda _m: new_section, text, count=1)

progress_pattern = re.compile(r'^\|\s*II\s*\|\s*4\. Context, Memory & Retrieval\s*\|.*\|$', re.MULTILINE)
progress_matches = progress_pattern.findall(text)
assert len(progress_matches) == 1, f'expected one chapter-4 progress row, got {progress_matches}'
text = progress_pattern.sub('| II | 4. Context, Memory & Retrieval | 进行中：4.1–4.4 已完成 |', text, count=1)

footer_pattern = re.compile(r'^下一步：继续 .*4\. Context, Memory & Retrieval.*4\.4 Long-term Memory.*$', re.MULTILINE)
footer_matches = footer_pattern.findall(text)
assert len(footer_matches) == 1, f'expected one 4.4 footer, got {footer_matches}'
text = footer_pattern.sub('下一步：继续 **II. Capabilities & Interoperability → 4. Context, Memory & Retrieval → 4.5 Persistence**。', text, count=1)

path.write_text(text, encoding='utf-8')
print('PATCH_OK')
