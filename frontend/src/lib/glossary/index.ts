import { AI_TERMS } from "./terms-ai";
import { EXTRA_TERMS } from "./terms-extra";
import { SCIENCE_TERMS } from "./terms-science";
import { SYSTEMS_TERMS } from "./terms-systems";
import { WEB_TERMS } from "./terms-web";
import type {
  GlossaryEntry,
  GlossaryToken,
} from "./types";

export type { GlossaryCategory, GlossaryEntry, GlossaryToken } from "./types";

export const GLOSSARY: GlossaryEntry[] = [
  ...AI_TERMS,
  ...WEB_TERMS,
  ...SCIENCE_TERMS,
  ...SYSTEMS_TERMS,
  ...EXTRA_TERMS,
];

interface Candidate {
  entry: GlossaryEntry;
  needle: string;
  needleLower: string;
  caseSensitive: boolean;
}

const WORD_CHAR = /[\p{L}\p{N}]/u;

function isWordChar(char: string | undefined): boolean {
  return char !== undefined && WORD_CHAR.test(char);
}

const candidatesByFirst = new Map<string, Candidate[]>();

for (const entry of GLOSSARY) {
  for (const form of [entry.term, ...(entry.aliases ?? [])]) {
    const first = form.charAt(0).toLowerCase();
    if (!first) continue;
    const list = candidatesByFirst.get(first) ?? [];
    list.push({
      entry,
      needle: form,
      needleLower: form.toLowerCase(),
      caseSensitive: entry.caseSensitive === true,
    });
    candidatesByFirst.set(first, list);
  }
}

for (const list of candidatesByFirst.values()) {
  list.sort((a, b) => b.needle.length - a.needle.length);
}

function matchEnd(
  text: string,
  start: number,
  candidate: Candidate,
): number | null {
  const end = start + candidate.needle.length;
  if (end > text.length) return null;

  const slice = text.slice(start, end);
  const same =
    candidate.caseSensitive === true
      ? slice === candidate.needle
      : slice.toLowerCase() === candidate.needleLower;
  if (!same) return null;

  if (isWordChar(text[start - 1])) return null;
  if (!isWordChar(text[end])) return end;
  if (
    (text[end] === "s" || text[end] === "S") &&
    !isWordChar(text[end + 1])
  ) {
    return end + 1;
  }
  return null;
}

export function splitGlossaryText(text: string): GlossaryToken[] {
  if (!text) return [];

  const tokens: GlossaryToken[] = [];
  const used = new Set<string>();
  let cursor = 0;
  let index = 0;

  while (index < text.length) {
    const list = candidatesByFirst.get(text.charAt(index).toLowerCase());
    let found: { entry: GlossaryEntry; end: number } | null = null;

    if (list) {
      for (const candidate of list) {
        const end = matchEnd(text, index, candidate);
        if (end !== null) {
          found = { entry: candidate.entry, end };
          break;
        }
      }
    }

    if (!found) {
      index += 1;
      continue;
    }

    if (index > cursor) {
      tokens.push({ type: "text", value: text.slice(cursor, index) });
    }

    const value = text.slice(index, found.end);
    if (used.has(found.entry.id)) {
      tokens.push({ type: "text", value });
    } else {
      tokens.push({ type: "term", value, entry: found.entry });
      used.add(found.entry.id);
    }

    index = found.end;
    cursor = found.end;
  }

  if (cursor < text.length) {
    tokens.push({ type: "text", value: text.slice(cursor) });
  }

  return tokens;
}
