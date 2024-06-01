import { render, screen } from "@testing-library/react";
import { Users } from "../components/Users";
import React from "react";

import { server } from "./mocks";

describe("Users", () => {
  beforeAll(() => {
    server.listen();
  });
  afterAll(() => server.close());

  test("Renders the view correctly", async () => {
    render(<Users />);
    screen.findByText("Users");
  });

  test("renders users", async () => {
    render(<Users />);
    await screen.findByText("test@test.pl");
  });

  test("matches snapshot", () => {
    const { asFragment } = render(<Users />);
    expect(asFragment()).toMatchSnapshot();
  });
});
