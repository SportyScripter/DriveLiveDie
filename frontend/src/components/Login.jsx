import { useForm } from "react-hook-form";

export function Login() {
  const { register, handleSubmit } = useForm();

  const onSubmit = (data) => {
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
          window.location.reload();
        });
      }
    });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <label>
        Email
        <input {...register("email")} />
      </label>
      <label>
        Password
        <input {...register("password")} />
      </label>
      <button type="submit">Login</button>
    </form>
  );
}
