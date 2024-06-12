import axios from "axios";

const HttpClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

export default HttpClient;
