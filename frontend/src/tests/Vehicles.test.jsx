import { render, screen } from "@testing-library/react";
import { Vehicles } from "../components/Vehicles";
import React from "react";

import { server } from "./mocks";

describe("Vehicles", () => {
  beforeAll(() => {
    server.listen();
  });
  afterAll(() => server.close());

  test("Renders the view correctly", async () => {
    render(<Vehicles />);
    screen.findByText("Vehicles");
  });

  test("renders vehicles", async () => {
    render(<Vehicles />);
    await screen.findByText("Car");
    await screen.findByText("Bike");
  });

  test("matches snapshot", () => {
    const { asFragment } = render(<Vehicles />);
    expect(asFragment()).toMatchSnapshot();
  });
});
