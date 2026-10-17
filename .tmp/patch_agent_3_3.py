from pathlib import Path
import re

DOC = Path("Agent_Knowledge_System.md")
SECTION = Path(".tmp/agent-3-3-tool-description-section.md")

text = DOC.read_text(encoding="utf-8")
section = SECTION.read_text(encoding="utf-8").rstrip()

marker = re.compile(r"### 3\.3 Tool Description\s*### 3\.4 Tool Selection")
if marker.search(text):
    text = marker.sub(section + "\n\n### 3.4 Tool Selection", text, count=1)
elif "#### 3.3.1 定义：Tool Description 到底是什么？" not in text:
    raise RuntimeError("Could not find the 3.3 placeholder and section is not already present")

old_progress = "| II | 3. Tool Use & Action | 进行中：3.1–3.2 已完成 |"
new_progress = "| II | 3. Tool Use & Action | 进行中：3.1–3.3 已完成 |"
if old_progress in text:
    text = text.replace(old_progress, new_progress, 1)
elif new_progress not in text:
    raise RuntimeError("Could not update progress row")

old_next = "下一步：继续 **II. Capabilities & Interoperability → 3. Tool Use & Action → 3.3 Tool Description**。"
new_next = "下一步：继续 **II. Capabilities & Interoperability → 3. Tool Use & Action → 3.4 Tool Selection**。"
if old_next in text:
    text = text.replace(old_next, new_next, 1)
elif new_next not in text:
    raise RuntimeError("Could not update next-step footer")

DOC.write_text(text, encoding="utf-8")
print("PATCH_OK")
