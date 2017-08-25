import assign from '../helpers/assign'

import {
  AUTH_SIGNIN_PENDING,
  AUTH_SIGNIN_FINISHED,
  AUTH_SIGNIN_ERROR,
  AUTH_TOKEN_VALIDATION_PENDING,
  AUTH_TOKEN_VALIDATION_FINISHED,
  AUTH_TOKEN_VALIDATION_ERROR
} from '../types/auth.types'


const token    = localStorage.getItem('token')
const hasToken = Boolean(token)

const initialState = {
  fetching: false,
  validating: false,
  authenticated: hasToken,
  error: null,
  fetchResponse: { status: null, status_message: null }
}

export default (state=initialState, action) => {
  switch(action.type) {

    case AUTH_TOKEN_VALIDATION_PENDING:
      return assign(state, {
        validating: true,
        fetchResponse: assign(state.fetchResponse, {
          status: null,
          status_message: null
        })
      })

    case AUTH_TOKEN_VALIDATION_FINISHED:
      return assign(state, {
        error: null,
        validating: false,
        authenticated: action.payload.authenticated,
        fetchResponse: assign(state.fetchResponse, {
          status: action.payload.fetchResponse.status,
          status_message: action.payload.fetchResponse.status_message
        })
      })

    case AUTH_TOKEN_VALIDATION_ERROR:
      return assign(state, {
        validating: false,
        error: action.payload.error
      })

    case AUTH_SIGNIN_PENDING:
      return assign(state, {
        fetching: true,
        fetchResponse: assign(state.fetchResponse, {
          status: null,
          status_message: null
        })
      })

    case AUTH_SIGNIN_FINISHED:
      return assign(state, {
        fetching: false,
        authenticated: action.payload.authenticated,
        error: null,
        fetchResponse: assign(state.fetchResponse, {
          status: action.payload.fetchResponse.status,
          status_message: action.payload.fetchResponse.status_message
        })
      })

    case AUTH_SIGNIN_ERROR:
      return assign(state, {
        fetching: false,
        error: action.payload.error
      })

    default:
      return state
  }
}
