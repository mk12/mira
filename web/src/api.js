import axios from "axios";

import { API_REQUEST_TIMEOUT } from "@/constants";
import { isDevelopment } from "@/util";

export default axios.create({
  baseURL: process.env.VUE_APP_BACKEND,
  withCredentials: isDevelopment(),
  headers: {
    "Content-Type": "application/json; charset=utf-8",
    "X-Requested-With": "XMLHttpRequest",
    "X-CSRFToken": window.csrfToken
  },
  responseType: "json",
  timeout: API_REQUEST_TIMEOUT
});
