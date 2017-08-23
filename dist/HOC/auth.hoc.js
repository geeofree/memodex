import React from 'react'
import { connect } from 'react-redux'
import AuthPage from '../views/auth.view'

const AuthHOC = (Component) => {
  const Login = (props) => (
    props.isLoggedIn ? <Component {...props} /> : <AuthPage {...props}/>
  )

  const mapStateToProps = (state) => ({
    isLoggedIn: state.auth.authenticated
  })

  return connect(mapStateToProps)(Login)
}

export default AuthHOC
