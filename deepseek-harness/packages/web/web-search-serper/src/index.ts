/**
 * Serper text and image search providers for the existing `ctx.web` service.
 * @module @deepseek-ai/dsh-web-search-serper
 */

import type { Context } from '@deepseek-ai/cordis'
import { launchEnvironmentOf } from '@deepseek-ai/dsh-launch-environment'
import z from '@deepseek-ai/schemastery'
import type {} from '@deepseek-ai/dsh-web'
import { SerperSearchProvider, SERPER_DEFAULT_BASE_URL } from './provider.ts'
import { SerperImageSearchProvider } from './image-provider.ts'

export { SerperSearchProvider, SERPER_DEFAULT_BASE_URL, SERPER_PROVIDER_ID } from './provider.ts'
export { SerperImageSearchProvider, SERPER_IMAGE_PROVIDER_ID, mapSerperImages } from './image-provider.ts'
export type { SerperSearchProviderOptions } from './provider.ts'

/** Cordis plugin name used by loader diagnostics. */
export const name = 'web-search-serper'

/** The web service this provider registers into. */
export const inject = ['web']

/** Deployment options; the model-facing tool retains its own result and timeout limits. */
export interface Config {
  /** Secret key; falls back to `$SERPER_API_KEY`. Empty makes the provider unavailable. */
  apiKey?: string
  /** Gateway origin; `/serper/search` and `/serper/images` are appended. */
  baseURL?: string
  /** Authentication header, with automatic retry on rejected/nonstandard Bearer responses. */
  authMode?: 'auto' | 'bearer' | 'x-api-key'
  /** Optional Serper `gl` country code. */
  country?: string
  /** Optional Serper `hl` language code. */
  language?: string
}

export const Config: z<Config> = z.object({
  apiKey: z.string(),
  baseURL: z.string(),
  authMode: z.union(['auto', 'bearer', 'x-api-key'] as const),
  country: z.string(),
  language: z.string(),
})

/** Register Serper for both text and image searches on the shared web service. */
export function apply(ctx: Context, config: Config): void {
  const options = {
    apiKey: config.apiKey ?? launchEnvironmentOf(ctx).get('SERPER_API_KEY')?.value ?? '',
    baseURL: config.baseURL ?? SERPER_DEFAULT_BASE_URL,
    authMode: config.authMode ?? 'auto',
    ...config.country === undefined ? {} : { country: config.country },
    ...config.language === undefined ? {} : { language: config.language },
  }
  ctx.web.registerSearchProvider(new SerperSearchProvider(options))
  ctx.web.registerImageSearchProvider(new SerperImageSearchProvider(options))
}
