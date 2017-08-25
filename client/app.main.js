import React from 'react'
import './app.style.sass'

import { Switch } from 'react-router-dom'
import Router from './components/Router/app.router'

import Home from './views/home/home.view'
import Dashboard from './views/dashboard/dashboard.view'

export default () => (
  <Router>
    <Switch>
      <Home path="/" exact={true} />
      <Dashboard path="/dashboard" protected />
    </Switch>
  </Router>
)
