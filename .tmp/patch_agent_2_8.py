from pathlib import Path

DOC = Path("Agent_Knowledge_System.md")
SECTION = Path(".tmp/agent-2-8-agent-vs-workflow-section.md")

text = DOC.read_text(encoding="utf-8")
section = SECTION.read_text(encoding="utf-8").rstrip() + "\n"

placeholder = "### 2.8 Agent vs Workflow\n\n待补充。"
if placeholder not in text:
    raise SystemExit("2.8 placeholder not found")
text = text.replace(placeholder, section.rstrip(), 1)

old_progress = "| I | 2. Agent Decision Loop | 进行中：2.1–2.7 已完成 |"
new_progress = "| I | 2. Agent Decision Loop | 已完成：2.1–2.8 |"
if old_progress not in text:
    raise SystemExit("progress marker not found")
text = text.replace(old_progress, new_progress, 1)

old_next = "下一步：继续 **I. Model & Decision Core → 2. Agent Decision Loop → 2.8 Agent vs Workflow**。"
new_next = "下一步：进入 **II. Capabilities & Interoperability → 3. Tool Use & Action → 3.1 Tool Definition**。"
if old_next not in text:
    raise SystemExit("next-step marker not found")
text = text.replace(old_next, new_next, 1)

DOC.write_text(text, encoding="utf-8")
