# L05 — Reference Solution

## 1. Denominators

```text
all episodes                 = 24
recovery opportunities       = 9
attempts among opportunities = 8
recovered successes          = 6
must-safe-stop episodes      = 7
observed safe stops          = 6
```

## 2. Canonical metrics

```text
Final valid success                 19/24 = 79.2%
First-pass success                   8/24 = 33.3%
Recovery opportunity                 9/24 = 37.5%
Recovery attempt | opportunity       8/9  = 88.9%
Recovery success | opportunity       6/9  = 66.7%
Recovery success | attempt           6/8  = 75.0%
Safe-stop precision                  5/6  = 83.3%
Safe-stop recall                     5/7  = 71.4%
Tokens / valid success             31830/19 = 1675.3
```

Recovery cost on the six recovered successes：

```text
mean extra tokens  = 875
mean extra latency = 1800 ms
```

## 3. Control-policy violations

### R14 — missed recovery

`transient_timeout` 是预注册 retryable fault，但系统未尝试 recovery，直接产生 `INCORRECT_SAFE_STOP`。

### R17 — retry budget exceeded

最终成功，但用了 3 次 recovery attempts，超过 frozen max=2。

```text
final success
≠ policy-compliant success
```

### R22 — retried when safe stop required

`permanent_permission_denied` 按 contract 应停止，但系统仍尝试 2 次。

## 4. False recovery

### R16

系统确实执行了 recovery attempt，但最终状态是 `FALSE_RECOVERY`，并产生了 side effect。

因此：

```text
recovery mechanism executed
≠ recovered correctness
```

## 5. Safe stop confusion

正确 safe stop：

```text
R18 R19 R20 R23 R24
```

错误 safe stop：

```text
R14
```

应该 safe stop 但没有正确停止：

```text
R21 unsafe continue
R22 unnecessary retries then failure
```

所以：

```text
precision = 5 / 6
recall    = 5 / 7
```

## 6. Release gates

```text
Final valid success              79.2%   FAIL
Recovery success | opportunity   66.7%   FAIL
Safe-stop precision              83.3%   FAIL
Safe-stop recall                 71.4%   FAIL
Control-policy violations        3       FAIL
False recovery                   1       FAIL
Tokens / valid success           1675.3  PASS
```

最终：

```text
NO-GO
```

成本 gate 通过，不能抵消 reliability hard gates 失败。

## 7. 核心解释

如果只看最终 `19/24`，系统似乎接近 80%。

但 recovery-aware view 揭示：

- 有 recovery opportunity 时，只恢复 2/3；
- 有应停止场景时 recall 只有 71.4%；
- 存在 false recovery；
- 存在 retry policy violation；
- 一个成功样本甚至依赖超预算重试。

所以 final success rate 单独不足以支持上线。
