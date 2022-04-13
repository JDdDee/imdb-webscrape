import axios from "axios";

export const API = axios.create({
  baseURL: "http://localhost:5000/api",
});

export async function executeQuery(sql, params) {
  return API.post("/execute", { sql, params })
    .then(({ data }) => data)
    .catch(({ response }) => response);
}
