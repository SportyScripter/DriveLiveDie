import { setupServer } from "msw/node";
import { http, HttpResponse } from "msw";

const handlers = [
  http.post("http://localhost:8008/auth/login", () => {
    return HttpResponse.json({ greeting: "hello there" });
  }),
  http.post("http://localhost:8008/auth/create-user", () => {
    return HttpResponse.json({ greeting: "hello there" });
  }),
  http.get("http://localhost:8008/vehicles", () => {
    return HttpResponse.json([
      { id: 1, name: "Car" },
      { id: 2, name: "Bike" },
    ]);
  }),
  http.get("http://localhost:8008/users", () => {
    return HttpResponse.json([{ id: 1, email: "test@test.pl" }]);
  }),
];

export const server = setupServer(...handlers);
