export function markdownExcerpt(markdown: string, maxChars = 180): string {
  const plain = markdown
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/[#*_`>~|-]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();

  if (plain.length <= maxChars) {
    return plain;
  }
  return `${plain.slice(0, maxChars).trimEnd()}…`;
}
