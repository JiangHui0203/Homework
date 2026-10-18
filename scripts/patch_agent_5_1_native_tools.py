from pathlib import Path
import re

DOC = Path("Agent_Knowledge_System.md")
SECTION = Path(".tmp/agent_5_1_native_tools.md")

text = DOC.read_text(encoding="utf-8")
section = SECTION.read_text(encoding="utf-8").rstrip() + "\n\n"

section_pat = re.compile(
    r"(?ms)^### 5\.1 Native Tools\s*\n.*?(?=^### 5\.2 Skills\s*$)"
)
matches = list(section_pat.finditer(text))
assert len(matches) == 1, f"expected exactly one 5.1 section, found {len(matches)}"
text = section_pat.sub(lambda m: section, text, count=1)

for line in text.splitlines():
    if "Capability Extension" in line or "Capabilities & Interoperability" in line and line.startswith("|"):
        print("DIAG:", line)

progress_pat = re.compile(r"(?m)^.*5\. Capability Extension.*$")
progress_matches = list(progress_pat.finditer(text))
assert len(progress_matches) == 1, f"expected one Chapter 5 progress row, found {len(progress_matches)}"
old_progress = progress_matches[0].group(0)
assert old_progress.startswith("|"), f"unexpected Chapter 5 progress line: {old_progress}"
text = text[:progress_matches[0].start()] + "| II | 5. Capability Extension | 进行中：5.1 已完成 |" + text[progress_matches[0].end():]

footer_old = "下一步：继续 **II. Capabilities & Interoperability → 5. Capability Extension → 5.1 Native Tools**。"
footer_new = "下一步：继续 **II. Capabilities & Interoperability → 5. Capability Extension → 5.2 Skills**。"
assert text.count(footer_old) == 1, f"expected one 5.1 footer, found {text.count(footer_old)}"
text = text.replace(footer_old, footer_new, 1)

assert "#### 5.1.88 参考资料" in text
assert "### 5.2 Skills" in text
assert "| II | 5. Capability Extension | 进行中：5.1 已完成 |" in text
assert footer_new in text

DOC.write_text(text, encoding="utf-8")
print("PATCH_OK")
