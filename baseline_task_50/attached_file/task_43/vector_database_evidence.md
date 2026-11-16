# 三种向量数据库的来源摘记

- Qdrant 官方 Query API 可组合稠密、稀疏查询，通过预取和融合组合候选。元数据采用 payload 条件，性能建议包含 payload 索引。本地 quickstart 提供单容器。https://qdrant.tech/documentation/search/hybrid-queries/ ；https://qdrant.tech/documentation/quickstart/ ；https://qdrant.tech/documentation/search/filtering/
- Weaviate 官方 hybrid 把关键词 BM25 与向量搜索结果融合，alpha 控制相对权重，支持属性过滤。本地运行有 Docker 与 Compose。https://docs.weaviate.io/weaviate/search/hybrid ；https://docs.weaviate.io/deploy/installation-guides/docker-installation
- Milvus 多向量 hybrid_search 支持多路 ANN 请求和重排。过滤有标准元数据预过滤和迭代过滤。部署说明区分 Lite、Standalone 和 Distributed，模式与版本决定能力和运维组件。https://milvus.io/docs/multi-vector-search.md ；https://milvus.io/docs/filtered-search.md ；https://milvus.io/docs/v2.5.x/install-overview.md
- ANN-Benchmarks 是独立开源项目，重点是 ANN 的吞吐量和召回权衡。见附件项目说明；运行配置与是否覆盖稀疏/混合/过滤需分别查看。Qdrant 自己发布的 filtered ANN 测试则为厂商测试。https://github.com/erikbern/ann-benchmarks ；https://qdrant.tech/benchmarks/


## 可核验来源

- https://qdrant.tech/documentation/search/hybrid-queries/
- https://qdrant.tech/documentation/quickstart/
- https://qdrant.tech/benchmarks/
- https://docs.weaviate.io/weaviate/search/hybrid
- https://docs.weaviate.io/deploy/installation-guides/docker-installation
- https://milvus.io/docs/multi-vector-search.md
- https://milvus.io/docs/filtered-search.md
- https://milvus.io/docs/v2.5.x/install-overview.md
- https://github.com/erikbern/ann-benchmarks
