# LeetCode Hot 100 算法模板库

> 目标：把 100 道题压缩成可复用的 Pattern。面试时先做“题目特征 → 模板”的识别，再进入具体实现。
>
> 默认语言：Python 3。模板只保留最典型骨架；具体题目的完整答案见 [`solutions/`](solutions/)。

---

## 0. 怎么使用这份模板库

不要把模板理解成“背代码”。真正需要形成的是下面这条链：

```text
题目特征
  ↓
识别 Pattern
  ↓
明确 invariant / 状态定义
  ↓
套代码骨架
  ↓
根据题目修改边界、更新条件、返回值
```

掌握标准分两档：

- **S 级模板：必须形成肌肉记忆。** 面试看到特征后，应能迅速写出骨架。
- **A 级模板：理解机制即可。** 不一定背完整代码，但要能从 invariant 推出来。

---

# 一、快速识别表

| 题目特征 | 第一反应 | 代表题 |
|---|---|---|
| “找另一个数使两者满足关系” | 哈希补数 | 1 两数之和 |
| 字符串按“等价特征”分组 | 规范化哈希键 | 49 字母异位词分组 |
| 无序数组中的连续整数 | set + 只从起点扩展 | 128 最长连续序列 |
| 有序数组 / 两端取舍 | 左右双指针 | 11、15 |
| 原地移动、删除、覆盖 | 快慢指针 | 283 |
| 连续子串/子数组 + 最长/最短约束 | 滑动窗口 | 3、76 |
| 固定长度窗口统计 | 固定滑窗 | 438 |
| 子数组和 = K | 前缀和 + 哈希 | 560 |
| 滑动窗口最大/最小值 | 单调队列 | 239 |
| 区间重叠 | 排序 + 合并 | 56 |
| 除自身外的累计信息 | 前缀/后缀 | 238 |
| 值域可映射到数组下标 | 原地置换/标记 | 41 |
| 链表头可能变化 | dummy 节点 | 21、19、24 |
| 链表局部方向反转 | 三指针反转 | 206、24、25 |
| 链表环 / 中点 | 快慢指针 | 141、142、234 |
| 倒数第 N 个节点 | 前后双指针 | 19 |
| 树：从根向下携带信息 | 自顶向下 DFS | 98 |
| 树：答案依赖左右子树返回值 | 自底向上 DFS | 104、543、124 |
| 树：按层处理 | BFS | 102、199 |
| BST + 第 k 小 | 中序遍历 | 230 |
| 网格连通块 | DFS/BFS Flood Fill | 200 |
| 多源扩散、最少轮数 | 多源 BFS | 994 |
| 课程依赖、先后关系 | 拓扑排序 | 207 |
| 前缀查询 | Trie | 208 |
| 所有排列/组合/方案 | 回溯 | 46、78、39 |
| 有序 + 查找位置/边界 | 二分 | 35、34 |
| 旋转有序数组 | 二分 + 判断有序半边 | 33、153 |
| 成对括号 / 嵌套结构 | 栈 | 20、394 |
| 最近更大/更小元素 | 单调栈 | 739、84 |
| 第 K 大 / Top K | 堆 | 215、347 |
| “能否到达 / 最少跳几次” | 贪心覆盖范围 | 55、45 |
| 当前最优依赖前几个状态 | 一维 DP | 70、198 |
| 每个物品最多一次 | 0/1 背包 | 416 |
| 物品可重复使用 | 完全背包 | 279、322 |
| 两个序列/字符串前缀关系 | 二维 DP | 1143、72 |

---

# 二、哈希与集合

## 模板 1：哈希补数查询【S】

### 识别信号

- “找两个元素满足某种关系”；
- 暴力需要枚举两两组合；
- 当前元素确定后，可以直接算出“需要的另一个值”。

### 核心 invariant

`seen` 只保存当前位置之前已经扫描过的元素。

```python
seen = {}
for i, x in enumerate(nums):
    need = target - x
    if need in seen:
        return seen[need], i
    seen[x] = i
```

### 易错点

- 通常要**先查询、后写入**，防止一个元素被使用两次。
- 先问清楚返回的是值还是下标。

### Hot 100

- 1 两数之和

---

## 模板 2：规范化键分组【A】

### 识别信号

