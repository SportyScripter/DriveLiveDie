// register.spec.js

import { user } from "../fixtures/user";

describe("Rejestracja użytkownika", () => {
  beforeEach(() => {
    cy.visit("http://127.0.0.1:5173/register");
  });

  it("Pomyślna rejestracja", () => {
    cy.get('input[name="username"]').type(user.username);
    cy.get('input[name="first_name"]').type(user.first_name);
    cy.get('input[name="last_name"]').type(user.last_name);
    cy.get('input[name="email"]').type(user.email);
    cy.get('input[name="password"]').type(user.password);
    cy.get("form").submit();
    cy.url().should("include", "/dashboard"); // Przekierowanie po pomyślnej rejestracji
  });

  it("Rejestracja z istniejącym adresem e-mail", () => {
    cy.get('input[name="username"]').type(user.username);
    cy.get('input[name="first_name"]').type(user.first_name);
    cy.get('input[name="last_name"]').type(user.last_name);
    cy.get('input[name="email"]').type(user.email);
    cy.get('input[name="password"]').type(user.password);
    cy.get("form").submit();
    cy.get(".error").should("contain", "Błędne dane.");
  });

  it("Przycisk rejestracji jest nieklikalny gdy formularz jest pusty", () => {
    cy.get('button[type="submit"]').should("be.disabled");
  });
});
