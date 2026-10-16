# 11 二分查找

> LeetCode Hot 100 个人题库 · Python 3 标准参考答案

## 35. 搜索插入位置（简单）
**核心模式：** 左边界二分

**题意摘要：** 在有序数组中找到 target；若不存在，返回其应插入的位置。

**标准思路：** 寻找第一个 >= target 的下标。使用左闭右开区间 [l,r)，循环 l<r。

```python
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums)
        while l < r:
            m = (l + r) // 2
            if nums[m] < target:
                l = m + 1
            else:
                r = m
        return l
```

**复杂度：** 时间 O(log n)，空间 O(1)。

**关键易错点：** 把它记成 lower_bound：第一个 >= target 的位置。

## 74. 搜索二维矩阵（中等）
**核心模式：** 展平后二分

**题意摘要：** 矩阵每行升序，且下一行首元素大于上一行尾元素；判断 target 是否存在。

**标准思路：** 把 m×n 矩阵视作长度 mn 的有序数组，虚拟下标 idx 对应 matrix[idx//n][idx%n]。

```python
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m, n = len(matrix), len(matrix[0])
        l, r = 0, m * n - 1
        while l <= r:
            mid = (l + r) // 2
            x = matrix[mid // n][mid % n]
            if x == target:
                return True
            if x < target:
                l = mid + 1
            else:
                r = mid - 1
        return False
```

**复杂度：** 时间 O(log(mn))，空间 O(1)。

**关键易错点：** 注意它与 240 题“行列各自有序但行之间不严格连续”的结构不同。

## 34. 在排序数组中查找元素的第一个和最后一个位置（中等）
**核心模式：** 两次边界二分

**题意摘要：** 在非递减数组中返回 target 的起止位置，不存在则 [-1,-1]。

**标准思路：** 实现 lower_bound(x)=第一个 >=x 的位置。left=lower_bound(target)，right=lower_bound(target+1)-1（整数 target）。

```python
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        def lower_bound(x):
            l, r = 0, len(nums)
            while l < r:
                m = (l + r) // 2
                if nums[m] < x:
                    l = m + 1
                else:
                    r = m
            return l

        left = lower_bound(target)
        if left == len(nums) or nums[left] != target:
            return [-1, -1]
        right = lower_bound(target + 1) - 1
        return [left, right]
```

**复杂度：** 时间 O(log n)，空间 O(1)。

**关键易错点：** 若元素类型不是整数，可改写 upper_bound（第一个 > target）而非 target+1。

## 33. 搜索旋转排序数组（中等）
**核心模式：** 二分 / 判断哪一半有序

**题意摘要：** 无重复升序数组在某点旋转后，O(log n) 查找 target。

**标准思路：** 每次 mid 至少有一半仍有序。先判断左半还是右半有序，再看 target 是否落在该有序范围内，从而舍弃另一半。

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums) - 1
        while l <= r:
            m = (l + r) // 2
            if nums[m] == target:
                return m
            if nums[l] <= nums[m]:
                if nums[l] <= target < nums[m]:
                    r = m - 1
                else:
                    l = m + 1
            else:
                if nums[m] < target <= nums[r]:
                    l = m + 1
                else:
                    r = m - 1
        return -1
```

**复杂度：** 时间 O(log n)，空间 O(1)。

**关键易错点：** 边界中的 <= / < 要和有序区间定义一致。

## 153. 寻找旋转排序数组中的最小值（中等）
**核心模式：** 二分 / 与右端比较

**题意摘要：** 无重复升序数组旋转后，找到最小元素。

**标准思路：** 比较 nums[mid] 与 nums[r]：若 mid 更大，最小值一定在右侧；否则最小值在 [l,mid]。最终 l==r。

```python
class Solution:
    def findMin(self, nums: List[int]) -> int:
        l, r = 0, len(nums) - 1
        while l < r:
            m = (l + r) // 2
            if nums[m] > nums[r]:
                l = m + 1
            else:
                r = m
        return nums[l]
```

**复杂度：** 时间 O(log n)，空间 O(1)。

**关键易错点：** 这里 r=m 而不是 m-1，因为 mid 本身可能就是最小值。

## 4. 寻找两个正序数组的中位数（困难）
**核心模式：** 二分分割 / 较短数组

**题意摘要：** 在 O(log(m+n)) 量级内求两个有序数组的中位数。

**标准思路：** 在较短数组上二分切分位置 i，并令另一数组切分 j 使左半总元素数固定。合法切分满足 Aleft<=Bright 且 Bleft<=Aright；根据违反方向调整 i。

```python
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        A, B = nums1, nums2
        if len(A) > len(B):
            A, B = B, A
        m, n = len(A), len(B)
        total_left = (m + n + 1) // 2
        l, r = 0, m

        while l <= r:
            i = (l + r) // 2
            j = total_left - i
            Aleft = float('-inf') if i == 0 else A[i - 1]
            Aright = float('inf') if i == m else A[i]
            Bleft = float('-inf') if j == 0 else B[j - 1]
            Bright = float('inf') if j == n else B[j]

            if Aleft <= Bright and Bleft <= Aright:
                if (m + n) % 2:
                    return float(max(Aleft, Bleft))
                return (max(Aleft, Bleft) + min(Aright, Bright)) / 2.0
            elif Aleft > Bright:
                r = i - 1
            else:
                l = i + 1
```

**复杂度：** 时间 O(log(min(m,n)))，空间 O(1)。

**关键易错点：** 最难点不是代码，而是“左右两部分数量固定 + 左部所有值不大于右部”这两个条件。
