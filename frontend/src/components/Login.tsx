import { useState } from "react";
import { useForm } from "react-hook-form";

export function Login() {
  const [error, setError] = useState("");
  const { formState, register, handleSubmit } = useForm();

  const touched = Object.keys(formState.touchedFields).length === 2;

  const onSubmit = (data: any) => {
    fetch("http://localhost:8008/auth/login", {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
      },
    }).then((response) => {
      if (response.ok) {
        response.json().then((data) => {
          localStorage.setItem("access_token", data.token);
          window.location.href = "/dashboard";
        });
      } else {
        console.log(response);
        setError("Nieprawidłowa nazwa użytkownika lub hasło.");
      }
    });
  };

  return (
    <form
      className="bg-white px-8 pt-6 pb-8 mb-4"
      onSubmit={handleSubmit(onSubmit)}
    >
      {error && (
        <div className="error mt-3 mb-3 bg-red-100 border-red-300 p-2">
          {error}
        </div>
      )}
      <div className="mb-4">
        <label
          className="block text-gray-700 text-sm font-bold mb-2"
          htmlFor="email"
        >
          Adres e-mail
        </label>
        <input
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="email"
          type="text"
          placeholder="email"
          {...register("email")}
        />
      </div>
      <div className="mb-6">
        <label
          className="block text-gray-700 text-sm font-bold mb-2"
          htmlFor="password"
        >
          Hasło
        </label>
        <input
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
          id="password"
          type="password"
          placeholder="******************"
          {...register("password")}
        />
      </div>
      <div className="flex items-center justify-between">
        <button
          disabled={!touched}
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          type="submit"
        >
          Zaloguj
        </button>
      </div>
    </form>
  );
}
