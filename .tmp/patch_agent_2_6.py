from pathlib import Path

path = Path("Agent_Knowledge_System.md")
section_path = Path(".tmp/agent-2-6-verification-section.md")
text = path.read_text(encoding="utf-8")
section = section_path.read_text(encoding="utf-8").rstrip()

old = "### 2.6 Verification\n\n待补充。\n\n### 2.7 Routing"
if text.count(old) != 1:
    raise RuntimeError(f"expected one 2.6 placeholder, found {text.count(old)}")
text = text.replace(old, section, 1)

old_progress = "| I | 2. Agent Decision Loop | 进行中：2.1–2.5 已完成 |"
new_progress = "| I | 2. Agent Decision Loop | 进行中：2.1–2.6 已完成 |"
if text.count(old_progress) != 1:
    raise RuntimeError("progress marker mismatch")
text = text.replace(old_progress, new_progress, 1)

old_next = "下一步：继续 **I. Model & Decision Core → 2. Agent Decision Loop → 2.6 Verification**。"
new_next = "下一步：继续 **I. Model & Decision Core → 2. Agent Decision Loop → 2.7 Routing**。"
if text.count(old_next) != 1:
    raise RuntimeError("next-step marker mismatch")
text = text.replace(old_next, new_next, 1)

path.write_text(text, encoding="utf-8")
