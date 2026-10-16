# 02 双指针

> LeetCode Hot 100 个人题库 · Python 3 标准参考答案

## 283. 移动零（简单）
**核心模式：** 快慢指针 / 原地覆盖

**题意摘要：** 保持非零元素相对顺序，把所有 0 移到数组末尾。

**标准思路：** slow 指向下一个应放非零元素的位置；fast 扫描数组，遇到非零就与 slow 位置交换。

```python
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        slow = 0
        for fast in range(len(nums)):
            if nums[fast] != 0:
                nums[slow], nums[fast] = nums[fast], nums[slow]
                slow += 1
```

**复杂度：** 时间 O(n)，额外空间 O(1)。

**关键易错点：** 题目要求原地修改，不要创建新数组作为最终答案。

## 11. 盛最多水的容器（中等）
**核心模式：** 左右双指针 / 贪心缩边

**题意摘要：** 选择两条竖线形成容器，使面积最大。

**标准思路：** 面积受较短边限制。每次计算当前面积后，移动较短的那一侧；移动长边不可能在宽度变小的同时突破短边瓶颈。

```python
class Solution:
    def maxArea(self, height: List[int]) -> int:
        l, r = 0, len(height) - 1
        ans = 0
        while l < r:
            ans = max(ans, (r - l) * min(height[l], height[r]))
            if height[l] <= height[r]:
                l += 1
            else:
                r -= 1
        return ans
```

**复杂度：** 时间 O(n)，空间 O(1)。

**关键易错点：** 理解“为什么移动短边”比记代码更重要。

## 15. 三数之和（中等）
**核心模式：** 排序 + 双指针 + 去重

**题意摘要：** 找出所有不重复的三元组，使三数之和为 0。

**标准思路：** 先排序。固定第一个数 i，在右侧用 l/r 双指针寻找 -nums[i]；固定值和命中后都要跳过重复元素。

```python
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        ans = []
        n = len(nums)
        for i in range(n - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            if nums[i] > 0:
                break
            l, r = i + 1, n - 1
            while l < r:
                s = nums[i] + nums[l] + nums[r]
                if s < 0:
                    l += 1
                elif s > 0:
                    r -= 1
                else:
                    ans.append([nums[i], nums[l], nums[r]])
                    l += 1
                    r -= 1
                    while l < r and nums[l] == nums[l - 1]:
                        l += 1
                    while l < r and nums[r] == nums[r + 1]:
                        r -= 1
        return ans
```

**复杂度：** 时间 O(n²)，排序带来 O(log n)~O(n) 额外空间（依实现）。

**关键易错点：** 去重分两层：固定的 i 去重；命中后的 l、r 去重。

## 42. 接雨水（困难）
**核心模式：** 左右双指针 / 单侧上界

**题意摘要：** 柱状图中计算能接住的雨水总量。

**标准思路：** 维护 left_max/right_max。哪一侧当前柱子更低，就可以确定该侧位置的水量，因为它的有效瓶颈已由该侧最大值和另一侧至少同等高度保证。

```python
class Solution:
    def trap(self, height: List[int]) -> int:
        l, r = 0, len(height) - 1
        left_max = right_max = 0
        ans = 0
        while l < r:
            if height[l] <= height[r]:
                left_max = max(left_max, height[l])
                ans += left_max - height[l]
                l += 1
            else:
                right_max = max(right_max, height[r])
                ans += right_max - height[r]
                r -= 1
        return ans
```

**复杂度：** 时间 O(n)，空间 O(1)。

**关键易错点：** 另一经典解法是单调栈；双指针版本更适合面试快速实现。
