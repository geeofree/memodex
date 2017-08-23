import axios from 'axios'

import {
  AUTH_FETCH_PENDING,
  AUTH_FETCH_SUCCESS,
  AUTH_FETCH_ERROR
} from '../types/auth.types'


const signinPending = () => ({
  type: AUTH_FETCH_PENDING
})

const signinSuccess = (authenticated, token) => ({
  type: AUTH_FETCH_SUCCESS,
  payload: { authenticated, token }
})

const signinError = (error) => ({
  type: AUTH_FETCH_ERROR,
  payload: { error }
})


export const signin = (authPayload) => (dispatch) => {

  dispatch(signinPending())

  const request = axios.create({
    baseURL: 'http://localhost:5000/api',
    withCredentials: true
  })

  request.post('/token', authPayload)
    .then(res => {
      const { data } = res

      if(data.status === 200) {
        dispatch(signinSuccess(true, data.token))
        localStorage.token = data.token
      }
      else if(data.status >= 400 && data.status !== 409) {
        dispatch(signinSuccess(false, null))
      }
    })
    .catch(err => {
      console.log(err)
      dispatch(signinError('Something went wrong'))
    })
}
