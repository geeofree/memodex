import axios from 'axios'

import { requestAuthToken, validateToken } from '../services/auth.service'

import {
  AUTH_FETCH_PENDING,
  AUTH_FETCH_SUCCESS,
  AUTH_FETCH_ERROR,
  AUTH_SET_TOKEN
} from '../types/auth.types'


const signinPending = () => ({
  type: AUTH_FETCH_PENDING
})

const signinSuccess = (authenticated) => ({
  type: AUTH_FETCH_SUCCESS,
  payload: { authenticated }
})

const signinError = (error) => ({
  type: AUTH_FETCH_ERROR,
  payload: { error }
})


export const signin = (authPayload) => (dispatch) => {

  dispatch(signinPending())

  requestAuthToken(authPayload)
    .then(res => {
      const { data } = res

      if(data.status === 200) {
        dispatch(signinSuccess(true))
        localStorage.token = data.token
      }
      else if(data.status >= 400) {
        dispatch(signinSuccess(false))
      }
    })
    .catch(err => {
      console.log(err)
      dispatch(signinError('Something went wrong'))
    })
}

export const authCheck = () => (dispatch) => {
  dispatch(signinPending())

  validateToken()
    .then(res => {
      const { data } = res

      if(data.status === 409) {
        dispatch(signinSuccess(true))
      }
      else if(data.status >= 400) {
        dispatch(signinSuccess(false))
      }

    })
    .catch(err => {
      console.log(err)
      dispatch(signinError('Somethin went wrong'))
    })
}
