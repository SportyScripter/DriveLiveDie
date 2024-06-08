// login.spec.js

import { user } from "../fixtures/user";

describe("Logowanie użytkownika", () => {
  beforeEach(() => {
    cy.visit("http://127.0.0.1:5173/login");
  });

  it("Logowanie z poprawnymi danymi", () => {
    cy.get('input[name="email"]').type(user.email);
    cy.get('input[name="password"]').type(user.password);
    cy.get("form").submit();
    cy.url().should("include", "/dashboard"); // Przekierowanie po pomyślnym logowaniu
  });

  it("Logowanie z niepoprawnymi danymi", () => {
    cy.get('input[name="email"]').type(user.email);
    cy.get('input[name="password"]').type("wrongPassword");
    cy.get("form").submit();
    cy.get(".error").should(
      "contain",
      "Nieprawidłowa nazwa użytkownika lub hasło."
    );
  });

  it("Przycisk logowania jest nieklikalny gdy formularz jest pusty", () => {
    cy.get('button[type="submit"]').should("be.disabled");
  });
});
