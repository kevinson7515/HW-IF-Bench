import { afterEach, describe, expect, it, vi } from 'vitest'
import { Context } from '@deepseek-ai/cordis'
import WebRuntime from '@deepseek-ai/dsh-web'
import * as serperPlugin from '../src/index.ts'
import { mapSerperResponse, SerperSearchProvider } from '../src/provider.ts'
import { mapSerperImages, SerperImageSearchProvider } from '../src/image-provider.ts'

const options = { apiKey: 'test-key', baseURL: 'https://search.test', authMode: 'auto' as const }

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json' } })
}

afterEach(() => vi.unstubAllGlobals())

describe('Serper response mapping', () => {
  it('maps valid organic entries and omits invalid links', () => {
    expect(mapSerperResponse({ organic: [
      { link: 'https://a.test/article', title: 'A', snippet: 'Summary' },
      { link: 'javascript:alert(1)', title: 'Unsafe' },
      { link: 'https://b.test/' },
    ] })).toEqual({ sources: [
      { url: 'https://a.test/article', title: 'A', snippet: 'Summary' },
      { url: 'https://b.test/' },
    ], truncated: false })
  })

  it('rejects a success response without the organic array', () => {
    expect(() => mapSerperResponse({ message: 'ok' })).toThrow(expect.objectContaining({ code: 'WEB_PROVIDER_ERROR' }))
  })
})

describe('Serper image search', () => {
  it('maps image URLs, thumbnails, and source pages without unsafe URL schemes', () => {
    expect(mapSerperImages({ images: [
      { imageUrl: 'https://images.test/a.jpg', thumbnailUrl: 'https://images.test/a-small.jpg', link: 'https://source.test/a', title: 'A' },
      { imageUrl: 'javascript:alert(1)', title: 'Unsafe' },
      { imageUrl: 'https://images.test/b.png', link: 'file:///tmp/b', thumbnailUrl: 'not-a-url' },
    ] })).toEqual({ images: [
      { imageUrl: 'https://images.test/a.jpg', thumbnailUrl: 'https://images.test/a-small.jpg', sourceUrl: 'https://source.test/a', title: 'A' },
      { imageUrl: 'https://images.test/b.png' },
    ], truncated: false })
    expect(() => mapSerperImages({ organic: [] })).toThrow(expect.objectContaining({ code: 'WEB_PROVIDER_ERROR' }))
  })

  it('posts to /serper/images with the existing result bound and region fields', async () => {
    const calls: { url: string; init: RequestInit }[] = []
    vi.stubGlobal('fetch', vi.fn(async (url: string, init: RequestInit) => {
      calls.push({ url, init })
      return jsonResponse({ images: [{ imageUrl: 'https://images.test/a.jpg' }] })
    }))
    const provider = new SerperImageSearchProvider({ ...options, authMode: 'x-api-key', country: 'us', language: 'en' })
    await expect(provider.searchImages({ query: 'ships', maxResults: 3 })).resolves.toMatchObject({ images: [{ imageUrl: 'https://images.test/a.jpg' }] })
    expect(calls[0]?.url).toBe('https://search.test/serper/images')
    expect(calls[0]?.init.headers).toMatchObject({ 'x-api-key': 'test-key' })
    const body = calls[0]?.init.body
    if (typeof body !== 'string') throw new Error('Serper request body must be JSON text')
    expect(JSON.parse(body)).toEqual({ q: 'ships', num: 3, gl: 'us', hl: 'en' })
  })

  it('retries rejected Bearer auth and rejects a malformed second response', async () => {
    const headers: HeadersInit[] = []
    vi.stubGlobal('fetch', vi.fn(async (_url: string, init: RequestInit) => {
      headers.push(init.headers ?? {})
      return headers.length === 1 ? jsonResponse({ error: 'unauthorized' }, 401) : jsonResponse({ organic: [] })
    }))
    await expect(new SerperImageSearchProvider(options).searchImages({ query: 'ships' }))
      .rejects.toThrow(expect.objectContaining({ code: 'WEB_PROVIDER_ERROR' }))
    expect(headers).toEqual([
      expect.objectContaining({ authorization: 'Bearer test-key' }),
      expect.objectContaining({ 'x-api-key': 'test-key' }),
    ])
  })
})

