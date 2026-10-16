# 08 二叉树

> LeetCode Hot 100 个人题库 · Python 3 标准参考答案

## 94. 二叉树的中序遍历（简单）
**核心模式：** 迭代栈

**题意摘要：** 按“左-根-右”顺序返回二叉树节点值。

**标准思路：** 一路把左链入栈；栈顶弹出后访问，再转向其右子树，重复上述过程。

```python
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        ans, stack = [], []
        cur = root
        while cur or stack:
            while cur:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            ans.append(cur.val)
            cur = cur.right
        return ans
```

**复杂度：** 时间 O(n)，空间 O(h)。

**关键易错点：** 迭代模板是树遍历基础；递归版本更短但面试常要求会迭代。

## 104. 二叉树的最大深度（简单）
**核心模式：** DFS 递归

**题意摘要：** 返回根节点到最远叶子节点的节点数。

**标准思路：** 空树深度 0；非空树深度 = 1 + max(左子树深度, 右子树深度)。

```python
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
```

**复杂度：** 时间 O(n)，递归栈 O(h)。

**关键易错点：** 先明确“深度”按节点数还是边数；本题按节点数。

## 226. 翻转二叉树（简单）
**核心模式：** DFS / 交换左右子树

**题意摘要：** 把每个节点的左右子树互换。

**标准思路：** 递归翻转左右子树并交换即可；前序/后序均可。

```python
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None
        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root
```

**复杂度：** 时间 O(n)，递归栈 O(h)。

**关键易错点：** 递归赋值右侧会先取旧引用，因此这种一行交换在 Python 中安全。

## 101. 对称二叉树（简单）
**核心模式：** 镜像递归

**题意摘要：** 判断一棵树是否关于根节点轴对称。

**标准思路：** 比较两棵子树是否镜像：节点值相等，且 a.left 对应 b.right、a.right 对应 b.left。

```python
class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        def mirror(a, b):
            if not a or not b:
                return a is b
            return (a.val == b.val and
                    mirror(a.left, b.right) and
                    mirror(a.right, b.left))
        return mirror(root.left, root.right) if root else True
```

**复杂度：** 时间 O(n)，空间 O(h)。

**关键易错点：** 对称比较不是“左右子树结构相同”，而是交叉镜像。

## 543. 二叉树的直径（简单）
**核心模式：** 后序 DFS / 高度贡献

**题意摘要：** 求任意两节点之间最长路径的边数。

**标准思路：** DFS 返回节点向下的最大深度；经过当前节点的直径为 left_depth + right_depth，用全局变量更新最大值。

```python
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        ans = 0

        def depth(node):
            nonlocal ans
            if not node:
                return 0
            l = depth(node.left)
            r = depth(node.right)
            ans = max(ans, l + r)
            return 1 + max(l, r)

        depth(root)
        return ans
```

**复杂度：** 时间 O(n)，空间 O(h)。

**关键易错点：** DFS 返回的是“深度”，全局更新的是“直径”；两个量不要混。

## 102. 二叉树的层序遍历（中等）
**核心模式：** BFS / 队列

**题意摘要：** 按层从上到下返回每层节点值。

**标准思路：** 队列做 BFS；每轮先记录当前队列长度 size，只弹出这 size 个节点组成一层。

```python
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        q = deque([root])
        ans = []
        while q:
            level = []
            for _ in range(len(q)):
                node = q.popleft()
                level.append(node.val)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            ans.append(level)
        return ans
```

**复杂度：** 时间 O(n)，空间 O(w)，w 为最大层宽。

**关键易错点：** for range(len(q)) 的 len(q) 在循环开始时取值，正好锁定当前层。

## 108. 将有序数组转换为二叉搜索树（简单）
**核心模式：** 分治 / 中点作为根

**题意摘要：** 把升序数组转换成高度平衡 BST。

**标准思路：** 每次取区间中点作为根，左右两半递归构造左右子树。

```python
class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        def build(l, r):
            if l > r:
                return None
            m = (l + r) // 2
            root = TreeNode(nums[m])
            root.left = build(l, m - 1)
            root.right = build(m + 1, r)
            return root
        return build(0, len(nums) - 1)
```

**复杂度：** 时间 O(n)，递归栈 O(log n)（平衡）。

**关键易错点：** 取左中点或右中点都可以，只要保持平衡。

## 98. 验证二叉搜索树（中等）
**核心模式：** 中序严格递增

**题意摘要：** 判断二叉树是否满足 BST：每个节点左子树都小于它，右子树都大于它。

**标准思路：** BST 的中序遍历应严格递增。迭代中序时保存前一个访问值，若当前值 <= prev 则失败。

```python
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        stack = []
        cur = root
        prev = None
        while cur or stack:
            while cur:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            if prev is not None and cur.val <= prev:
                return False
            prev = cur.val
            cur = cur.right
        return True
```

**复杂度：** 时间 O(n)，空间 O(h)。

**关键易错点：** 只比较节点与直接孩子不够；BST 约束作用于整棵左右子树。

## 230. 二叉搜索树中第 K 小的元素（中等）
**核心模式：** BST 中序遍历

**题意摘要：** 返回 BST 中第 k 小的节点值。

**标准思路：** BST 中序遍历天然升序；迭代中序每弹出一个节点就令 k-1，减到 0 时返回。

