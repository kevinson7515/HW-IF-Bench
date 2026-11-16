/** Complete system-prompt replacement for one fresh benchmark process. */
export const name = 'benchmark-prompt';
export const inject = ['systemPrompt'];

/**
 * Register the literal benchmark prompt while retaining tool schemas and context.
 * @param {import('@deepseek-ai/cordis').Context} ctx - Plugin context.
 * @param {{ text: string }} config - Complete, nonempty system prompt.
 * @returns {void}
 */
export function apply(ctx, config) {
  if (typeof config?.text !== 'string' || !config.text.trim()) {
    throw new Error('benchmark-prompt requires nonempty config.text');
  }
  ctx.effect(() => ctx.systemPrompt.section({
    name: 'benchmark:complete',
    order: 0,
    text: config.text,
    complete: true,
    interpolate: false,
  }), 'benchmark.complete-prompt');
}
