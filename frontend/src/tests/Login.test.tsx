import { fireEvent, render, screen } from "@testing-library/react";
import { Login } from "../components/Login";

import { server } from "./mocks.ts";

describe("Login", () => {
  beforeAll(() => {
    server.listen();
  });
  afterAll(() => server.close());

  test("Renders the form correctly", async () => {
    render(<Login />);
    screen.findByLabelText("Adres e-mail");
    screen.findByLabelText("Hasło");
    screen.findByRole("button", { name: "Zaloguj" });
  });

  test("Submits the form", async () => {
    render(<Login />);

    fireEvent.change(screen.getByRole("textbox", { name: "Adres e-mail" }), {
      target: { value: "test@test.pl" },
    });
    fireEvent.change(screen.getByLabelText("Hasło"), {
      target: { value: "password" },
    });

    fireEvent.click(screen.getByRole("button", { name: "Zaloguj" }));
  });

  test("matches snapshot", () => {
    const { asFragment } = render(<Login />);
    expect(asFragment()).toMatchSnapshot();
  });
});
