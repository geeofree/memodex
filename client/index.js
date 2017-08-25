import React from 'react'
import ReactDOM, { render } from 'react-dom'

import { Provider } from 'react-redux'
import appState     from './app.state'
import Application  from './app.main'

const Memodex = () => (
  <Provider store={appState}>
    <Application />
  </Provider>
)

const root = document.getElementById('root')
render(<Memodex />, root)
