import axios from "axios";

import { API_REQUEST_TIMEOUT } from "@/constants";

export default axios.create({
  baseURL: process.env.VUE_APP_BACKEND,
  headers: {
    "Content-Type": "application/json; charset=utf-8",
    "X-Requested-With": "XMLHttpRequest",
    "X-CSRF-TOKEN": window.csrfToken
  },
  responseType: "json",
  timeout: API_REQUEST_TIMEOUT
});