多个对象表面不同，但存在一个“规范化表示”，规范化后相同就属于同类。

```python
groups = defaultdict(list)
for item in items:
    key = normalize(item)
    groups[key].append(item)
```

常见 `normalize`：

- 排序结果；
- 字符计数元组；
- 坐标差值；
- 频率向量。

### Hot 100

- 49 字母异位词分组

---

## 模板 3：集合中只从“起点”扩展【S】

### 识别信号

- 无序元素；
- 要找连续段；
- 用 set 可 O(1) 判断邻居是否存在。

```python
s = set(nums)
ans = 0

for x in s:
    if x - 1 not in s:      # x 才是起点
        y = x
        while y in s:
            y += 1
        ans = max(ans, y - x)
```

### 核心 invariant

每个连续段只从最小元素启动一次。

### Hot 100

- 128 最长连续序列

---

# 三、双指针与滑动窗口

## 模板 4：左右双指针【S】

### 识别信号

- 数组有序；
- 两端状态可以决定舍弃哪一端；
- 两元素组合 / 面积 / 接水等问题。

```python
left, right = 0, len(nums) - 1
while left < right:
    # 根据 nums[left] / nums[right] 更新答案

    if 应该移动左边:
        left += 1
    else:
        right -= 1
```

### 关键问题

每移动一次指针，都要能解释：**为什么被舍弃的这一侧不可能产生更优答案？**

### Hot 100

- 11 盛最多水的容器
- 15 三数之和（排序后内层双指针）
- 42 接雨水（双指针解法）

---

## 模板 5：快慢指针原地覆盖【S】

### 识别信号

- 原地删除 / 移动；
- 保持剩余元素相对顺序；
- 要求 O(1) 额外空间。

```python
slow = 0
for fast in range(len(nums)):
    if nums[fast] 满足保留条件:
        nums[slow] = nums[fast]
        slow += 1
```

### Hot 100

- 283 移动零

---

## 模板 6：可变长度滑动窗口【S】

### 识别信号

- **连续**子串 / 子数组；
- 有一个可维护的窗口约束；
- 求最长、最短或满足条件的区间。

```python
left = 0
state = ...

for right, x in enumerate(data):
    # 1. 把 data[right] 加入窗口
    add(x)

    # 2. 窗口不合法，移动 left 恢复合法
    while window_is_invalid():
        remove(data[left])
        left += 1

    # 3. 当前窗口合法，更新答案
    ans = update(ans, left, right)
```

### 核心 invariant

循环结束时，`[left, right]` 始终满足当前定义的合法条件。

### 最长 vs 最短

- **最长合法窗口：** 非法时收缩，合法时更新答案。
- **最短覆盖窗口：** 合法时主动收缩并不断更新最短答案。

### 易错点

- `while` 和 `if` 不可随意互换；一次移动 left 未必足够恢复合法。
- 必须明确“加入右端、移除左端”分别如何更新状态。

### Hot 100

- 3 无重复字符的最长子串
- 76 最小覆盖子串

---

## 模板 7：固定长度滑动窗口【S】

### 识别信号

窗口长度已知，随着 `right` 移动，每次只需加入一个、移出一个。

```python
for right, x in enumerate(data):
    add(x)

    if right >= k:
        remove(data[right - k])

    if right >= k - 1:
        check_or_update()
```

### Hot 100

- 438 找到字符串中所有字母异位词

---

# 四、前缀信息与队列

## 模板 8：前缀和 + 哈希【S】

### 识别信号

- 连续子数组；
- 要求“区间和 = K”；
- 数组可能有负数，因此普通滑动窗口失效。

若 `prefix[j] - prefix[i] = k`，则对当前 `prefix[j]`，只需查询此前是否存在 `prefix[j] - k`。

```python
count = {0: 1}
prefix = 0
ans = 0

for x in nums:
    prefix += x
    ans += count.get(prefix - k, 0)
    count[prefix] = count.get(prefix, 0) + 1
```

### 为什么先查再存

避免把当前位置的前缀和错误地当作之前出现的前缀。

### Hot 100

- 560 和为 K 的子数组

---

## 模板 9：单调队列【A】

### 识别信号

固定滑动窗口中，需要实时得到最大值 / 最小值。

