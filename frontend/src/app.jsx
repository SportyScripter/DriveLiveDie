import React from "react";
import { Login } from "./components/Login";
import { Register } from "./components/Register";
import { Vehicles } from "./components/Vehicles";
import { Users } from "./components/Users";

export function App() {
  const [isLogged, setIsLogged] = React.useState(false);
  const [selectedTab, setSelectedTab] = React.useState("vehicles");

  const token = localStorage.getItem("access_token");

  const logout = () => {
    localStorage.removeItem("access_token");
    setIsLogged(false);
  };

  React.useEffect(() => {
    if (token && !isLogged) {
      setIsLogged(true);
    }
  }, [token]);

  if (!isLogged) {
    return (
      <section>
        Nie jesteś zalogowany
        <Login />
      </section>
    );
  }

  return (
    <div>
      <section>
        <button onClick={() => setSelectedTab("vehicles")}>Pojazdy</button>
        <button onClick={() => setSelectedTab("users")}>Uzytkownicy</button>
        <button onClick={logout}>Wyloguj</button>
      </section>

      {selectedTab === "vehicles" && <Vehicles />}
      {selectedTab === "users" && <Users />}
    </div>
  );
}
