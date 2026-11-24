import { describe, expect, it } from "vitest";
import { GLOSSARY, splitGlossaryText } from "./index";

function terms(text: string): string[] {
  return splitGlossaryText(text).flatMap((token) =>
    token.type === "term" ? [token.value] : [],
  );
}

describe("splitGlossaryText", () => {
  it("links only the first occurrence of a term in one block", () => {
    expect(terms("The model learns. The model predicts.")).toEqual(["model"]);
  });

  it("prefers the longest matching phrase", () => {
    expect(terms("The SIR model spreads.")).toEqual(["SIR model"]);
    expect(terms("We compare SQL injection with SQL.")).toEqual([
      "SQL injection",
      "SQL",
    ]);
  });

  it("respects word boundaries", () => {
    expect(terms("Said HTML is not ML.")).toEqual(["HTML", "ML"]);
    expect(terms("A paragraph about shipping.")).toEqual([]);
  });

  it("handles simple plurals", () => {
    expect(terms("APIs and models.")).toEqual(["APIs", "models"]);
  });

  it("keeps ambiguous acronyms case sensitive", () => {
    expect(terms("She smiles at the SMILES string.")).toEqual(["SMILES"]);
    expect(terms("The acid test is simple, but ACID matters.")).toEqual([
      "ACID",
    ]);
  });

  it("matches aliases and alternative spellings", () => {
    expect(terms("Solving the Schrodinger equation.")).toEqual([
      "Schrodinger equation",
    ]);
    expect(terms("The train/test split avoids target leakage.")).toEqual([
      "train/test split",
      "target leakage",
    ]);
  });

  it("leaves prose without known terms alone", () => {
    expect(terms("A plain sentence about farmers.")).toEqual([]);
  });

  it("has unique ids and match forms", () => {
    const ids = new Set<string>();
    const forms = new Map<string, string>();

    for (const entry of GLOSSARY) {
      expect(ids.has(entry.id), `duplicate id: ${entry.id}`).toBe(false);
      ids.add(entry.id);

      for (const form of [entry.term, ...(entry.aliases ?? [])]) {
        expect(form).toBe(form.trim());
        const key = `${entry.caseSensitive ? "c" : "i"}:${form.toLowerCase()}`;
        expect(forms.has(key), `duplicate match form: ${form}`).toBe(false);
        forms.set(key, entry.id);
      }
    }
  });
});