以窗口最大值为例，deque 中保存**下标**，对应值保持单调递减：

```python
q = deque()

for i, x in enumerate(nums):
    # 1. 移除已经离开窗口的下标
    while q and q[0] <= i - k:
        q.popleft()

    # 2. 新元素比队尾更强，弱者以后永远不可能成为最大值
    while q and nums[q[-1]] <= x:
        q.pop()

    q.append(i)

    if i >= k - 1:
        ans.append(nums[q[0]])
```

### 核心 invariant

队列下标递增；对应值单调递减；队首始终是当前窗口最大值。

### Hot 100

- 239 滑动窗口最大值

---

# 五、数组与区间

## 模板 10：排序后合并区间【S】

### 识别信号

一组区间，需要合并重叠、统计覆盖或处理相交关系。

```python
intervals.sort(key=lambda x: x[0])
merged = []

for start, end in intervals:
    if not merged or start > merged[-1][1]:
        merged.append([start, end])
    else:
        merged[-1][1] = max(merged[-1][1], end)
```

### Hot 100

- 56 合并区间

---

## 模板 11：前缀 / 后缀累计【S】

### 识别信号

当前位置答案由“左边所有元素的信息 + 右边所有元素的信息”共同决定。

```python
ans = [1] * n

prefix = 1
for i in range(n):
    ans[i] = prefix
    prefix *= nums[i]

suffix = 1
for i in range(n - 1, -1, -1):
    ans[i] *= suffix
    suffix *= nums[i]
```

### Hot 100

- 238 除了自身以外数组的乘积

---

## 模板 12：值 ↔ 下标原地映射【A】

### 识别信号

- 数值范围与数组长度强相关，例如答案必在 `[1, n+1]`；
- 要求 O(1) 额外空间；
- 可以把值 `x` 放到它“应该在的下标” `x-1`。

```python
for i in range(n):
    while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
        j = nums[i] - 1
        nums[i], nums[j] = nums[j], nums[i]
```

### Hot 100

- 41 缺失的第一个正数

---

# 六、链表

## 模板 13：dummy 哨兵节点【S】

### 识别信号

- 删除节点；
- 合并链表；
- 头节点本身可能被替换；
- 希望统一“处理头”和“处理中间节点”的逻辑。

```python
dummy = ListNode(0, head)
cur = dummy

# 修改 cur.next ...

return dummy.next
```

### Hot 100

- 21 合并两个有序链表
- 19 删除链表的倒数第 N 个结点
- 24 两两交换链表中的节点
- 25 K 个一组翻转链表

---

## 模板 14：链表三指针反转【S】

```python
prev = None
cur = head

while cur:
    nxt = cur.next
    cur.next = prev
    prev = cur
    cur = nxt

return prev
```

### 核心 invariant

- `prev`：已经反转好的链表头；
- `cur`：当前待处理节点；
- `nxt`：先保存未处理链表，否则修改 `cur.next` 后会断链。

### Hot 100

- 206 反转链表
- 234 回文链表（反转后半段）
- 24 两两交换链表中的节点
- 25 K 个一组翻转链表

---

## 模板 15：链表快慢指针【S】

### 找中点

```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
```

### 判断环

```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow is fast:
        return True
return False
```

### 找环入口

相遇后一个指针回到 head，两者都每次走一步，再次相遇处即入口。

### Hot 100

- 141 环形链表
- 142 环形链表 II
- 234 回文链表

---

## 模板 16：前后间隔 N 的双指针【S】

### 识别信号

链表倒数第 N 个节点 / 删除倒数第 N 个。

```python
dummy = ListNode(0, head)
fast = slow = dummy

for _ in range(n + 1):
    fast = fast.next

while fast:
    fast = fast.next
    slow = slow.next

slow.next = slow.next.next
return dummy.next
```

### Hot 100

- 19 删除链表的倒数第 N 个结点

---

# 七、二叉树

## 模板 17：自顶向下 DFS【S】

### 识别信号

当前节点的判断依赖“从祖先传下来的状态”。

```python
def dfs(node, state):
    if not node:
        return

    new_state = update(state, node)
    dfs(node.left, new_state)
    dfs(node.right, new_state)
```

### 常见 state

