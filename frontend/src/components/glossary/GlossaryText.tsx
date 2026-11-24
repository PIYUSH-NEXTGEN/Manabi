import { Fragment } from "react";
import { splitGlossaryText } from "@/lib/glossary";
import { GlossaryTerm } from "./GlossaryTerm";

interface GlossaryTextProps {
  text: string;
}

export function GlossaryText({ text }: GlossaryTextProps) {
  const tokens = splitGlossaryText(text);

  return (
    <span>
      {tokens.map((token, index) =>
        token.type === "term" ? (
          <GlossaryTerm key={`${token.entry.id}-${index}`} entry={token.entry}>
            {token.value}
          </GlossaryTerm>
        ) : (
          <Fragment key={`text-${index}`}>{token.value}</Fragment>
        ),
      )}
    </span>
  );
}
