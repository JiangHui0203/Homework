# 01 哈希

> LeetCode Hot 100 个人题库 · Python 3 标准参考答案

## 1. 两数之和（简单）
**核心模式：** 哈希表 / 补数查询

**题意摘要：** 在数组中找到两个下标，使对应元素之和等于 target。

**标准思路：** 从左到右扫描。对当前数 x，只需判断 target-x 是否已经出现；若出现立即返回，否则记录 x 的下标。

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        pos = {}
        for i, x in enumerate(nums):
            need = target - x
            if need in pos:
                return [pos[need], i]
            pos[x] = i
        return []
```

**复杂度：** 时间 O(n)，空间 O(n)。

**关键易错点：** 先查再存，避免同一个元素被使用两次。

## 49. 字母异位词分组（中等）
**核心模式：** 哈希表 / 规范化键

**题意摘要：** 把互为字母异位词的字符串分到同一组。

**标准思路：** 异位词排序后结果相同。用排序后的字符串作为哈希键，将原字符串追加到对应分组。

```python
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        for s in strs:
            key = ''.join(sorted(s))
            groups[key].append(s)
        return list(groups.values())
```

**复杂度：** 设字符串平均长度为 k：时间 O(n·k log k)，空间 O(nk)。

**关键易错点：** 若面试追求 O(nk)，可用 26 个字母计数元组作为 key。

## 128. 最长连续序列（中等）
**核心模式：** 哈希集合 / 只从序列起点扩展

**题意摘要：** 给定无序数组，求最长连续整数序列长度，要求整体接近 O(n)。

**标准思路：** 把元素放入 set。只有当 x-1 不在集合中时，x 才是某段连续序列的起点；从起点向右扩展并更新最长长度。

```python
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        s = set(nums)
        ans = 0
        for x in s:
            if x - 1 not in s:
                y = x
                while y in s:
                    y += 1
                ans = max(ans, y - x)
        return ans
```

**复杂度：** 均摊时间 O(n)，空间 O(n)。

**关键易错点：** 关键是“只从起点扩展”；否则会退化成 O(n²)。