- 当前路径和；
- 合法值域 `(low, high)`；
- 路径上的最大/最小值；
- 深度。

### Hot 100

- 98 验证二叉搜索树
- 437 路径总和 III（部分思路）

---

## 模板 18：自底向上 DFS【S】

### 识别信号

父节点的答案依赖左右子树先算出的信息。

```python
def dfs(node):
    if not node:
        return base

    left = dfs(node.left)
    right = dfs(node.right)

    # 可在这里更新全局答案
    update_global(left, right, node)

    # 返回父节点真正需要的信息
    return combine(left, right, node)
```

### 最重要的问题

必须区分：

1. **当前节点用于更新全局答案的信息是什么？**
2. **当前节点能向父节点返回的信息是什么？**

这两个值经常不同。

### Hot 100

- 104 二叉树的最大深度
- 543 二叉树的直径
- 124 二叉树中的最大路径和
- 236 二叉树的最近公共祖先

---

## 模板 19：层序 BFS【S】

```python
q = deque([root])

while q:
    size = len(q)
    level = []

    for _ in range(size):
        node = q.popleft()
        level.append(node.val)

        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)

    process(level)
```

### 核心点

`size = len(q)` 必须在处理本层前固定下来。

### Hot 100

- 102 二叉树的层序遍历
- 199 二叉树的右视图

---

## 模板 20：BST 中序 / 值域性质【S】

### 中序遍历递增

```python
def inorder(node):
    if not node:
        return
    inorder(node.left)
    visit(node)
    inorder(node.right)
```

### 值域验证

```python
def valid(node, low, high):
    if not node:
        return True
    if not (low < node.val < high):
        return False
    return (
        valid(node.left, low, node.val)
        and valid(node.right, node.val, high)
    )
```

### Hot 100

- 94 二叉树的中序遍历
- 98 验证二叉搜索树
- 230 二叉搜索树中第 K 小的元素

---

# 八、图与网格

## 模板 21：DFS/BFS Flood Fill【S】

### 识别信号

二维网格中的连通块、岛屿、区域染色。

```python
def dfs(r, c):
    if r < 0 or r >= m or c < 0 or c >= n:
        return
    if grid[r][c] != target:
        return

    grid[r][c] = visited_mark

    for dr, dc in directions:
        dfs(r + dr, c + dc)
```

外层扫描：

```python
for r in range(m):
    for c in range(n):
        if grid[r][c] == target:
            ans += 1
            dfs(r, c)
```

### Hot 100

- 200 岛屿数量
- 79 单词搜索（带回溯的网格 DFS）

---

## 模板 22：多源 BFS【S】

### 识别信号

- 多个起点同时向外扩散；
- 每轮扩散一步；
- 求全部覆盖所需最短时间 / 层数。

```python
q = deque(all_sources)
steps = 0

while q:
    for _ in range(len(q)):
        cur = q.popleft()
        for nxt in neighbors(cur):
            if can_visit(nxt):
                mark_visited(nxt)
                q.append(nxt)
    steps += 1
```

### Hot 100

- 994 腐烂的橘子

---

## 模板 23：拓扑排序 Kahn【S】

### 识别信号

- 课程依赖；
- 有向图先后关系；
- 判断是否存在环；
- 输出可行执行顺序。

```python
graph = [[] for _ in range(n)]
indegree = [0] * n

for a, b in edges:
    graph[b].append(a)
    indegree[a] += 1

q = deque(i for i in range(n) if indegree[i] == 0)
count = 0

while q:
    u = q.popleft()
    count += 1

    for v in graph[u]:
        indegree[v] -= 1
        if indegree[v] == 0:
            q.append(v)

return count == n
```

### Hot 100

- 207 课程表

---

## 模板 24：Trie 前缀树【A】

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.end = True
```

### 识别信号

大量字符串需要反复进行：

- 精确查找；
- 前缀查询；
- 按字符逐层共享路径。

### Hot 100

- 208 实现 Trie

---

# 九、回溯

## 模板 25：通用回溯【S】

```python
ans = []
path = []

def backtrack(state):
    if 满足结束条件:
        ans.append(path[:])
        return

    for choice in 当前可选项:
        if 不合法:
            continue

        path.append(choice)      # 做选择
        backtrack(next_state)
        path.pop()               # 撤销选择
