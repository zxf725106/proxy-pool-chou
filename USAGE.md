# 代理池工具使用指南

## 项目概述
这是一个自动爬取和验证代理节点的工具，每天9点自动更新代理池，提供REST API和Clash Meta配置生成。

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行一次代理更新
```bash
cd src
python -c "from scheduler import ProxyScheduler; s = ProxyScheduler(); s.update_proxies()"
```

### 3. 启动API服务器
```bash
cd src
python main.py
```

### 4. 测试API
```bash
# 获取JSON格式代理
curl http://localhost:5000/proxies?count=5

# 获取Clash配置
curl "http://localhost:5000/clash?count=10" > config.yaml
```

## 主要功能

### 🔄 自动更新
- 每天早上9点自动爬取新代理
- 验证代理有效性
- 更新数据库

### 🌐 REST API
- `GET /proxies` - 获取所有代理
- `GET /proxies?count=N` - 获取指定数量代理
- `GET /clash` - 生成Clash Meta配置
- `GET /clash?count=N` - 生成指定数量的Clash配置

### 📄 配置生成
```bash
# 生成Clash配置文件
python generate_clash.py --count 20 --output proxies.yaml
```

## 文件结构
```
proxy-pool-chou/
├── src/                    # 源代码目录
│   ├── crawler.py         # 代理爬虫
│   ├── validator.py       # 代理验证器
│   ├── database.py        # 数据库操作
│   ├── scheduler.py       # 定时任务
│   └── main.py           # Flask API服务器
├── generate_clash.py      # Clash配置生成脚本
├── requirements.txt       # Python依赖
├── README.md             # 项目说明
└── clash_config.yaml     # 示例Clash配置
```

## 使用场景

### 在Python项目中使用
```python
import requests

# 获取代理
response = requests.get('http://localhost:5000/proxies?count=1')
proxy = response.json()[0]

# 使用代理
proxies = {
    'http': f"http://{proxy['ip']}:{proxy['port']}",
    'https': f"http://{proxy['ip']}:{proxy['port']}"
}

# 发送请求
response = requests.get('http://example.com', proxies=proxies)
```

### Clash Meta客户端
1. 生成配置文件：`python generate_clash.py --count 50 --output config.yaml`
2. 导入到Clash Meta客户端
3. 选择"auto"代理组自动切换

## 注意事项

- 免费代理质量不稳定，建议在使用前测试
- 代理池每天自动更新，无需手动维护
- API服务器运行在5000端口，确保端口可用
- 数据库文件proxies.db包含所有代理数据

## 技术栈

- **后端**: Python Flask
- **数据库**: SQLite
- **爬虫**: BeautifulSoup + requests
- **配置**: PyYAML
- **调度**: schedule库

## 许可证

MIT License