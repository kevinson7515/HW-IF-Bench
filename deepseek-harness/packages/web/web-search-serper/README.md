---
description: "Use a Serper-compatible gateway for text and image searches while retaining the web tools' result limits and timeout policy."
kind: "package-reference"
---

# @deepseek-ai/dsh-web-search-serper

English | [中文](README.zh.md)

## Summary

Use this package when a deployment searches through a Serper-compatible gateway instead of DeepSeek search. It registers text and image providers for the existing `web_search` tool and the optional `image_search` tool. Their result limits, timeouts, presentation, and session logging remain owned by `dsh-tool-web`. A missing API key makes both providers unavailable.

## Table of Contents

- [Use this package](#use-this-package)
- [Understand the implementation](#understand-the-implementation)
- [Further Exploration](#further-exploration)
- [Model Experience](#model-experience)
- [Known Limitations and Deferred Work](#known-limitations-and-deferred-work)
- [Dev Note](#dev-note)

-----

<a id="use-this-package"></a>
## Use this package

Mount this provider alongside `dsh-web`, then select `searchProvider: serper` and `imageSearchProvider: serper` if other providers of either kind are registered. Enable `imageSearch: true` in `dsh-tool-web` to expose the image tool.

### When to choose it

Choose it when the gateway returns Serper's `organic` array from `POST /serper/search` and `images` array from `POST /serper/images`. Image results contain links, not downloaded image bytes.

### Minimal configuration

The deployment supplies `SERPER_API_KEY` through its launch environment; do not put the key in a committed patch.

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

| Field | Default | Meaning |
|---|---|---|
| `apiKey` | `$SERPER_API_KEY` | Credential; empty means unavailable |
| `baseURL` | `https://yibuapi.com` | HTTP(S) gateway origin; `/serper/search` or `/serper/images` is appended |
| `authMode` | `auto` | Bearer first, then `X-API-KEY` on authorization or response-format failure |
| `country` | unset | Optional Serper `gl` country |
| `language` | unset | Optional Serper `hl` language |

The [configuration catalog](../../../docs/config-catalog.md#deepseek-aidsh-web-search-serper) lists the accepted fields. A request's `maxResults` is sent as Serper `num`; `ctx.web` enforces the returned source or image limit. Network, HTTP, and invalid-response failures become `WEB_PROVIDER_ERROR`; cancellation becomes `WEB_ABORTED`.

-----

<a id="understand-the-implementation"></a>
## Understand the implementation

<details>
<summary>Implementation internals — click to expand</summary>

The provider validates the gateway origin when mounted and registers both capabilities with `ctx.web`. Text search accepts only an `organic` array and keeps HTTP(S) source links with optional titles and snippets. Image search accepts only an `images` array and keeps HTTP(S) image, thumbnail, and source-page URLs. `src/index.ts` owns configuration; `src/request.ts` owns shared HTTP behavior; `src/provider.ts` and `src/image-provider.ts` map the respective results.

</details>

-----

<a id="further-exploration"></a>
## Further Exploration

- [Web subsystem](../../../docs/subsystems/web.md) — shared search results and errors.
- [Web package map](../README.md) — available search providers.
- [Web tool](../tool-web/README.md) — model-facing result and timeout limits.

-----

<a id="model-experience"></a>
## Model Experience

Indirectly, through `dsh-tool-web`, the model receives organic sources or image references, or a structured provider/cancellation error.

#### KV Cache effect

No direct invalidation; `dsh-tool-web` owns model-visible tool declarations.

## Known Limitations and Deferred Work

<a id="known-limitations-and-deferred-work"></a>

This provider serves text and image search, but does not retrieve the image bytes.

- A gateway that returns HTTP 200 without the route's required `organic` or `images` array is treated as a failure, not an empty search.

<a id="dev-note"></a>
### Dev Note

<details>
<summary>Working context for maintainers — click to expand</summary>

None.

</details>