```

### 三问法

写回溯前先回答：

1. **path 表示什么？**
2. **当前有哪些 choices？**
3. **什么时候算完成？**

### 常见变体

#### 排列：用 `used`

```python
for i in range(n):
    if used[i]:
        continue
    used[i] = True
    path.append(nums[i])
    backtrack()
    path.pop()
    used[i] = False
```

#### 组合/子集：用 `start`

```python
def backtrack(start):
    ans.append(path[:])
    for i in range(start, n):
        path.append(nums[i])
        backtrack(i + 1)
        path.pop()
```

#### 可重复选择

递归时传 `i` 而不是 `i + 1`。

### Hot 100

- 46 全排列
- 78 子集
- 17 电话号码的字母组合
- 39 组合总和
- 22 括号生成
- 79 单词搜索
- 131 分割回文串
- 51 N 皇后

---

# 十、二分查找

## 模板 26：标准二分 / lower bound【S】

### 精确查找

```python
left, right = 0, len(nums) - 1

while left <= right:
    mid = (left + right) // 2
    if nums[mid] == target:
        return mid
    elif nums[mid] < target:
        left = mid + 1
    else:
        right = mid - 1
```

### 找第一个 `>= target` 的位置

推荐使用左闭右开区间：

```python
left, right = 0, len(nums)

while left < right:
    mid = (left + right) // 2
    if nums[mid] < target:
        left = mid + 1
    else:
        right = mid

return left
```

### 核心原则

不要混着背边界。固定一种区间语义，并让：

- 初始化；
- `while` 条件；
- 指针更新；

三者保持一致。

### Hot 100

- 35 搜索插入位置
- 34 查找第一个和最后一个位置
- 74 搜索二维矩阵

---

## 模板 27：旋转有序数组二分【A】

### 识别信号

整体不再完全有序，但任意一次二分后，**至少有一半仍然有序**。

```python
while left <= right:
    mid = (left + right) // 2

    if nums[mid] == target:
        return mid

    if nums[left] <= nums[mid]:
        # 左半边有序
        if nums[left] <= target < nums[mid]:
            right = mid - 1
        else:
            left = mid + 1
    else:
        # 右半边有序
        if nums[mid] < target <= nums[right]:
            left = mid + 1
        else:
            right = mid - 1
```

### Hot 100

- 33 搜索旋转排序数组
- 153 寻找旋转排序数组中的最小值

---

# 十一、栈与单调栈

## 模板 28：普通栈处理嵌套结构【S】

### 识别信号

- 括号匹配；
- 嵌套表达式；
- 需要保存“进入下一层之前”的状态。

```python
stack = []

for x in data:
    if x 是开始标记:
        stack.append(current_state)
        reset_or_enter_new_state()
    elif x 是结束标记:
        prev = stack.pop()
        current_state = merge(prev, current_state)
```

### Hot 100

- 20 有效的括号
- 394 字符串解码
- 155 最小栈（额外维护状态）

---

## 模板 29：单调栈【S】

### 识别信号

“右边/左边第一个比我大（小）的元素在哪里？”

以“下一个更大元素”为例：

```python
stack = []   # 保存尚未找到答案的下标

for i, x in enumerate(nums):
    while stack and nums[stack[-1]] < x:
        j = stack.pop()
        ans[j] = i - j
    stack.append(i)
```

### 核心 invariant

栈中元素保持某种单调性；新元素到来时，把已经可以确定答案的元素弹出。

### Hot 100

- 739 每日温度
- 84 柱状图中最大的矩形（单调递增栈）

---

# 十二、堆

## 模板 30：Top K 小顶堆【S】

### 识别信号

- 第 K 大；
- Top K；
- 数据持续到来，不希望整体排序。

```python
heap = []

for x in data:
    heapq.heappush(heap, x)
    if len(heap) > k:
        heapq.heappop(heap)

# heap[0] 是当前 Top K 中最小的，也就是第 K 大
```

### Hot 100

- 215 数组中的第 K 个最大元素
- 347 前 K 个高频元素

### 双堆维护中位数【A】

- `small`：最大堆（Python 中存负数）；
- `large`：最小堆；
- 始终维持两边大小差不超过 1。

对应：295 数据流的中位数。

---

# 十三、贪心

## 模板 31：维护“最远可达位置”【S】

### 识别信号

从左向右，每个位置都提供新的覆盖范围，问题问“能否到达”。

```python
farthest = 0

