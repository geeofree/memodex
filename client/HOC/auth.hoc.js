import React       from 'react'
import { connect } from 'react-redux'

import { Redirect }  from 'react-router-dom'
import { authCheck } from '../actions/auth.action'


const AuthHOC = (Component) => {

  class Authentication extends React.Component {
    componentWillMount() {
      // Variable for checking during redirects from /login route so
      // we don't do another network request even after successfully
      // getting a verified authentication
      let alreadyVerified = false

      const { authCheck, isLoggedIn, location } = this.props
      
      if(location.state) alreadyVerified = location.state.verified

      // Send network request to check if user's token is still valid
      // if user has not already been verified and a user is deemed
      // 'logged in' when they have a token locally stored
      if(!alreadyVerified && isLoggedIn) authCheck()
    }

    render() {
      const { props } = this
      const { isLoggedIn, isValidating, location } = props

      return (
        isLoggedIn ?
          !isValidating && <Component {...props} /> :
          !isValidating && <Redirect to={{ pathname:'/login', state: { referrer: location.pathname } }}/>
      )
    }
  }

  const mapStateToProps = (state) => ({
    isLoggedIn: state.auth.authenticated,
    isValidating: state.auth.validating
  })

  const mapDispatchToProps = (dispatch) => ({
    authCheck: () => dispatch(authCheck())
  })

  return connect(mapStateToProps, mapDispatchToProps)(Authentication)
}

export default AuthHOC
