export type GlossaryCategory =
  | "AI & data"
  | "Web & code"
  | "Science"
  | "Systems & security"
  | "World & work";

export interface GlossaryEntry {
  id: string;
  term: string;
  aliases?: string[];
  definition: string;
  category: GlossaryCategory;
  /**
   * Acronyms that are also ordinary words (SMILES, PIN, ACID, RAPTOR) only
   * match with their exact casing so we never underline normal prose.
   */
  caseSensitive?: boolean;
}

export type GlossaryToken =
  | { type: "text"; value: string }
  | { type: "term"; value: string; entry: GlossaryEntry };
