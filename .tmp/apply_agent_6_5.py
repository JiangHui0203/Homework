from pathlib import Path

DOC = Path('Agent_Knowledge_System.md')
SECTION = Path('.tmp/section_6_5.md')

doc = DOC.read_text(encoding='utf-8')
section = SECTION.read_text(encoding='utf-8').rstrip()

placeholder = '### 6.5 Shared / Private Context\n### 6.6 Coordination Failure'
assert doc.count(placeholder) == 1, doc.count(placeholder)
doc = doc.replace(placeholder, section + '\n\n### 6.6 Coordination Failure', 1)

old_progress = '| II | 6. Multi-Agent & Agent Interoperability | 进行中：6.1–6.3 已完成 |'
new_progress = '| II | 6. Multi-Agent & Agent Interoperability | 进行中：6.1–6.5 已完成；下一节 6.6 Coordination Failure |'
assert doc.count(old_progress) == 1, doc.count(old_progress)
doc = doc.replace(old_progress, new_progress, 1)

old_pending = '''### 6.7 A2A

- Agent Card
- Discovery
- Task
- State
- Remote Agent

以上各节待补充。'''
new_pending = '''### 6.7 A2A

- Agent Card
- Discovery
- Task
- State
- Remote Agent

6.6–6.7 待补充。'''
assert doc.count(old_pending) == 1, doc.count(old_pending)
doc = doc.replace(old_pending, new_pending, 1)

DOC.write_text(doc, encoding='utf-8')

assert doc.count('### 6.5 Shared / Private Context') == 1
assert doc.count('### 6.6 Coordination Failure') == 1
assert '#### 6.5.153 参考资料' in doc
assert '6.1–6.5 已完成；下一节 6.6 Coordination Failure' in doc
print('PATCH_OK')
