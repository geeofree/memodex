import assign from '../helpers/assign'

import {
  AUTH_FETCH_PENDING,
  AUTH_FETCH_SUCCESS,
  AUTH_FETCH_ERROR
} from '../types/auth.types'


const token    = localStorage.getItem('token')
const hasToken = Boolean(token)

const initialState = {
  fetching: false,
  authenticated: hasToken,
  error: null,
  token
}

export default (state=initialState, action) => {
  switch(action.type) {

    case AUTH_FETCH_PENDING:
      return assign(state, { fetching: true })

    case AUTH_FETCH_SUCCESS:
      return assign(state, {
        fetching: false,
        authenticated: action.payload.authenticated,
        token: action.payload.token,
        error: null
      })

    case AUTH_FETCH_ERROR:
      return assign(state, {
        fetching: false,
        error: action.payload.error
      })

    default:
      return state
  }
}
