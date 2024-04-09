
import { render, screen } from "@testing-library/react";
import { Index } from "../routes/index.lazy";

test("Renders the main page", async () => {
    render(<Index />)
    await screen.findByText("Hello!");
})