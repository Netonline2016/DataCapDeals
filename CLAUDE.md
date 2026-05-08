# Filfox DataCap Deal Fetcher

## 项目概述

从 Filfox API 获取指定 Filecoin Provider 或 Client 的全部 Deal 条目，输出为 JSON 与 CSV 格式。

## 项目结构

```
filfox-datacap/
├── src/
│   ├── __init__.py
│   ├── api.py          # FilfoxClient：HTTP 客户端、自动分页、重试
│   ├── models.py       # Deal 数据模型（dataclass）
│   ├── output.py       # JSON/CSV 序列化
│   └── main.py         # CLI 入口
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_main.py
│   ├── test_models.py
│   └── test_output.py
├── requirements.txt    # requests
└── README.md
```

## 常用命令

```bash
# 安装依赖
pip install -r requirements.txt

# 运行测试
pytest tests/ -v

# 获取指定地址的 deals
python3 -m src.main --address f01313
python3 -m src.main --address f1ogcgz4a6bmsmcdk3nnksw4yac5syis4tpqxd7by --output-dir ./deals

# 调整分页延迟（默认 500ms）
python3 -m src.main --address f01313 --delay 1000
```

## API 说明

- 端点：`GET https://filfox.info/api/v1/deal/list`
- 过滤参数：`address`（支持 provider ID 或 client address）
- 分页参数：`page`（0-based）、`pageSize`
- 返回：`{"totalCount": int, "deals": [...]}`

## 注意事项

- Filfox 对请求频率有限制，脚本已内置 User-Agent 与 429 退避重试
- 默认每页请求间隔 500ms，可根据网络情况调整 `--delay`
- 大量数据获取可能需要较长时间（例如 13 万条约需 11 分钟）
