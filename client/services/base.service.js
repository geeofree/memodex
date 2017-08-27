import axios from 'axios'

export default (baseURL='http://localhost:5000/api', withCredentials=false) => {

  if(baseURL && typeof baseURL !== "string") {
    throw Error("Invalid baseURL input. Must be of type 'string'")
  }

  const request = axios.create({ baseURL, withCredentials })

  const serviceAction = (callback) => (...args) => {
      const token = localStorage.getItem('token')
      request.defaults.headers.common['x-access-token'] = token
      return callback(request)(...args)
  }

  return { serviceAction }
}