```python
class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        stack = []
        cur = root
        while True:
            while cur:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            k -= 1
            if k == 0:
                return cur.val
            cur = cur.right
```

**复杂度：** 时间 O(h+k) 到 O(n)，空间 O(h)。

**关键易错点：** 利用 BST 性质，不需要先完整遍历或排序全部节点。

## 199. 二叉树的右视图（中等）
**核心模式：** BFS / 每层最后一个

**题意摘要：** 从右侧观察二叉树，返回每层最右可见节点。

**标准思路：** 层序遍历，每层处理完成时记录该层最后弹出的节点值。

```python
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []
        q = deque([root])
        ans = []
        while q:
            size = len(q)
            for i in range(size):
                node = q.popleft()
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
                if i == size - 1:
                    ans.append(node.val)
        return ans
```

**复杂度：** 时间 O(n)，空间 O(w)。

**关键易错点：** 也可以 DFS 先访问右子树，并在首次到达某深度时记录。

## 114. 二叉树展开为链表（中等）
**核心模式：** 反向前序 DFS

**题意摘要：** 原地把树展开成“根-左-右”前序顺序的右链表，所有 left 置空。

**标准思路：** 按“右-左-根”反向前序遍历，用 prev 指向已展开好的后继；当前节点 right=prev，left=None，再更新 prev。

```python
class Solution:
    def flatten(self, root: Optional[TreeNode]) -> None:
        prev = None

        def dfs(node):
            nonlocal prev
            if not node:
                return
            dfs(node.right)
            dfs(node.left)
            node.right = prev
            node.left = None
            prev = node

        dfs(root)
```

**复杂度：** 时间 O(n)，递归栈 O(h)。

**关键易错点：** 必须先递归 right 再 left，因为是在反向构造前序链。

## 105. 从前序与中序遍历序列构造二叉树（中等）
**核心模式：** 分治 + 中序索引表

**题意摘要：** 由无重复元素的前序和中序遍历重建二叉树。

**标准思路：** 前序首元素是根；在中序中找到根即可确定左子树大小。用哈希表 O(1) 获取中序位置，并通过下标区间递归。

```python
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        idx = {v: i for i, v in enumerate(inorder)}

        def build(pl, pr, il, ir):
            if pl > pr:
                return None
            root_val = preorder[pl]
            k = idx[root_val]
            left_size = k - il
            root = TreeNode(root_val)
            root.left = build(pl + 1, pl + left_size, il, k - 1)
            root.right = build(pl + left_size + 1, pr, k + 1, ir)
            return root

        n = len(preorder)
        return build(0, n - 1, 0, n - 1)
```

**复杂度：** 时间 O(n)，空间 O(n)。

**关键易错点：** 左右递归边界最容易写错，先明确 left_size 再推下标。

## 437. 路径总和 III（中等）
**核心模式：** 树上前缀和 + 回溯计数

**题意摘要：** 统计树中向下连续路径和等于 targetSum 的路径数量；路径不要求从根开始或到叶结束。

**标准思路：** DFS 维护从根到当前节点的前缀和 cur；若之前出现过 cur-target，就得到相应数量的合法路径。进入节点时加计数，离开时减计数，体现回溯。

```python
class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        prefix = defaultdict(int)
        prefix[0] = 1

        def dfs(node, cur):
            if not node:
                return 0
            cur += node.val
            ans = prefix[cur - targetSum]
            prefix[cur] += 1
            ans += dfs(node.left, cur)
            ans += dfs(node.right, cur)
            prefix[cur] -= 1
            return ans

        return dfs(root, 0)
```

**复杂度：** 时间 O(n)，空间 O(h)~O(n)。

**关键易错点：** 离开当前递归分支时必须 prefix[cur]-=1，避免不同分支之间互相污染。

## 236. 二叉树的最近公共祖先（中等）
**核心模式：** 后序 DFS

**题意摘要：** 在普通二叉树中寻找两个给定节点 p、q 的最近公共祖先。

**标准思路：** 若当前节点是 p/q 直接返回；递归左右子树。左右都非空说明 p/q 分居两侧，当前节点即 LCA；否则返回非空的一侧。

```python
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if not root or root is p or root is q:
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left and right:
            return root
        return left or right
```

**复杂度：** 时间 O(n)，空间 O(h)。

**关键易错点：** 这是普通二叉树版本，不要误用 BST 的大小比较性质。

## 124. 二叉树中的最大路径和（困难）
**核心模式：** 后序 DFS / 单边贡献

**题意摘要：** 路径可从任意节点到任意节点，但相邻节点必须由边连接；求最大路径和。

**标准思路：** DFS 返回“从当前节点向父节点能提供的最大单边贡献”，负贡献截断为 0；经过当前节点的完整路径可同时取左右两边，用它更新全局答案。

```python
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        ans = float('-inf')

        def gain(node):
            nonlocal ans
            if not node:
                return 0
            left = max(0, gain(node.left))
            right = max(0, gain(node.right))
            ans = max(ans, node.val + left + right)
            return node.val + max(left, right)

        gain(root)
        return ans
```

**复杂度：** 时间 O(n)，空间 O(h)。

**关键易错点：** “返回给父节点”的路径不能同时走左右两边；全局候选才可以。