for i, step in enumerate(nums):
    if i > farthest:
        return False
    farthest = max(farthest, i + step)

return True
```

### Hot 100

- 55 跳跃游戏

---

## 模板 32：分层贪心 / 最少跳跃【A】

### 识别信号

每一步可以覆盖一个区间，要求最少多少步覆盖到终点。

```python
jumps = 0
current_end = 0
farthest = 0

for i in range(len(nums) - 1):
    farthest = max(farthest, i + nums[i])

    if i == current_end:
        jumps += 1
        current_end = farthest
```

可以把它理解成“不显式建队列的 BFS 分层”。

### Hot 100

- 45 跳跃游戏 II

---

# 十四、动态规划

## 模板 33：一维 DP【S】

### 写 DP 前的四步

1. `dp[i]` **到底表示什么**；
2. 写出状态转移；
3. 确定初始化；
4. 确定遍历顺序。

通用形式：

```python
dp = [0] * n
dp[0] = base

for i in range(1, n):
    dp[i] = transition(dp, i)

return dp[-1]
```

如果只依赖固定数量的前置状态，可以压缩空间：

```python
prev2, prev1 = ...
for ...:
    cur = transition(prev2, prev1)
    prev2, prev1 = prev1, cur
```

### Hot 100

- 70 爬楼梯
- 198 打家劫舍
- 152 乘积最大子数组（同时维护 max/min）

---

## 模板 34：0/1 背包【S】

### 识别信号

- 每个物品最多选一次；
- 问能否凑出某个容量 / 最大价值；
- 常见转化：数组能否分成两部分，使和相等。

```python
dp = [False] * (target + 1)
dp[0] = True

for x in nums:
    for j in range(target, x - 1, -1):
        dp[j] = dp[j] or dp[j - x]
```

### 为什么容量倒序

防止同一个物品在同一轮被重复使用。

### Hot 100

- 416 分割等和子集

---

## 模板 35：完全背包【S】

### 识别信号

每个元素可以被无限次使用。

求最少个数：

```python
dp = [float('inf')] * (target + 1)
dp[0] = 0

for amount in range(1, target + 1):
    for x in choices:
        if x <= amount:
            dp[amount] = min(dp[amount], dp[amount - x] + 1)
```

### 0/1 与完全背包最容易混的地方

核心区别不是名字，而是：**当前物品在本轮能不能再次被使用。**

### Hot 100

- 279 完全平方数
- 322 零钱兑换

---

## 模板 36：LIS “维护最小尾部”【A】

### 识别信号

最长严格递增子序列，追求 O(n log n)。

```python
tails = []

for x in nums:
    i = bisect_left(tails, x)
    if i == len(tails):
        tails.append(x)
    else:
        tails[i] = x

return len(tails)
```

### 关键理解

`tails[i]` 不是实际 LIS，而是“长度为 i+1 的递增子序列中，最小可能的结尾值”。结尾越小，未来越容易继续接元素。

### Hot 100

- 300 最长递增子序列

---

## 模板 37：二维网格 DP【S】

### 识别信号

从左上走到右下，只允许固定方向移动，求路径数 / 最小代价。

```python
dp = [[0] * n for _ in range(m)]

for i in range(m):
    for j in range(n):
        dp[i][j] = transition(
            dp[i - 1][j] if i > 0 else ...,
            dp[i][j - 1] if j > 0 else ...
        )
```

### Hot 100

- 62 不同路径
- 64 最小路径和

---

## 模板 38：双字符串二维 DP【S】

### LCS 型

定义：`dp[i][j]` 表示 `text1[:i]` 与 `text2[:j]` 的答案。

```python
for i in range(1, m + 1):
    for j in range(1, n + 1):
        if a[i - 1] == b[j - 1]:
            dp[i][j] = dp[i - 1][j - 1] + 1
        else:
            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
