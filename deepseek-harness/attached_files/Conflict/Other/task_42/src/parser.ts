export function parseTokens(text: string): string[] {
  const tokens = text.trim() ? text.trim().split(/\s+/) : [];
  if (tokens.length === 0) throw new RangeError("empty input");
  return tokens;
}
