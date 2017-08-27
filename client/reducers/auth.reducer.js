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
  fetching: false,
  validating: false,
  authenticated: hasToken,
  token: accesstoken || null,
  error: null,
  fetchResponse: { status: null, status_message: null }
}

export default (state=initialState, action) => {
  switch(action.type) {

    case AUTH_FETCH_TOKEN_VALIDATION_PENDING:
      return assign(state, {
        validating: true,
        fetchResponse: assign(state.fetchResponse, {
          status: null,
          status_message: null
        })
      })

    case AUTH_FETCH_TOKEN_VALIDATION_FINISHED:
      return assign(state, {
        error: null,
        validating: false,
        authenticated: action.payload.authenticated,
        fetchResponse: assign(state.fetchResponse, {
          status: action.payload.fetchResponse.status,
          status_message: action.payload.fetchResponse.status_message
        })
      })

    case AUTH_FETCH_TOKEN_VALIDATION_ERROR:
      return assign(state, {
        validating: false,
        error: action.payload.error
      })

    case AUTH_FETCH_USER_VERIFICATION_PENDING:
      return assign(state, {
        fetching: true,
        fetchResponse: assign(state.fetchResponse, {
          status: null,
          status_message: null
        })
      })

    case AUTH_FETCH_USER_VERIFICATION_FINISHED:
      return assign(state, {
        fetching: false,
        authenticated: action.payload.authenticated,
        error: null,
        fetchResponse: assign(state.fetchResponse, {
          status: action.payload.fetchResponse.status,
          status_message: action.payload.fetchResponse.status_message
        })
      })

    case AUTH_FETCH_USER_VERIFICATION_ERROR:
      return assign(state, {
        fetching: false,
        error: action.payload.error
      })

    default:
      return state
  }
}
