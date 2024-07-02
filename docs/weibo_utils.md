# 6. 微博工具模块 (`weibo_utils.py`)

# 6.1 微博ID和MID转换

## 从微博URL获取ID (`get_id_from_url`)
- **目的**: 从微博页面URL中提取用户ID。

- **参数**:
  - `url`: 微博页面的URL。

- **用法**:
  ```python
  user_id = get_id_from_url('http://weibo.com/user/1234567890')
  ```

## 从微博URL获取MID (`get_mid_from_url`)
- **目的**: 从微博页面URL中提取用户MID。

- **参数**:
  - `url`: 微博页面的URL。

- **用法**:
  ```python
  user_mid = get_mid_from_url('http://weibo.com/user/u/1234567890')
  ```

## MID转ID (`mid_to_id`)
- **目的**: 将MID转换为微博用户ID。

- **参数**:
  - `mid`: 用户的MID。

- **用法**:
  ```python
  user_id = mid_to_id('K1uAj')
  ```

## ID转MID (`id_to_mid`)
- **目的**: 将微博用户ID转换为MID。

- **参数**:
  - `id_`: 用户的ID。

- **用法**:
  ```python
  user_mid = id_to_mid('1234567890')
  ```

## Base62转整数 (`str62_to_int`)
- **目的**: 将Base62编码的字符串转换为整数。

- **参数**:
  - `str62`: Base62编码的字符串。

- **用法**:
  ```python
  number = str62_to_int('A1')
  ```

## 整数转Base62 (`int_to_str62`)
- **目的**: 将整数转换为Base62编码的字符串。

- **参数**:
  - `int10`: 要转换的整数。

- **用法**:
  ```python
  str62 = int_to_str62(65)
  ```