# 4. 代理配置模块 (`proxies.py`)

## 4.1 `AbuyunProxy` 类

## 请求代理 (`reqProxy`)
- **目的**: 获取Abuyun代理服务器配置。

- **用法**:
  ```python
  proxy = AbuyunProxy('username', 'password')
  proxies = proxy.reqProxy()
  ```

## Scrapy代理 (`scrapyProxy`)
- **目的**: 获取Scrapy爬虫使用的代理配置。

- **用法**:
  ```python
  proxy_server, proxy_auth = proxy.scrapyProxy()
  ```

## Chrome代理 (`chromeProxy`)
- **目的**: 生成Chrome浏览器插件，用于设置代理。

- **用法**:
  ```python
  plugin_path = proxy.chromeProxy()
  ```

## PhantomJS代理 (`phantomjsProxy`)
- **目的**: 获取PhantomJS使用的代理配置。

- **用法**:
  ```python
  service_args = proxy.phantomjsProxy()
  ```

# 4.2 `DuobeiProxy` 类

## 请求代理 (`reqProxy`)
- **目的**: 获取Duobei代理服务器配置。

- **用法**:
  ```python
  proxy = DuobeiProxy('username', 'password')
  proxies = proxy.reqProxy()
  ```

## Scrapy代理 (`scrapyProxy`)
- **目的**: 获取Scrapy爬虫使用的代理配置。

- **用法**:
  ```python
  proxy_server, proxy_auth = proxy.scrapyProxy()
  ```

## Chrome代理 (`chromeProxy`)
- **目的**: 生成Chrome浏览器插件，用于设置代理。

- **用法**:
  ```python
  plugin_path = proxy.chromeProxy()
  ```

## PhantomJS代理 (`phantomjsProxy`)
- **目的**: 获取PhantomJS使用的代理配置。

- **用法**:
  ```python
  service_args = proxy.phantomjsProxy()
  ```

# 4.3 `MayiProxy` 类

## 生成签名 (`generate_sign`)
- **目的**: 生成Mayi代理的认证签名。

- **参数**:
  - `app_key`: 应用密钥。
  - `secret`: 应用密钥对应的保密字段。
  - `mayi_url`: Mayi代理服务器地址。
  - `mayi_port`: Mayi代理服务器端口。

- **用法**:
  ```python
  headers, proxies = MayiProxy.generate_sign('app_key', 'secret', 'mayi_url', 'mayi_port')
  ```