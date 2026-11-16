# 固定版本 CSV API

pandas 2.2.3 的 read_csv 文档说明 low_memory 允许 C 解析器分块处理，但默认仍返回一个 DataFrame，chunksize 或 iterator 才将分块暴露给调用方。memory_map 在传入文件路径时可用。Polars 1.31.0 API 源码含 read_csv 和 scan_csv 的参数文档。附件没有统一数据和硬件下的峰值 RSS 实测；可根据接口行为解释内存机制。

## 可核验来源

- https://pandas.pydata.org/pandas-docs/version/2.2/reference/api/pandas.read_csv.html
- https://github.com/pola-rs/polars/blob/py-1.31.0/py-polars/polars/io/csv/functions.py
