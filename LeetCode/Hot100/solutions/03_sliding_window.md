# 03 滑动窗口

> LeetCode Hot 100 个人题库 · Python 3 标准参考答案

## 3. 无重复字符的最长子串（中等）
**核心模式：** 可变长滑动窗口 / 最近位置

**题意摘要：** 求不含重复字符的最长连续子串长度。

**标准思路：** 记录每个字符最近出现位置。右指针扩展时，如字符在当前窗口中出现过，left 直接跳到其上次位置后一位。

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last = {}
        left = 0
        ans = 0
        for right, ch in enumerate(s):
            if ch in last and last[ch] >= left:
                left = last[ch] + 1
            last[ch] = right
            ans = max(ans, right - left + 1)
        return ans
```

**复杂度：** 时间 O(n)，空间 O(字符集大小)。

**关键易错点：** left 只能向右移动，不能被旧位置拉回去。

## 438. 找到字符串中所有字母异位词（中等）
**核心模式：** 固定长滑动窗口 / 频次匹配

**题意摘要：** 在 s 中找出所有长度与 p 相同且字符频次一致的子串起点。

**标准思路：** 窗口长度固定为 len(p)。维护 need 和 window 计数；每次加入右端字符，若窗口过长则移出左端，再比较计数。

```python
class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        if len(p) > len(s):
            return []
        need = Counter(p)
        window = Counter()
        ans = []
        m = len(p)
        for r, ch in enumerate(s):
            window[ch] += 1
            if r >= m:
                left_ch = s[r - m]
                window[left_ch] -= 1
                if window[left_ch] == 0:
                    del window[left_ch]
            if r >= m - 1 and window == need:
                ans.append(r - m + 1)
        return ans
```

**复杂度：** 时间近似 O(n)（字符集固定时），空间 O(字符集大小)。

**关键易错点：** 若字符集为固定 26 个小写字母，可用长度 26 的数组进一步降低常数。
