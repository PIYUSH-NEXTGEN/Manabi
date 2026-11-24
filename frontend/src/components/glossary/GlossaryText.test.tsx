import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import { GlossaryText } from "./GlossaryText";

describe("GlossaryText", () => {
  it("shows a plain definition when a term is hovered", async () => {
    const user = userEvent.setup();
    render(
      <p>
        <GlossaryText text="SGP4 predicts where the ISS will be." />
      </p>,
    );

    await user.hover(screen.getByRole("button", { name: "SGP4" }));

    const tooltip = await screen.findByRole("tooltip");
    expect(tooltip).toHaveTextContent("SGP4");
    expect(tooltip).toHaveTextContent(/standard model/i);
  });

  it("pins on click and closes with Escape", async () => {
    const user = userEvent.setup();
    render(
      <p>
        <GlossaryText text="The ISS orbits Earth." />
      </p>,
    );

    const term = screen.getByRole("button", { name: "ISS" });
    await user.click(term);
    expect(await screen.findByRole("tooltip")).toHaveTextContent(
      /space station/i,
    );

    await user.unhover(term);
    expect(screen.getByRole("tooltip")).toBeInTheDocument();

    await user.keyboard("{Escape}");
    await waitFor(() =>
      expect(screen.queryByRole("tooltip")).not.toBeInTheDocument(),
    );
  });

  it("leaves prose without known terms alone", () => {
    render(
      <p>
        <GlossaryText text="A plain sentence about farmers." />
      </p>,
    );

    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });
});
