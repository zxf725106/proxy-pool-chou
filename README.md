# proxy-pool-chou

一个自动爬取和验证代理节点的工具，每天9点自动更新代理池。

## 功能特性

- 自动从多个免费代理网站爬取代理节点
- 验证代理的有效性和速度
- 使用SQLite数据库存储代理信息
- 提供REST API获取有效代理
- 每天9点自动更新代理池

## 安装

1. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用

### 运行调度器（自动更新）
```bash
python src/scheduler.py
```

### 运行API服务器
```bash
cd src && python main.py
```

API端点：
- `GET /proxies` - 获取所有有效代理（JSON格式）
- `GET /proxies?count=N` - 获取指定数量的代理（JSON格式）
- `GET /clash` - 获取所有代理的Clash Meta配置（YAML格式）
- `GET /clash?count=N` - 获取指定数量代理的Clash Meta配置（YAML格式）

### 生成Clash Meta配置文件
```bash
# 生成包含所有代理的配置
python generate_clash.py

# 生成指定数量代理的配置
python generate_clash.py --count 10

# 保存配置到文件
python generate_clash.py --count 20 --output my_proxies.yaml
```

## Clash Meta配置示例

访问 `http://localhost:5000/clash?count=5` 获取的配置：

```yaml
proxies:
- name: proxy-1
  port: 80
  server: 159.65.221.25
  type: http
  udp: true
- name: proxy-2
  port: 9080
  server: 8.213.215.187
  type: http
  udp: true
proxy-groups:
- interval: 300
  name: auto
  proxies:
  - proxy-1
  - proxy-2
  type: url-test
  url: http://www.gstatic.com/generate_204
```

你可以将此配置保存为 `.yaml` 文件导入到Clash Meta客户端中使用。

## 项目结构

- `src/crawler.py` - 代理爬虫
- `src/validator.py` - 代理验证器
- `src/database.py` - 数据库操作
- `src/scheduler.py` - 定时任务调度器
- `src/main.py` - Flask API服务器
- `requirements.txt` - Python依赖