describe('Serper provider', () => {
  it('uses the existing search request bounds and optional region fields', async () => {
    const calls: { url: string; init: RequestInit }[] = []
    vi.stubGlobal('fetch', vi.fn(async (url: string, init: RequestInit) => {
      calls.push({ url, init })
      return jsonResponse({ organic: [{ link: 'https://a.test', title: 'A' }] })
    }))
    const provider = new SerperSearchProvider({ ...options, authMode: 'bearer', country: 'us', language: 'en' })
    const signal = new AbortController().signal
    await expect(provider.search({ query: 'ships', maxResults: 3 }, signal)).resolves.toMatchObject({
      sources: [{ url: 'https://a.test/' }],
    })
    expect(calls).toHaveLength(1)
    expect(calls[0]?.url).toBe('https://search.test/serper/search')
    expect(calls[0]?.init).toMatchObject({ method: 'POST', redirect: 'error', signal })
    expect(calls[0]?.init.headers).toMatchObject({ authorization: 'Bearer test-key' })
    const body = calls[0]?.init.body
    if (typeof body !== 'string') throw new Error('Serper request body must be JSON text')
    expect(JSON.parse(body)).toEqual({ q: 'ships', num: 3, gl: 'us', hl: 'en' })
  })

  it('retries with X-API-KEY only for an invalid Bearer response', async () => {
    const headers: HeadersInit[] = []
    vi.stubGlobal('fetch', vi.fn(async (_url: string, init: RequestInit) => {
      headers.push(init.headers ?? {})
      return headers.length === 1 ? jsonResponse({ message: 'not results' }) : jsonResponse({ organic: [] })
    }))
    await expect(new SerperSearchProvider(options).search({ query: 'ships' }))
      .resolves.toMatchObject({ sources: [] })
    expect(headers).toEqual([
      expect.objectContaining({ authorization: 'Bearer test-key' }),
      expect.objectContaining({ 'x-api-key': 'test-key' }),
    ])
  })

  it('does not retry an HTTP 500 response', async () => {
    const fetchMock = vi.fn(async () => jsonResponse({}, 500))
    vi.stubGlobal('fetch', fetchMock)
    await expect(new SerperSearchProvider(options).search({ query: 'ships' }))
      .rejects.toThrow(expect.objectContaining({ code: 'WEB_PROVIDER_ERROR' }))
    expect(fetchMock).toHaveBeenCalledOnce()
  })

  it('preserves an abort as WEB_ABORTED', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => { throw new DOMException('aborted', 'AbortError') }))
    await expect(new SerperSearchProvider(options).search({ query: 'ships' }))
      .rejects.toThrow(expect.objectContaining({ code: 'WEB_ABORTED' }))
  })

  it('rejects invalid endpoint configuration at load', () => {
    expect(() => new SerperSearchProvider({ ...options, baseURL: 'file:///tmp/test' })).toThrow(/baseURL/)
    expect(() => new SerperSearchProvider({ ...options, baseURL: 'https://search.test/custom' })).toThrow(/baseURL/)
  })

  it('registers through ctx.web and uses its normal provider selection', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => jsonResponse({ organic: [] })))
    const ctx = new Context()
    await ctx.plugin(WebRuntime, { searchProvider: 'serper' })
    const fiber = await ctx.plugin(serperPlugin, { apiKey: 'test-key', baseURL: 'https://search.test' })
    await expect(ctx.web.search({ query: 'ships' })).resolves.toMatchObject({ sources: [] })
    await fiber.dispose()
    await expect(ctx.web.search({ query: 'ships' })).rejects.toThrow(expect.objectContaining({ code: 'WEB_PROVIDER_CONFIGURED_MISSING' }))
  })

  it('registers text search on a runtime without the image search API', () => {
    const registerSearchProvider = vi.fn()
    const ctx = { web: { registerSearchProvider } } as unknown as Context
    serperPlugin.apply(ctx, options)
    expect(registerSearchProvider).toHaveBeenCalledExactlyOnceWith(expect.objectContaining({ id: 'serper' }))
  })

  it('registers both search capabilities through the plugin fiber', async () => {
    vi.stubGlobal('fetch', vi.fn(async (url: string) => jsonResponse(url.endsWith('/images') ? { images: [] } : { organic: [] })))
    const ctx = new Context()
    await ctx.plugin(WebRuntime, { searchProvider: 'serper', imageSearchProvider: 'serper' })
    const fiber = await ctx.plugin(serperPlugin, { apiKey: 'test-key', baseURL: 'https://search.test' })
    await expect(ctx.web.searchImages({ query: 'ships' })).resolves.toEqual({ images: [], truncated: false })
    await fiber.dispose()
    await expect(ctx.web.searchImages({ query: 'ships' }))
      .rejects.toThrow(expect.objectContaining({ code: 'WEB_PROVIDER_CONFIGURED_MISSING' }))
  })
})
