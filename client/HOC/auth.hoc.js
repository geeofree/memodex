import React       from 'react'
import { connect } from 'react-redux'

import AuthView      from '../views/auth/auth.view'
import { authCheck } from '../actions/auth.action'


const AuthHOC = (Component) => {

  class Authentication extends React.Component {
    componentWillMount() {
      const { dispatch, isLoggedIn } = this.props
      if(isLoggedIn) dispatch(authCheck())
    }

    render() {
      const { props } = this
      const { isLoggedIn, isValidating } = props

      return (
        isLoggedIn ? !isValidating && <Component {...props} /> : !isValidating && <AuthView {...props}/>
      )
    }
  }

  const mapStateToProps = (state) => ({
    isLoggedIn: state.auth.authenticated,
    isValidating: state.auth.validating
  })

  return connect(mapStateToProps)(Authentication)
}

export default AuthHOC
