import { useEffect, useState } from "react";
import { Navigate, Outlet, useLocation } from "react-router-dom";

export default function Root() {
  const [isLogged, setIsLogged] = useState(false);
  let location = useLocation();

  const token = localStorage.getItem("access_token");

  const logout = () => {
    localStorage.removeItem("access_token");
    setIsLogged(false);
  };

  useEffect(() => {
    if (token && !isLogged) {
      setIsLogged(true);
    }
  }, [token]);

  if (
    !token &&
    !isLogged &&
    location.pathname !== "/login" &&
    location.pathname !== "/register"
  ) {
    return <Navigate to="login" />;
  }

  return (
    <>
      <div id="sidebar">
        <nav>
          <ul>{isLogged && <li onClick={logout}>Wyloguj</li>}</ul>
        </nav>

        {/* other elements */}
      </div>
      {/* all the other elements */}
      <div id="detail">
        <Outlet />
      </div>
    </>
  );
}
