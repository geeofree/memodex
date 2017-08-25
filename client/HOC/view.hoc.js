import React     from 'react'
import { Route } from 'react-router-dom'
import AuthHOC   from './auth.hoc'

export default (Component) => (props) => (
  <Route {...props} component={props.protected ? AuthHOC(Component) : Component} />
)
