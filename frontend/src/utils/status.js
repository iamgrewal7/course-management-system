export const getStatus = async () => {
  const response = await fetch("http://localhost:8000/api/status/", {
    credentials: "include"
  });
  const data = await response.json();
  return data.Result;
};
