# 06 矩阵

> LeetCode Hot 100 个人题库 · Python 3 标准参考答案

## 73. 矩阵置零（中等）
**核心模式：** 原地标记 / 首行首列

**题意摘要：** 若某位置为 0，则将其整行整列置 0，要求原地。

**标准思路：** 利用第一行和第一列充当标记数组；额外用两个布尔量记录第一行/第一列原本是否含 0。

```python
class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        m, n = len(matrix), len(matrix[0])
        row0 = any(matrix[0][j] == 0 for j in range(n))
        col0 = any(matrix[i][0] == 0 for i in range(m))

        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0
                    matrix[0][j] = 0

        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0

        if row0:
            for j in range(n):
                matrix[0][j] = 0
        if col0:
            for i in range(m):
                matrix[i][0] = 0
```

**复杂度：** 时间 O(mn)，空间 O(1)。

**关键易错点：** 第一行和第一列同时承担标记职责，所以原始状态要先单独保存。

## 54. 螺旋矩阵（中等）
**核心模式：** 边界模拟

**题意摘要：** 按顺时针螺旋顺序遍历矩阵。

**标准思路：** 维护 top/bottom/left/right 四条边界，每轮依次走上边、右边、下边、左边；每走完一边收缩对应边界，并在必要时检查边界仍合法。

```python
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1
        ans = []
        while top <= bottom and left <= right:
            for j in range(left, right + 1):
                ans.append(matrix[top][j])
            top += 1

            for i in range(top, bottom + 1):
                ans.append(matrix[i][right])
            right -= 1

            if top <= bottom:
                for j in range(right, left - 1, -1):
                    ans.append(matrix[bottom][j])
                bottom -= 1

            if left <= right:
                for i in range(bottom, top - 1, -1):
                    ans.append(matrix[i][left])
                left += 1
        return ans
```

**复杂度：** 时间 O(mn)，空间 O(1)（不计输出）。

**关键易错点：** 走下边和左边前必须重新判断边界，避免单行/单列重复访问。

## 48. 旋转图像（中等）
**核心模式：** 转置 + 每行反转

**题意摘要：** 将 n×n 矩阵顺时针旋转 90°，要求原地。

**标准思路：** 顺时针 90° 等价于“沿主对角线转置”后“每一行反转”。

```python
class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        for row in matrix:
            row.reverse()
```

**复杂度：** 时间 O(n²)，空间 O(1)。

**关键易错点：** 记忆几何关系：顺时针=转置+行反转；逆时针则可用转置+列反转。

## 240. 搜索二维矩阵 II（中等）
**核心模式：** 右上角阶梯搜索

**题意摘要：** 矩阵每行递增、每列递增，判断 target 是否存在。

**标准思路：** 从右上角开始：当前值太大就左移，太小就下移；每一步排除一整行或一整列。

```python
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        if not matrix or not matrix[0]:
            return False
        i, j = 0, len(matrix[0]) - 1
        while i < len(matrix) and j >= 0:
            if matrix[i][j] == target:
                return True
            if matrix[i][j] > target:
                j -= 1
            else:
                i += 1
        return False
```

**复杂度：** 时间 O(m+n)，空间 O(1)。

**关键易错点：** 应从右上或左下开始；左上无法同时决定唯一移动方向。
