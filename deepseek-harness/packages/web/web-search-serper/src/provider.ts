/**
 * Map Serper's `/serper/search` results into the portable `ctx.web` search result.
 * @module @deepseek-ai/dsh-web-search-serper/provider
 */

import { WebError } from '@deepseek-ai/dsh-web'
import type { WebSearchProvider, WebSearchRequest, WebSearchResult, WebSearchSource } from '@deepseek-ai/dsh-web'
import { isRecord, requestSerper, serperEndpoint } from './request.ts'
import type { SerperRequestOptions } from './request.ts'

/** Provider id selected through `dsh-web` config. */
export const SERPER_PROVIDER_ID = 'serper'

/** Default gateway origin; deployments may set another origin. */
export const SERPER_DEFAULT_BASE_URL = 'https://yibuapi.com'

/** Resolved Serper HTTP options; tool-level budgets remain with `dsh-tool-web`. */
export type SerperSearchProviderOptions = SerperRequestOptions

/**
 * Convert only valid Serper organic entries into citeable web sources.
 * @param payload - parsed Serper response body.
 * @returns web search sources from valid organic entries.
 */
export function mapSerperResponse(payload: unknown): WebSearchResult {
  if (!isRecord(payload) || !Array.isArray(payload.organic)) {
    throw new WebError('Serper returned no organic result array', 'WEB_PROVIDER_ERROR')
  }
  const sources: WebSearchSource[] = []
  for (const entry of payload.organic) {
    if (!isRecord(entry) || typeof entry.link !== 'string') continue
    let url: URL
    try {
      url = new URL(entry.link)
    } catch {
      continue
    }
    if (url.protocol !== 'http:' && url.protocol !== 'https:') continue
    sources.push({
      url: url.href,
      ...typeof entry.title === 'string' && entry.title.length > 0 ? { title: entry.title } : {},
      ...typeof entry.snippet === 'string' && entry.snippet.length > 0 ? { snippet: entry.snippet } : {},
    })
  }
  return { sources, truncated: false }
}

/** Search through a Serper-compatible gateway without changing `web_search` limits. */
export class SerperSearchProvider implements WebSearchProvider {
  readonly id = SERPER_PROVIDER_ID
  private readonly endpoint: string

  constructor(private readonly options: SerperSearchProviderOptions) {
    this.endpoint = serperEndpoint(options.baseURL, 'search')
  }

  available(): boolean {
    return this.options.apiKey.length > 0
  }

  async search(request: WebSearchRequest, signal?: AbortSignal): Promise<WebSearchResult> {
    return mapSerperResponse(await requestSerper(this.endpoint, 'organic', this.options, request, signal))
  }
}
