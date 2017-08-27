import assign from '../helpers/assign'

import {
  AUTH_FETCH_USER_VERIFICATION_PENDING,
  AUTH_FETCH_USER_VERIFICATION_FINISHED,
  AUTH_FETCH_USER_VERIFICATION_ERROR,
  AUTH_FETCH_TOKEN_VALIDATION_PENDING,
  AUTH_FETCH_TOKEN_VALIDATION_FINISHED,
  AUTH_FETCH_TOKEN_VALIDATION_ERROR
} from '../types/auth.types'


const accesstoken = localStorage.getItem('token')
const hasToken    = Boolean(accesstoken)

const initialState = {
  verifyingUser: false,
  verifyingToken: false,
  hasVerifiedAccessToken: hasToken,
  token: accesstoken || null,
  error: null,
  fetchResponse: { status: null, status_message: null }
}

export default (state=initialState, action) => {
  switch(action.type) {

    case AUTH_FETCH_TOKEN_VALIDATION_PENDING:
      return assign(state, {
        verifyingToken: true,
        fetchResponse: assign(state.fetchResponse, {
          status: null,
          status_message: null
        })
      })

    case AUTH_FETCH_TOKEN_VALIDATION_FINISHED:
      return assign(state, {
        error: null,
        verifyingToken: false,
        hasVerifiedAccessToken: action.payload.hasVerifiedAccessToken,
        fetchResponse: assign(state.fetchResponse, {
          status: action.payload.fetchResponse.status,
          status_message: action.payload.fetchResponse.status_message
        })
      })

    case AUTH_FETCH_TOKEN_VALIDATION_ERROR:
      return assign(state, {
        verifyingToken: false,
        error: action.payload.error
      })

    case AUTH_FETCH_USER_VERIFICATION_PENDING:
      return assign(state, {
        verifyingUser: true,
        fetchResponse: assign(state.fetchResponse, {
          status: null,
          status_message: null
        })
      })

    case AUTH_FETCH_USER_VERIFICATION_FINISHED:
      return assign(state, {
        verifyingUser: false,
        hasVerifiedAccessToken: action.payload.hasVerifiedAccessToken,
        error: null,
        fetchResponse: assign(state.fetchResponse, {
          status: action.payload.fetchResponse.status,
          status_message: action.payload.fetchResponse.status_message
        })
      })

    case AUTH_FETCH_USER_VERIFICATION_ERROR:
      return assign(state, {
        verifyingUser: false,
        error: action.payload.error
      })

    default:
      return state
  }
}
