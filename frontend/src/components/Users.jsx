import React from "react";

export function Users() {
  const [users, setUsers] = React.useState([]);

  React.useEffect(() => {
    const fetchUsers = async () => {
      const response = await fetch("http://localhost:8008/users");
      const data = await response.json();
      if (response.ok) {
        setUsers(data);
      }
    };

    fetchUsers();
  }, []);

  return (
    <div>
      <h1>Users</h1>

      <ul>
        {users.map((user) => (
          <li key={user.id}>{user.email}</li>
        ))}
      </ul>
    </div>
  );
}
