import axios from 'axios'

export default (baseURL='http://localhost:5000/api', withCredentials=true) => {
  
  if(baseURL && typeof baseURL !== "string") {
    throw Error("Invalid baseURL input. Must be of type 'string'")
  }

  const request = axios.create({ baseURL, withCredentials })
  return { request }
}
