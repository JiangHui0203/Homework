from pathlib import Path

DOC = Path("Agent_Knowledge_System.md")
PART_DIR = Path(".tmp_agent_ch67")

text = DOC.read_text(encoding="utf-8")
section = "".join((PART_DIR / f"part{i}.md").read_text(encoding="utf-8") for i in range(1, 5))

old_section = """### 6.7 A2A

- Agent Card
- Discovery
- Task
- State
- Remote Agent

6.7 待补充。

概念边界：

```text
MCP：Agent ↔ Capability / Data / Tool
A2A：Agent ↔ Agent
```

---
"""

old_progress = "| II | 6. Multi-Agent & Agent Interoperability | 进行中：6.1–6.6 已完成；下一节 6.7 A2A |"
new_progress = "| II | 6. Multi-Agent & Agent Interoperability | 已完成：6.1–6.7；下一章 7. Agent Harness |"
next_chapter = "# III. Harness & Agent System\n\n## 7. Agent Harness"

checks = {
    "old 6.7 skeleton": text.count(old_section),
    "old progress pointer": text.count(old_progress),
    "next chapter marker": text.count(next_chapter),
    "6.7 heading before patch": text.count("### 6.7 A2A"),
    "pending marker before patch": text.count("6.7 待补充。"),
}

for name, count in checks.items():
    if count != 1:
        raise SystemExit(f"GUARD_FAIL {name}: expected 1, got {count}")

if not section.startswith("### 6.7 A2A\n"):
    raise SystemExit("GUARD_FAIL staged section missing expected heading")
if not section.rstrip().endswith("---"):
    raise SystemExit("GUARD_FAIL staged section missing closing separator")

patched = text.replace(old_section, section, 1).replace(old_progress, new_progress, 1)

post_checks = {
    "new 6.7 heading": patched.count("### 6.7 A2A"),
    "new progress pointer": patched.count(new_progress),
    "next chapter marker after patch": patched.count(next_chapter),
    "final reference heading": patched.count("#### 6.7.119 参考资料"),
}
for name, count in post_checks.items():
    if count != 1:
        raise SystemExit(f"POST_GUARD_FAIL {name}: expected 1, got {count}")

if "6.7 待补充。" in patched:
    raise SystemExit("POST_GUARD_FAIL pending marker still present")
if old_progress in patched:
    raise SystemExit("POST_GUARD_FAIL old progress pointer still present")

DOC.write_text(patched, encoding="utf-8")
print("PATCH_OK")
print(f"section_chars={len(section)}")
print(f"doc_chars_before={len(text)}")
print(f"doc_chars_after={len(patched)}")
