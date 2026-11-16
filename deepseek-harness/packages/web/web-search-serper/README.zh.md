---
description: "通过 Serper 兼容网关提供文本和图像搜索，同时保留 web 工具原有的结果上限与超时策略。"
kind: "package-reference"
---

# @deepseek-ai/dsh-web-search-serper

[English](README.md) | 中文

## 概述

部署需要通过 Serper 兼容网关而非 DeepSeek 搜索时，可以使用此包。它为现有 `web_search` 和可选的 `image_search` 工具注册文本与图像提供方。结果上限、超时、呈现方式和会话记录仍由 `dsh-tool-web` 负责。缺少 API 密钥时，两种提供方均不可用。

## 目录

- [使用此包](#use-this-package)
- [了解实现](#understand-the-implementation)
- [延伸阅读](#further-exploration)
- [模型体验](#model-experience)
- [已知限制与待办](#known-limitations-and-deferred-work)
- [开发备注](#dev-note)

-----

<a id="use-this-package"></a>
## 使用此包

将此提供方与 `dsh-web` 一起挂载；若还注册了同类的其他提供方，请指定 `searchProvider: serper` 与 `imageSearchProvider: serper`。在 `dsh-tool-web` 中设置 `imageSearch: true` 才会向模型公开图像工具。

### 适用情况

当网关从 `POST /serper/search` 返回 Serper 的 `organic` 数组、从 `POST /serper/images` 返回 `images` 数组时使用它。图像结果包含链接，而非下载后的图像字节。

### 最小配置

部署通过启动环境提供 `SERPER_API_KEY`；不要把密钥写进提交的补丁。

```yaml
- id: web
  name: '@deepseek-ai/dsh-web'
  config:
    searchProvider: serper
    imageSearchProvider: serper
- id: web-search-serper
  name: '@deepseek-ai/dsh-web-search-serper'
- id: tool-web
  name: '@deepseek-ai/dsh-tool-web'
  config:
    imageSearch: true
```

| 字段 | 默认值 | 含义 |
|---|---|---|
| `apiKey` | `$SERPER_API_KEY` | 凭据；为空时不可用 |
| `baseURL` | `https://yibuapi.com` | HTTP(S) 网关源地址；后接 `/serper/search` 或 `/serper/images` |
| `authMode` | `auto` | 先用 Bearer，授权失败或响应格式无效时改用 `X-API-KEY` |
| `country` | 未设置 | 可选的 Serper `gl` 国家代码 |
| `language` | 未设置 | 可选的 Serper `hl` 语言代码 |

[配置目录](../../../docs/config-catalog.zh.md#deepseek-aidsh-web-search-serper)列出允许的字段。请求的 `maxResults` 作为 Serper 的 `num` 发送；`ctx.web` 强制执行最终来源或图像上限。网络、HTTP 与无效响应失败映射为 `WEB_PROVIDER_ERROR`；取消映射为 `WEB_ABORTED`。

-----

<a id="understand-the-implementation"></a>
## 了解实现

<details>
<summary>实现内部细节——点击展开</summary>

提供方挂载时校验网关源地址，并把两种能力注册到 `ctx.web`。文本搜索仅接受 `organic` 数组，保留带可选标题与摘要的 HTTP(S) 来源链接。图像搜索仅接受 `images` 数组，保留 HTTP(S) 图像、缩略图与来源页面 URL。`src/index.ts` 负责配置，`src/request.ts` 负责共用 HTTP 行为，`src/provider.ts` 与 `src/image-provider.ts` 分别映射结果。

</details>

-----

<a id="further-exploration"></a>
## 延伸阅读

- [Web 子系统](../../../docs/subsystems/web.zh.md)——共享搜索结果与错误。
- [Web 包映射](../README.zh.md)——可用的搜索提供方。
- [Web 工具](../tool-web/README.zh.md)——面向模型的结果与超时上限。

-----

<a id="model-experience"></a>
## 模型体验

模型通过 `dsh-tool-web` 间接接收自然搜索来源或图像引用，也可能接收结构化的提供方或取消错误。

#### KV Cache 影响

不会直接使缓存失效；面向模型的工具声明由 `dsh-tool-web` 负责。

## 已知限制与待办

<a id="known-limitations-and-deferred-work"></a>

此提供方处理文本和图像搜索，但不抓取图像字节。

- 网关返回 HTTP 200 但不含对应路由要求的 `organic` 或 `images` 数组时，调用会失败，不会当作空结果。

<a id="dev-note"></a>
### 开发备注

<details>
<summary>维护者的工作上下文——点击展开</summary>

无。

</details>
