from pathlib import Path
import re

DOC = Path('Agent_Knowledge_System.md')
SECTION = Path('.agent_doc_staging/4_5_persistence.md')

text = DOC.read_text(encoding='utf-8')
section = SECTION.read_text(encoding='utf-8').rstrip() + '\n\n'

pattern = re.compile(r'(?ms)^### 4\.5 Persistence\n.*?(?=^### 4\.6 Retrieval\n)')
if len(pattern.findall(text)) != 1:
    raise SystemExit('expected exactly one 4.5 section')
text = pattern.sub(lambda _: section, text, count=1)

progress_pattern = re.compile(r'^\| II \| 4\. Context, Memory & Retrieval \| .*? \|$', re.M)
if len(progress_pattern.findall(text)) != 1:
    raise SystemExit('expected exactly one chapter 4 progress row')
text = progress_pattern.sub('| II | 4. Context, Memory & Retrieval | 进行中：4.1–4.5 已完成 |', text, count=1)

footer_pattern = re.compile(r'^下一步：继续 \*\*II\. Capabilities & Interoperability → 4\. Context, Memory & Retrieval → .*?\*\*。$', re.M)
if len(footer_pattern.findall(text)) != 1:
    raise SystemExit('expected exactly one next-step footer')
text = footer_pattern.sub('下一步：继续 **II. Capabilities & Interoperability → 4. Context, Memory & Retrieval → 4.6 Retrieval**。', text, count=1)

DOC.write_text(text, encoding='utf-8')
print('patched 4.5 Persistence')
