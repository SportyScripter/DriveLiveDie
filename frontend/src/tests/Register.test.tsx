import { fireEvent, render, screen } from "@testing-library/react";
import { Register } from "../components/Register";

import { server } from "./mocks.ts";

describe("Register", () => {
  beforeAll(() => {
    server.listen();
  });
  afterAll(() => server.close());

  test("Renders the form correctly", async () => {
    render(<Register />);
    screen.findByLabelText("Adres e-mail");
    screen.findByLabelText("Hasło");
    screen.findByRole("button", { name: "Zarejestruj" });
  });

  test("Submits the form", async () => {
    render(<Register />);

    fireEvent.change(screen.getByRole("textbox", { name: "Adres e-mail" }), {
      target: { value: "test@test.pl" },
    });
    fireEvent.change(screen.getByLabelText("Hasło"), {
      target: { value: "password" },
    });

    fireEvent.click(screen.getByRole("button", { name: "Zarejestruj" }));
  });

  test("matches snapshot", () => {
    const { asFragment } = render(<Register />);
    expect(asFragment()).toMatchSnapshot();
  });
});
