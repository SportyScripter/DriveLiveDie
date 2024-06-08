import { Vehicles } from "../components/Vehicles";
import { Users } from "../components/Users";
import { useState } from "react";

export default function DashboardPage() {
  const [selectedTab, setSelectedTab] = useState("vehicles");

  return (
    <div>
      <div>
        <section>
          <button onClick={() => setSelectedTab("vehicles")}>Pojazdy</button>
          <button onClick={() => setSelectedTab("users")}>Uzytkownicy</button>
        </section>

        {selectedTab === "vehicles" && <Vehicles />}
        {selectedTab === "users" && <Users />}
      </div>
    </div>
  );
}
