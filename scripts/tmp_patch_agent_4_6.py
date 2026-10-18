from pathlib import Path
import re

DOC = Path('Agent_Knowledge_System.md')
SECTION = Path('tmp_agent_4_6_section.md')
text = DOC.read_text(encoding='utf-8')
section = SECTION.read_text(encoding='utf-8').rstrip() + '\n\n'

# Replace the entire 4.6 section up to Chapter 5.
pat = re.compile(r'^### 4\.6 Retrieval\s*.*?(?=^## 5\.)', re.M | re.S)
new_text, n = pat.subn(lambda m: section, text)
assert n == 1, f'expected exactly one 4.6 section, got {n}'
text = new_text

# Mark Chapter 4 complete regardless of the exact prior progress wording.
progress_pat = re.compile(r'^\| II \| 4\. Context, Memory & Retrieval \|.*?\|$', re.M)
new_text, n = progress_pat.subn('| II | 4. Context, Memory & Retrieval | 已完成：4.1–4.6 |', text)
assert n == 1, f'expected exactly one Chapter 4 progress row, got {n}'
text = new_text

# Advance footer from 4.6 to 5.1, allowing minor wording variation in the existing footer.
footer_pat = re.compile(r'^下一步：继续 \*\*II\. Capabilities & Interoperability → 4\. Context, Memory & Retrieval → 4\.6 Retrieval\*\*。$', re.M)
new_text, n = footer_pat.subn('下一步：继续 **II. Capabilities & Interoperability → 5. Capability Extension → 5.1 Native Tools**。', text)
if n == 0:
    # Fallback: replace any current "下一步" line that still points to 4.6 Retrieval.
    footer_pat2 = re.compile(r'^下一步：.*4\.6 Retrieval.*$', re.M)
    new_text, n = footer_pat2.subn('下一步：继续 **II. Capabilities & Interoperability → 5. Capability Extension → 5.1 Native Tools**。', text)
assert n == 1, f'expected exactly one footer update, got {n}'
text = new_text

DOC.write_text(text, encoding='utf-8')

# Self-checks.
checks = [
    '#### 4.6.1 定义：Retrieval 到底是什么？',
    '#### 4.6.233 参考资料',
    '| II | 4. Context, Memory & Retrieval | 已完成：4.1–4.6 |',
    '下一步：继续 **II. Capabilities & Interoperability → 5. Capability Extension → 5.1 Native Tools**。',
]
final = DOC.read_text(encoding='utf-8')
for c in checks:
    assert c in final, f'missing check: {c}'
print('PATCH_OK')
