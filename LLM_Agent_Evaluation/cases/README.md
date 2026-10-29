# Cases

Case 负责把稳定理论映射到真实系统，但不承担概念定义权。

当前主案例：[`veriagent/`](./veriagent/)。

规则：

- `current/` 可以随实现更新；
- `frozen/` 绑定日期 / commit / protocol，冻结后不覆盖；
- 源代码仍留在原项目仓库；
- 单个案例经验只有跨案例稳定后才能 promote 到 `EVAL_PATTERNS.md` 或正式知识章节。