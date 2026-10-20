from pathlib import Path

DOC = Path("Agent_Knowledge_System.md")
PART_DIR = Path(".tmp_agent_ch71")

text = DOC.read_text(encoding="utf-8")
section = "".join((PART_DIR / f"part{i}.md").read_text(encoding="utf-8") for i in range(1, 3))

old_marker = "### 7.1 What is an Agent Harness?\n### 7.2 Agent Loop Policy"
new_marker = section + "### 7.2 Agent Loop Policy"

old_progress_6 = "| II | 6. Multi-Agent & Agent Interoperability | 已完成：6.1–6.7；下一章 7. Agent Harness |"
new_progress_6 = "| II | 6. Multi-Agent & Agent Interoperability | 已完成：6.1–6.7 |"
old_progress_7 = "| III | 7. Agent Harness | 待写 |"
new_progress_7 = "| III | 7. Agent Harness | 进行中：7.1 已完成；下一节 7.2 Agent Loop Policy |"
old_pending = "### 7.10 Termination Policy\n### 7.11 Recovery Policy\n\n以上各节待补充。"
new_pending = "### 7.10 Termination Policy\n### 7.11 Recovery Policy\n\n7.2–7.11 待补充。"

checks = {
    "7.1-to-7.2 marker": text.count(old_marker),
    "chapter 6 progress pointer": text.count(old_progress_6),
    "chapter 7 progress pointer": text.count(old_progress_7),
    "chapter 7 pending marker": text.count(old_pending),
    "7.1 heading before patch": text.count("### 7.1 What is an Agent Harness?"),
    "7.2 heading before patch": text.count("### 7.2 Agent Loop Policy"),
}
for name, count in checks.items():
    if count != 1:
        raise SystemExit(f"GUARD_FAIL {name}: expected 1, got {count}")

if not section.startswith("### 7.1 What is an Agent Harness?\n"):
    raise SystemExit("GUARD_FAIL staged section missing expected heading")
if not section.rstrip().endswith("---"):
    raise SystemExit("GUARD_FAIL staged section missing closing separator")

patched = text.replace(old_marker, new_marker, 1)
patched = patched.replace(old_progress_6, new_progress_6, 1)
patched = patched.replace(old_progress_7, new_progress_7, 1)
patched = patched.replace(old_pending, new_pending, 1)

post_checks = {
    "7.1 heading after patch": patched.count("### 7.1 What is an Agent Harness?"),
    "7.2 heading after patch": patched.count("### 7.2 Agent Loop Policy"),
    "final 7.1 reference heading": patched.count("#### 7.1.84 参考资料"),
    "new chapter 6 progress": patched.count(new_progress_6),
    "new chapter 7 progress": patched.count(new_progress_7),
    "new pending marker": patched.count(new_pending),
}
for name, count in post_checks.items():
    if count != 1:
        raise SystemExit(f"POST_GUARD_FAIL {name}: expected 1, got {count}")

for stale in (old_progress_6, old_progress_7, old_pending):
    if stale in patched:
        raise SystemExit(f"POST_GUARD_FAIL stale marker remains: {stale}")

DOC.write_text(patched, encoding="utf-8")
print("PATCH_OK")
print(f"section_chars={len(section)}")
print(f"doc_chars_before={len(text)}")
print(f"doc_chars_after={len(patched)}")
