import React, { StrictMode } from "react";
import ReactDOM from "react-dom/client";

import { App } from "./app";

import "./index.css";
// Render the app
const rootElement = document.getElementById("root");

if (!rootElement.innerHTML) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    <StrictMode>
      <App />
    </StrictMode>
  );
}
