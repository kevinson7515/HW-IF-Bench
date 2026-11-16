/** Serper `/serper/images` provider for image references, not image bytes. */

import { WebError } from '@deepseek-ai/dsh-web'
import type {
  WebImageSearchItem,
  WebImageSearchProvider,
  WebImageSearchRequest,
  WebImageSearchResult,
} from '@deepseek-ai/dsh-web'
import { isRecord, requestSerper, serperEndpoint } from './request.ts'
import type { SerperRequestOptions } from './request.ts'

/** Provider id selected through `dsh-web` image-search config. */
export const SERPER_IMAGE_PROVIDER_ID = 'serper'

function httpUrl(value: unknown): string | undefined {
  if (typeof value !== 'string') return undefined
  try {
    const url = new URL(value)
    return url.protocol === 'http:' || url.protocol === 'https:' ? url.href : undefined
  } catch {
    return undefined
  }
}

/**
 * Keep image references with usable HTTP(S) URLs from a Serper response.
 * @param payload - parsed `/serper/images` response body.
 * @returns normalized image references in provider order.
 */
export function mapSerperImages(payload: unknown): WebImageSearchResult {
  if (!isRecord(payload) || !Array.isArray(payload.images)) {
    throw new WebError('Serper returned no images result array', 'WEB_PROVIDER_ERROR')
  }
  const images: WebImageSearchItem[] = []
  for (const entry of payload.images) {
    if (!isRecord(entry)) continue
    const imageUrl = httpUrl(entry.imageUrl)
    if (imageUrl === undefined) continue
    const thumbnailUrl = httpUrl(entry.thumbnailUrl)
    const sourceUrl = httpUrl(entry.link)
    images.push({
      imageUrl,
      ...thumbnailUrl === undefined ? {} : { thumbnailUrl },
      ...sourceUrl === undefined ? {} : { sourceUrl },
      ...typeof entry.title === 'string' && entry.title.length > 0 ? { title: entry.title } : {},
    })
  }
  return { images, truncated: false }
}

/** Search image references through the Serper-compatible gateway. */
export class SerperImageSearchProvider implements WebImageSearchProvider {
  readonly id = SERPER_IMAGE_PROVIDER_ID
  private readonly endpoint: string

  constructor(private readonly options: SerperRequestOptions) {
    this.endpoint = serperEndpoint(options.baseURL, 'images')
  }

  available(): boolean {
    return this.options.apiKey.length > 0
  }

  async searchImages(request: WebImageSearchRequest, signal?: AbortSignal): Promise<WebImageSearchResult> {
    return mapSerperImages(await requestSerper(this.endpoint, 'images', this.options, request, signal))
  }
}