```

### 编辑距离型

若字符相同：继承 `dp[i-1][j-1]`；否则考虑：

- 删除；
- 插入；
- 替换。

```python
dp[i][j] = 1 + min(
    dp[i - 1][j],      # 删除
    dp[i][j - 1],      # 插入
    dp[i - 1][j - 1],  # 替换
)
```

### Hot 100

- 1143 最长公共子序列
- 72 编辑距离

---

# 十五、几个必须单独记住的技巧

这些不一定值得抽象成“大模板”，但在 Hot 100 里出现频率高，值得形成条件反射。

## 1. Kadane：最大子数组和

```python
cur = ans = nums[0]
for x in nums[1:]:
    cur = max(x, cur + x)
    ans = max(ans, cur)
```

对应：53 最大子数组和。

## 2. 中心扩展：回文子串

对每个位置分别考虑：

- 奇数长度中心 `(i, i)`；
- 偶数长度中心 `(i, i+1)`。

对应：5 最长回文子串。

## 3. XOR 消除成对元素

```python
ans = 0
for x in nums:
    ans ^= x
```

对应：136 只出现一次的数字。

## 4. Boyer-Moore 多数投票

维护候选人及票数；票数归零时更换候选人。

对应：169 多数元素。

## 5. 荷兰国旗三指针

维护三个区域：

```text
[0 ... left-1]      = 0
[left ... i-1]      = 1
[i ... right]       = 未处理
[right+1 ... end]   = 2
```

对应：75 颜色分类。

## 6. 下一个排列

固定步骤：

1. 从右向左找第一个下降点 `i`；
2. 从右找第一个大于 `nums[i]` 的数并交换；
3. 反转 `i+1:`。

对应：31 下一个排列。

---

# 十六、建议优先背熟的 S 级模板

如果时间有限，优先保证下面这些能不看答案写出骨架：

1. 哈希补数；
2. 左右双指针；
3. 快慢指针原地覆盖；
4. 可变滑动窗口；
5. 固定滑动窗口；
6. 前缀和 + 哈希；
7. 区间排序合并；
8. 链表 dummy；
9. 链表三指针反转；
10. 链表快慢指针；
11. 树自顶向下 DFS；
12. 树自底向上 DFS；
13. 层序 BFS；
14. BST 中序 / 值域；
15. Flood Fill；
16. 多源 BFS；
17. 拓扑排序；
18. 通用回溯；
19. 标准二分 / lower bound；
20. 普通栈；
21. 单调栈；
22. Top K 堆；
23. 最远可达贪心；
24. 一维 DP；
25. 0/1 背包；
26. 完全背包；
27. 二维网格 DP；
28. 双字符串二维 DP。

真正复习时，不需要一天背 28 个。正确方式是：**做题 → 识别模板 → 写模板 → 再做同模板变体**。

---

# 十七、面试时的“先判断再写代码”检查表

看到一道题，先快速问自己：

1. 题目要求的是不是**连续**区间？如果是，先想滑窗 / 前缀和。
2. 数据是否**有序**？如果是，先想双指针 / 二分。
3. 是否在找“另一个元素”？先想哈希。
4. 是否要求最近更大/更小？先想单调栈。
5. 是否要求 Top K / 第 K 大？先想堆。
6. 是否是链表？先检查 dummy、快慢指针、反转能否套用。
7. 是否是树？先判断答案是“祖先传下来”还是“子树算上去”。
8. 是否是网格连通性？先想 Flood Fill。
9. 是否有依赖关系？先想拓扑排序。
10. 是否枚举所有方案？先想回溯，并先定义 path / choices / end condition。
11. 是否有明显最优子结构？再进入 DP，并先写清楚 `dp[i]` 的定义。
12. DP 中每个元素能否重复选？决定 0/1 背包还是完全背包。

---

# 十八、与题解库的关系

本文件解决的是：

> **“这类题应该想到什么？”**

专题题解文件解决的是：

> **“这道具体题怎么完整实现？”**

因此推荐复习顺序：

```text
README.md
  ↓ 看今天要复习哪些题
TEMPLATES.md
  ↓ 回忆对应 Pattern 和代码骨架
solutions/*.md
  ↓ 卡住时再看具体标准答案
自己重新默写
  ↓
记录错误 / 更新掌握度
```

不要把 `solutions/` 当成第一入口。最终目标是看到题目后，先在脑中命中这里的模板，再完成具体实现。
