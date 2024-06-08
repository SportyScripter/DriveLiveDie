import { useForm } from "react-hook-form";

export function Register() {
  const { register, handleSubmit } = useForm();

  const onSubmit = (data) => {
    console.log(data);

    fetch("http://localhost:8008/auth/create-user", {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
      },
    });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <label>
        Name
        <input {...register("name")} />
      </label>
      <label>
        last name
        <input {...register("last_name")} />
      </label>
      <label>
        username
        <input {...register("username")} />
      </label>
      <label>
        Email
        <input {...register("email")} />
      </label>
      <label>
        Password
        <input {...register("password")} />
      </label>
      <button type="submit">Register</button>
    </form>
  );
}
