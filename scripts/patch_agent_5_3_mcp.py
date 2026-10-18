from pathlib import Path
import re

DOC = Path("Agent_Knowledge_System.md")
SECTION = Path(".tmp/agent_5_3_mcp.md")

text = DOC.read_text(encoding="utf-8")
section = SECTION.read_text(encoding="utf-8").rstrip() + "\n\n"

section_pat = re.compile(
    r"(?ms)^### 5\.3 MCP\s*\n.*?(?=^### 5\.4 Capability Discovery\s*$)"
)
section_matches = list(section_pat.finditer(text))
assert len(section_matches) == 1, f"expected exactly one 5.3 section, found {len(section_matches)}"
text = section_pat.sub(lambda m: section, text, count=1)

old_progress = "| II | 5. Capability Extension & Protocols | 进行中：5.1–5.2 已完成 |"
new_progress = "| II | 5. Capability Extension & Protocols | 进行中：5.1–5.3 已完成 |"
assert text.count(old_progress) == 1, f"expected one old progress row, found {text.count(old_progress)}"
text = text.replace(old_progress, new_progress, 1)

footer_old = "下一步：继续 **II. Capabilities & Interoperability → 5. Capability Extension → 5.3 MCP**。"
footer_new = "下一步：继续 **II. Capabilities & Interoperability → 5. Capability Extension → 5.4 Capability Discovery**。"
assert text.count(footer_old) == 1, f"expected one 5.3 footer, found {text.count(footer_old)}"
text = text.replace(footer_old, footer_new, 1)

assert "#### 5.3.215 参考资料" in text
assert "### 5.4 Capability Discovery" in text
assert new_progress in text
assert footer_new in text

DOC.write_text(text, encoding="utf-8")
print("PATCH_OK")
