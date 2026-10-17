from pathlib import Path

DOC = Path("Agent_Knowledge_System.md")
SECTION = Path(".tmp/agent-3-7-observation-section.md").read_text(encoding="utf-8").rstrip() + "\n"
text = DOC.read_text(encoding="utf-8")

old_section = "### 3.7 Observation\n### 3.8 Failure Handling"
new_section = SECTION + "### 3.8 Failure Handling"
if old_section not in text:
    raise SystemExit("3.7 placeholder not found or already replaced")
text = text.replace(old_section, new_section, 1)

old_progress = "| II | 3. Tool Use & Action | 进行中：3.1–3.6 已完成 |"
new_progress = "| II | 3. Tool Use & Action | 进行中：3.1–3.7 已完成 |"
if old_progress not in text:
    raise SystemExit("progress marker not found")
text = text.replace(old_progress, new_progress, 1)

old_next = "下一步：继续 **II. Capabilities & Interoperability → 3. Tool Use & Action → 3.7 Observation**。"
new_next = "下一步：继续 **II. Capabilities & Interoperability → 3. Tool Use & Action → 3.8 Failure Handling**。"
if old_next not in text:
    raise SystemExit("next-step marker not found")
text = text.replace(old_next, new_next, 1)

DOC.write_text(text, encoding="utf-8")
