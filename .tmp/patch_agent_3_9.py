from pathlib import Path

DOC = Path("Agent_Knowledge_System.md")
SECTION = Path(".tmp/agent-3-9-side-effects-section.md").read_text(encoding="utf-8").rstrip() + "\n"
text = DOC.read_text(encoding="utf-8")

old_section = "### 3.9 Side Effects\n\n- Idempotency\n- Confirmation\n- Irreversible actions\n"
if old_section not in text:
    raise SystemExit("3.9 placeholder not found or already replaced")
text = text.replace(old_section, SECTION, 1)

old_progress = "| II | 3. Tool Use & Action | 进行中：3.1–3.8 已完成 |"
new_progress = "| II | 3. Tool Use & Action | 已完成：3.1–3.9 |"
if old_progress not in text:
    raise SystemExit("progress marker not found")
text = text.replace(old_progress, new_progress, 1)

old_next = "下一步：继续 **II. Capabilities & Interoperability → 3. Tool Use & Action → 3.9 Side Effects**。"
new_next = "下一步：继续 **II. Capabilities & Interoperability → 4. Context, Memory & Retrieval → 4.1 Context Engineering**。"
if old_next not in text:
    raise SystemExit("next-step marker not found")
text = text.replace(old_next, new_next, 1)

DOC.write_text(text, encoding="utf-8")
