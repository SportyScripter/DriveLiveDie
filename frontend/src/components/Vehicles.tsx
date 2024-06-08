import React from "react";

interface Vehicle {
  id: number;
  name: string;
}

export function Vehicles() {
  const [vehicles, setVehicles] = React.useState<Vehicle[]>([]);

  React.useEffect(() => {
    const fetchVehicles = async () => {
      const response = await fetch("http://localhost:8008/vehicles");
      const data = await response.json();
      if (response.ok) {
        setVehicles(data);
      }
    };

    fetchVehicles();
  }, []);

  return (
    <div>
      <h1>Vehicles</h1>

      <ul>
        {vehicles.map((vehicle) => (
          <li key={vehicle.id}>{vehicle.name}</li>
        ))}
      </ul>
    </div>
  );
}
