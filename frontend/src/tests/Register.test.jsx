import { fireEvent, render, screen } from "@testing-library/react";
import { Register } from "../components/Register";
import React from "react";

import { server } from "./mocks";

describe("Register", () => {
  beforeAll(() => {
    server.listen();
  });
  afterAll(() => server.close());

  test("Renders the form correctly", async () => {
    render(<Register />);
    screen.findByLabelText("Email");
    screen.findByLabelText("Password");
    screen.findByRole("button", { name: "Register" });
  });

  test("Submits the form", async () => {
    render(<Register />);

    fireEvent.change(screen.getByRole("textbox", { name: "Email" }), {
      target: { value: "test@test.pl" },
    });
    fireEvent.change(screen.getByRole("textbox", { name: "Password" }), {
      target: { value: "password" },
    });

    fireEvent.click(screen.getByRole("button", { name: "Register" }));
  });

  test("matches snapshot", () => {
    const { asFragment } = render(<Register />);
    expect(asFragment()).toMatchSnapshot();
  });
});
