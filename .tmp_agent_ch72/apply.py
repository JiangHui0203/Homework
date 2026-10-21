from pathlib import Path

DOC = Path("Agent_Knowledge_System.md")
PART_DIR = Path(".tmp_agent_ch72")

text = DOC.read_text(encoding="utf-8")
section = "".join((PART_DIR / f"part{i}.md").read_text(encoding="utf-8") for i in range(1, 4))

# Preserve the canonical Chapter 7 skeleton already defined on main.
wrong_boundary = "7.8 Model Routing Policy\n    → 当前 transition 使用哪个模型 / 配置"
right_boundary = "7.8 Subagent Policy\n    → 何时 delegation、如何给 context / permission / budget / return contract"
if section.count(wrong_boundary) != 1:
    raise SystemExit(f"GUARD_FAIL staged 7.8 boundary: expected 1, got {section.count(wrong_boundary)}")
section = section.replace(wrong_boundary, right_boundary, 1)

old_marker = "### 7.2 Agent Loop Policy\n### 7.3 Instruction Policy"
new_marker = section + "### 7.3 Instruction Policy"

old_progress_7 = "| III | 7. Agent Harness | 进行中：7.1 已完成；下一节 7.2 Agent Loop Policy |"
new_progress_7 = "| III | 7. Agent Harness | 进行中：7.1–7.2 已完成；下一节 7.3 Instruction Policy |"

old_pending = "### 7.10 Termination Policy\n### 7.11 Recovery Policy\n\n7.2–7.11 待补充。"
new_pending = "### 7.10 Termination Policy\n### 7.11 Recovery Policy\n\n7.3–7.11 待补充。"

checks = {
    "7.2-to-7.3 marker": text.count(old_marker),
    "chapter 7 progress pointer": text.count(old_progress_7),
    "chapter 7 pending marker": text.count(old_pending),
    "7.1 final reference heading": text.count("#### 7.1.84 参考资料"),
    "7.2 heading before patch": text.count("### 7.2 Agent Loop Policy"),
    "7.3 heading before patch": text.count("### 7.3 Instruction Policy"),
}
for name, count in checks.items():
    if count != 1:
        raise SystemExit(f"GUARD_FAIL {name}: expected 1, got {count}")

if not section.startswith("### 7.2 Agent Loop Policy\n"):
    raise SystemExit("GUARD_FAIL staged section missing expected heading")
if not section.rstrip().endswith("---"):
    raise SystemExit("GUARD_FAIL staged section missing closing separator")
if "7.8 Model Routing Policy" in section:
    raise SystemExit("GUARD_FAIL stale non-canonical 7.8 name remains")
if section.count("#### 7.2.71 参考资料") != 1:
    raise SystemExit("GUARD_FAIL final 7.2 reference heading")

patched = text.replace(old_marker, new_marker, 1)
patched = patched.replace(old_progress_7, new_progress_7, 1)
patched = patched.replace(old_pending, new_pending, 1)

post_checks = {
    "7.2 heading after patch": patched.count("### 7.2 Agent Loop Policy"),
    "7.3 heading after patch": patched.count("### 7.3 Instruction Policy"),
    "final 7.2 reference heading": patched.count("#### 7.2.71 参考资料"),
    "new chapter 7 progress": patched.count(new_progress_7),
    "new pending marker": patched.count(new_pending),
    "canonical 7.8 heading": patched.count("### 7.8 Subagent Policy"),
}
for name, count in post_checks.items():
    if count != 1:
        raise SystemExit(f"POST_GUARD_FAIL {name}: expected 1, got {count}")

for stale in (old_progress_7, old_pending, "7.8 Model Routing Policy"):
    if stale in patched:
        raise SystemExit(f"POST_GUARD_FAIL stale marker remains: {stale}")

DOC.write_text(patched, encoding="utf-8")
print("PATCH_OK")
print(f"section_chars={len(section)}")
print(f"doc_chars_before={len(text)}")
print(f"doc_chars_after={len(patched)}")
