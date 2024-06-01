import { fireEvent, render, screen } from "@testing-library/react";
import { Login } from "../components/Login";
import React from "react";

import { server } from "./mocks";

describe("Login", () => {
  beforeAll(() => {
    server.listen();
  });
  afterAll(() => server.close());

  test("Renders the form correctly", async () => {
    render(<Login />);
    screen.findByLabelText("Email");
    screen.findByLabelText("Password");
    screen.findByRole("button", { name: "Login" });
  });

  test("Submits the form", async () => {
    render(<Login />);

    fireEvent.change(screen.getByRole("textbox", { name: "Email" }), {
      target: { value: "test@test.pl" },
    });
    fireEvent.change(screen.getByRole("textbox", { name: "Password" }), {
      target: { value: "password" },
    });

    fireEvent.click(screen.getByRole("button", { name: "Login" }));
  });

  test("matches snapshot", () => {
    const { asFragment } = render(<Login />);
    expect(asFragment()).toMatchSnapshot();
  });
});
