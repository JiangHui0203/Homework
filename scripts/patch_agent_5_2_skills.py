from pathlib import Path
import re

DOC = Path("Agent_Knowledge_System.md")
SECTION = Path(".tmp/agent_5_2_skills.md")

text = DOC.read_text(encoding="utf-8")
section = SECTION.read_text(encoding="utf-8").rstrip() + "\n\n"

section_pat = re.compile(r"(?ms)^### 5\.2 Skills\s*\n.*?(?=^### 5\.3 MCP\s*$)")
matches = list(section_pat.finditer(text))
assert len(matches) == 1, f"expected exactly one 5.2 section, found {len(matches)}"
text = section_pat.sub(lambda m: section, text, count=1)

progress_pat = re.compile(r"(?m)^\| II \| 5\. Capability Extension & Protocols \|.*\|$")
progress_matches = list(progress_pat.finditer(text))
assert len(progress_matches) == 1, f"expected one Chapter 5 progress row, found {len(progress_matches)}"
text = progress_pat.sub("| II | 5. Capability Extension & Protocols | 进行中：5.1–5.2 已完成 |", text, count=1)

footer_pat = re.compile(r"(?m)^下一步：继续 \*\*II\. Capabilities & Interoperability → 5\.[^\n]*→ 5\.2 Skills\*\*。$")
footer_matches = list(footer_pat.finditer(text))
assert len(footer_matches) == 1, f"expected one 5.2 footer, found {len(footer_matches)}"
text = footer_pat.sub("下一步：继续 **II. Capabilities & Interoperability → 5. Capability Extension → 5.3 MCP**。", text, count=1)

assert "#### 5.2.125 参考资料" in text
assert "### 5.3 MCP" in text
assert "| II | 5. Capability Extension & Protocols | 进行中：5.1–5.2 已完成 |" in text
assert "→ 5.3 MCP**。" in text

DOC.write_text(text, encoding="utf-8")
print("PATCH_OK")
