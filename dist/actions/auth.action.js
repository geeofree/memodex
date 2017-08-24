import axios from 'axios'

import { requestAuthToken, validateToken } from '../services/auth.service'

import {
  AUTH_FETCH_PENDING,
  AUTH_FETCH_SUCCESS,
  AUTH_FETCH_ERROR,
  AUTH_TOKEN_VALIDATION_PENDING,
  AUTH_TOKEN_VALIDATION_FINISHED,
  AUTH_TOKEN_VALIDATION_ERROR,
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

const validationPending = () => ({
  type: AUTH_TOKEN_VALIDATION_PENDING
})

const validationFinished = (authenticated) => ({
  type: AUTH_TOKEN_VALIDATION_FINISHED,
  payload: { authenticated }
})

const validationError = (error) => ({
  type: AUTH_TOKEN_VALIDATION_ERROR,
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
      dispatch(signinError('Something went wrong while signing in'))
    })
}

export const authCheck = () => (dispatch) => {
  dispatch(validationPending())

  validateToken()
    .then(res => {
      const { data } = res

      if(data.status === 409) {
        dispatch(validationFinished(true))
      }
      else if(data.status >= 400) {
        dispatch(validationFinished(false))
      }
      
    })
    .catch(err => {
      console.log(err)
      dispatch(validationError('Somethin went wrong while validating authentication'))
    })
}
