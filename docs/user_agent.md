# 3. 用户代理模块 (`user_agent.py`)

**目的**: 提供随机的用户代理字符串，用于模拟浏览器访问。

## 获取用户代理 (`get`)
- **参数**:
  - `ua_type`: 用户代理类型，如`"chrome"`, `"opera"`, `"firefox"`等。

- **用法**:
  ```python
  user_agent = get('chrome')
  ```