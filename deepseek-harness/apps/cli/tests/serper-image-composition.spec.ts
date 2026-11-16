/** The real Loader exposes Serper image references through the opt-in tool. */

import { resolve } from 'node:path'
import { afterEach, describe, expect, it, vi } from 'vitest'
import type { Context } from '@deepseek-ai/cordis'
import { boot } from '@deepseek-ai/dsh-app-boot'
import { ToolCallId } from '@deepseek-ai/dsh-llm'
import SystemPrompt from '@deepseek-ai/dsh-system-prompt'
import ToolRuntime from '@deepseek-ai/dsh-tools'
import WebRuntime from '@deepseek-ai/dsh-web'
import * as Serper from '../../../packages/web/web-search-serper/src/index.ts'
import * as ToolWeb from '../../../packages/web/tool-web/src/index.ts'

const configPath = resolve(import.meta.dirname, 'fixtures/serper-image.cordis.yml')
const liveContexts = new Set<Context>()

afterEach(async () => {
  vi.unstubAllGlobals()
  await Promise.all([...liveContexts].map(ctx => ctx.fiber.dispose()))
  liveContexts.clear()
})

describe('Serper image-search composition', () => {
  it('registers image_search and retains bounded image links in the tool result', async () => {
    const requests: string[] = []
    vi.stubGlobal('fetch', vi.fn(async (url: string) => {
      requests.push(url)
      return new Response(JSON.stringify({ images: [
        { imageUrl: 'https://images.test/a.jpg', link: 'https://source.test/a', title: 'A' },
        { imageUrl: 'https://images.test/b.jpg' },
      ] }), { status: 200, headers: { 'content-type': 'application/json' } })
    }))
    const ctx = await boot('serper-image-test', configPath, [], (context) => {
      liveContexts.add(context)
      context.loader.builtins['serper-test-system-prompt'] = SystemPrompt
      context.loader.builtins['serper-test-tools'] = ToolRuntime
      context.loader.builtins['serper-test-web'] = WebRuntime
      context.loader.builtins['serper-test-provider'] = Serper
      context.loader.builtins['serper-test-tool-web'] = ToolWeb
    })
    expect(ctx.tools.schemas().map(schema => schema.name)).toEqual(['image_search'])
    const result = await ctx.tools.execute({
      callId: ToolCallId('serper-image-test-call'),
      name: 'image_search',
      arguments: { query: 'vessel' },
      signal: new AbortController().signal,
    })
    expect(result.isError).toBe(false)
    expect(result.value).toEqual({
      images: [{ imageUrl: 'https://images.test/a.jpg', sourceUrl: 'https://source.test/a', title: 'A' }],
      truncated: true,
    })
    expect(requests).toEqual(['https://search.test/serper/images'])
  })
})
