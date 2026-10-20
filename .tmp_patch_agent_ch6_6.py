from pathlib import Path

DOC = Path("Agent_Knowledge_System.md")
PARTS = [
    Path(".tmp_agent_ch6_6_part1.md"),
    Path(".tmp_agent_ch6_6_part2.md"),
    Path(".tmp_agent_ch6_6_part3.md"),
]

text = DOC.read_text(encoding="utf-8")
section = "\n\n".join(p.read_text(encoding="utf-8").strip() for p in PARTS).strip() + "\n\n"

h66 = "### 6.6 Coordination Failure"
h67 = "### 6.7 A2A"
old_progress = "| II | 6. Multi-Agent & Agent Interoperability | 进行中：6.1–6.5 已完成；下一节 6.6 Coordination Failure |"
new_progress = "| II | 6. Multi-Agent & Agent Interoperability | 进行中：6.1–6.6 已完成；下一节 6.7 A2A |"
old_pending = "6.6–6.7 待补充。"
new_pending = "6.7 待补充。"

assert section.startswith(h66 + "\n"), "section heading mismatch"
assert section.count(h66) == 1, "section contains duplicate 6.6 heading"
assert text.count(h66) == 1, f"expected exactly one 6.6 placeholder, got {text.count(h66)}"
assert text.count(h67) == 1, f"expected exactly one 6.7 heading, got {text.count(h67)}"
assert text.count(old_progress) == 1, "canonical progress pointer mismatch"
assert text.count(old_pending) == 1, "Chapter 6 pending marker mismatch"

start = text.index(h66)
end = text.index(h67, start)
assert start < end, "6.6 must precede 6.7"
placeholder_region = text[start:end]
assert "#### 6.6." not in placeholder_region, "6.6 is no longer an empty placeholder"

text = text[:start] + section + text[end:]
text = text.replace(old_progress, new_progress, 1)
text = text.replace(old_pending, new_pending, 1)

assert text.count(h66) == 1
assert text.count("#### 6.6.1 Coordination Failure 到底是什么") == 1
assert text.count("#### 6.6.133 参考资料") == 1
assert text.count(h67) == 1
assert old_progress not in text
assert new_progress in text
assert old_pending not in text
assert new_pending in text

DOC.write_text(text, encoding="utf-8")
print("PATCH_OK")
