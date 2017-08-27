import { createStore, applyMiddleware } from 'redux'

import rootReducer from './reducers/root.reducer'
import thunk from 'redux-thunk'
// For development only
import logger from 'redux-logger'

const middleware = applyMiddleware(thunk, logger)

export default createStore(rootReducer, middleware)
