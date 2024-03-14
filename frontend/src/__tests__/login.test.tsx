
import { render, screen } from "@testing-library/react";
import { Login } from "../routes/login.lazy";


test("Renders the main page", async () => {
    render(<Login />)
    await screen.findByText("Hello from Login!");
})