import axios from 'axios'

import { requestAuthToken, validateToken } from '../services/auth.service'

import {
  AUTH_SIGNIN_PENDING,
  AUTH_SIGNIN_FINISHED,
  AUTH_SIGNIN_ERROR,
  AUTH_TOKEN_VALIDATION_PENDING,
  AUTH_TOKEN_VALIDATION_FINISHED,
  AUTH_TOKEN_VALIDATION_ERROR,
} from '../types/auth.types'


const signinPending = () => ({
  type: AUTH_SIGNIN_PENDING
})

const signinSuccess = (authenticated, fetchResponse) => ({
  type: AUTH_SIGNIN_FINISHED,
  payload: { authenticated, fetchResponse }
})

const signinError = (error) => ({
  type: AUTH_SIGNIN_ERROR,
  payload: { error }
})

const validationPending = () => ({
  type: AUTH_TOKEN_VALIDATION_PENDING
})

const validationFinished = (authenticated, fetchResponse) => ({
  type: AUTH_TOKEN_VALIDATION_FINISHED,
  payload: { authenticated, fetchResponse }
})

const validationError = (error) => ({
  type: AUTH_TOKEN_VALIDATION_ERROR,
  payload: { error }
})

export const userSignin = (authPayload) => (dispatch) => {
  dispatch(signinPending())

  requestAuthToken(authPayload)
    .then(res => {

      const { data } = res
      const { status, status_message } = data

      if(data.status === 200) {
        dispatch(signinSuccess(true, { status, status_message }))
        localStorage.token = data.token
      }
      else if(data.status >= 400) {
        dispatch(signinSuccess(false, { status, status_message }))
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
      const { status, status_message } = data

      if(data.status === 409) {
        dispatch(validationFinished(true, { status, status_message }))
      }
      else if(data.status >= 400) {
        dispatch(validationFinished(false, { status, status_message }))
      }

    })
    .catch(err => {
      console.log(err)
      dispatch(validationError('Somethin went wrong while validating authentication'))
    })
}
