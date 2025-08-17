export const login = async (userData) => {
  const response = await fetch(
    `${import.meta.env.VITE_BACKEND_URL}/api/login`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userData),
    }
  );
  const data = await response.json();
  if (!response.ok) {
    alert(data.msg);
    return;
  }
  localStorage.setItem("token", data.token);
};
