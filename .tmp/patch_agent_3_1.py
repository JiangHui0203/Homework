from pathlib import Path

DOC = Path("Agent_Knowledge_System.md")
SECTION = Path(".tmp/agent-3-1-tool-definition-section.md")

text = DOC.read_text(encoding="utf-8")
section = SECTION.read_text(encoding="utf-8").rstrip()

old_section = "### 3.1 Tool Definition\n### 3.2 Tool Schema"
if old_section not in text:
    raise SystemExit("3.1 placeholder not found")
text = text.replace(old_section, section + "\n\n### 3.2 Tool Schema", 1)

old_progress = "| II | 3. Tool Use & Action | 待写 |"
new_progress = "| II | 3. Tool Use & Action | 进行中：3.1 已完成 |"
if old_progress not in text:
    raise SystemExit("progress row not found")
text = text.replace(old_progress, new_progress, 1)

old_next = "下一步：进入 **II. Capabilities & Interoperability → 3. Tool Use & Action → 3.1 Tool Definition**。"
new_next = "下一步：继续 **II. Capabilities & Interoperability → 3. Tool Use & Action → 3.2 Tool Schema**。"
if old_next not in text:
    raise SystemExit("next-step marker not found")
text = text.replace(old_next, new_next, 1)

DOC.write_text(text, encoding="utf-8")
