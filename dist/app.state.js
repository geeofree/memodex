import { createStore, applyMiddleware } from 'redux'

import reducers from './reducers'
import thunk from 'redux-thunk'
// For development only
import logger from 'redux-logger'

const middleware = applyMiddleware(thunk, logger)

export default createStore(reducers, middleware)
