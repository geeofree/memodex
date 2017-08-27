import axios from 'axios'

import { requestAuthToken, validateToken } from '../services/auth.service'

import {
  AUTH_FETCH_USER_VERIFICATION_PENDING,
  AUTH_FETCH_USER_VERIFICATION_FINISHED,
  AUTH_FETCH_USER_VERIFICATION_ERROR,
  AUTH_FETCH_TOKEN_VALIDATION_PENDING,
  AUTH_FETCH_TOKEN_VALIDATION_FINISHED,
  AUTH_FETCH_TOKEN_VALIDATION_ERROR,
} from '../types/auth.types'


const signinPending = () => ({
  type: AUTH_FETCH_USER_VERIFICATION_PENDING
})

const signinFinished = (hasVerifiedAccessToken, fetchResponse) => ({
  type: AUTH_FETCH_USER_VERIFICATION_FINISHED,
  payload: { hasVerifiedAccessToken, fetchResponse }
})

const signinError = (error) => ({
  type: AUTH_FETCH_USER_VERIFICATION_ERROR,
  payload: { error }
})

const validationPending = () => ({
  type: AUTH_FETCH_TOKEN_VALIDATION_PENDING
})

const validationFinished = (hasVerifiedAccessToken, fetchResponse) => ({
  type: AUTH_FETCH_TOKEN_VALIDATION_FINISHED,
  payload: { hasVerifiedAccessToken, fetchResponse }
})

const validationError = (error) => ({
  type: AUTH_FETCH_TOKEN_VALIDATION_ERROR,
  payload: { error }
})

export const userSignin = (authPayload) => (dispatch) => {
  dispatch(signinPending())

  requestAuthToken(authPayload)
    .then(res => {

      const { data } = res
      const { status, status_message } = data

      if(data.status === 200) {
        // Token storing on client storage must be before
        // dispatch so the request headers get updated
        // for the next serviceAction() call
        localStorage.token = data.token
        dispatch(signinFinished(true, { status, status_message }))
      }
      else if(data.status >= 400) {
        dispatch(signinFinished(false, { status, status_message }))
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
