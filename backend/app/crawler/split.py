"""Split multi-problem documents before any LLM call (§7.3)."""

import re


def split_multiproblem_text(text: str, id_regex: str | None) -> list[str]:
    """Split on problem-ID matches; never ask the LLM to enumerate problems."""
    if not id_regex:
        return [text] if text.strip() else []
    matches = list(re.finditer(id_regex, text))
    if len(matches) <= 1:
        return [text] if text.strip() else []
    chunks: list[str] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        chunk = text[match.start():end].strip()
        if chunk:
            chunks.append(chunk)
    return chunks
