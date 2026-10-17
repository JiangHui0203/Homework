from pathlib import Path

p = Path("Agent_Knowledge_System.md")
s = p.read_text(encoding="utf-8")
section = Path(".tmp/agent-2-2-section.md").read_text(encoding="utf-8").rstrip() + "\n"

old = "### 2.2 Agent Loop\n\n- State\n- Decision\n- Action\n- Observation\n- Termination\n\n待补充。\n"
if old not in s:
    raise SystemExit("2.2 placeholder not found; aborting")
s = s.replace(old, section, 1)

old_progress = "| I | 2. Agent Decision Loop | 进行中：2.1 已完成 |"
new_progress = "| I | 2. Agent Decision Loop | 进行中：2.1–2.2 已完成 |"
if old_progress not in s:
    raise SystemExit("progress marker not found; aborting")
s = s.replace(old_progress, new_progress, 1)

old_next = "下一步：继续 **I. Model & Decision Core → 2. Agent Decision Loop → 2.2 Agent Loop**。"
new_next = "下一步：继续 **I. Model & Decision Core → 2. Agent Decision Loop → 2.3 ReAct**。"
if old_next not in s:
    raise SystemExit("next-step marker not found; aborting")
s = s.replace(old_next, new_next, 1)

p.write_text(s, encoding="utf-8")
