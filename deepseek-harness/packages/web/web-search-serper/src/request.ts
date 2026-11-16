/** Shared HTTP transport for Serper text and image searches. */

import { WebError } from '@deepseek-ai/dsh-web'

/** Resolved gateway options supplied by the plugin at mount time. */
export interface SerperRequestOptions {
  apiKey: string
  baseURL: string
  authMode: 'auto' | 'bearer' | 'x-api-key'
  country?: string
  language?: string
}

/** Narrow a parsed JSON value to an object. */
export function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

/** Resolve one supported route, rejecting paths and credentials in the gateway origin. */
export function serperEndpoint(baseURL: string, route: 'search' | 'images'): string {
  let url: URL
  try {
    url = new URL(baseURL)
  } catch (error) {
    throw new Error('web-search-serper: baseURL must be an HTTP(S) origin', { cause: error })
  }
  if (!['http:', 'https:'].includes(url.protocol) || url.pathname !== '/' || url.search || url.hash || url.username || url.password) {
    throw new Error('web-search-serper: baseURL must be an HTTP(S) origin without a path or credentials')
  }
  return new URL(`/serper/${route}`, url).href
}

/**
 * POST a query, with a second auth header only when automatic mode needs it.
 * @param endpoint - validated Serper route URL.
 * @param resultField - required array field in a successful response.
 * @param options - gateway credential and region configuration.
 * @param request - query and optional result bound.
 * @param signal - cancellation from the calling tool.
 * @returns parsed response containing the required result array.
 */
export async function requestSerper(
  endpoint: string,
  resultField: 'organic' | 'images',
  options: SerperRequestOptions,
  request: { readonly query: string; readonly maxResults?: number },
  signal?: AbortSignal,
): Promise<Record<string, unknown>> {
  const modes = options.authMode === 'auto' ? ['bearer', 'x-api-key'] as const : [options.authMode]
  const failures: string[] = []
  for (const mode of modes) {
    let response: Response
    try {
      response = await fetch(endpoint, {
        method: 'POST',
        redirect: 'error',
        headers: {
          accept: 'application/json',
          'content-type': 'application/json',
          ...mode === 'bearer'
            ? { authorization: `Bearer ${options.apiKey}` }
            : { 'x-api-key': options.apiKey },
        },
        body: JSON.stringify({
          q: request.query,
          ...request.maxResults === undefined ? {} : { num: request.maxResults },
          ...options.country === undefined ? {} : { gl: options.country },
          ...options.language === undefined ? {} : { hl: options.language },
        }),
        ...signal === undefined ? {} : { signal },
      })
    } catch (error) {
      if (error instanceof Error && error.name === 'AbortError') {
        throw new WebError('Serper search aborted', 'WEB_ABORTED', { cause: error })
      }
      throw new WebError('Serper search request failed', 'WEB_PROVIDER_ERROR', { cause: error })
    }
    if (!response.ok) {
      if (options.authMode === 'auto' && (response.status === 401 || response.status === 403)) {
        failures.push(`${mode}: HTTP ${response.status}`)
        continue
      }
      throw new WebError(`Serper API error (HTTP ${response.status})`, 'WEB_PROVIDER_ERROR')
    }
    let payload: unknown
    try {
      payload = await response.json()
    } catch (error) {
      if (error instanceof Error && error.name === 'AbortError') {
        throw new WebError('Serper search aborted', 'WEB_ABORTED', { cause: error })
      }
      if (options.authMode === 'auto') {
        failures.push(`${mode}: non-JSON response`)
        continue
      }
      throw new WebError('Serper returned non-JSON content', 'WEB_PROVIDER_ERROR', { cause: error })
    }
    if (isRecord(payload) && Array.isArray(payload[resultField])) return payload
    if (options.authMode === 'auto') {
      failures.push(`${mode}: no ${resultField} result array`)
      continue
    }
    throw new WebError(`Serper returned no ${resultField} result array`, 'WEB_PROVIDER_ERROR')
  }
  throw new WebError(`Serper returned no valid results (${failures.join('; ')})`, 'WEB_PROVIDER_ERROR')
}
