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

      const { authCheck, hasVerifiedAccessToken, location } = this.props

      if(location.state) alreadyVerified = location.state.verified

      // Send network request to check if user's token is still valid
      // if user has not already been verified and a user is deemed
      // 'logged in' when they have a token locally stored
      if(!alreadyVerified && hasVerifiedAccessToken) authCheck()
    }

    render() {
      const { props } = this
      const { hasVerifiedAccessToken, isVerifyingToken, location } = props

      return (
        hasVerifiedAccessToken ?
          !isVerifyingToken && <Component {...props} /> :
          !isVerifyingToken && <Redirect to={{ pathname:'/login', state: { referrer: location.pathname } }}/>
      )
    }
  }

  const mapStateToProps = ({ auth }) => ({
    hasVerifiedAccessToken: auth.hasVerifiedAccessToken,
    isVerifyingToken: auth.verifyingToken
  })

  const mapDispatchToProps = (dispatch) => ({
    authCheck: () => dispatch(authCheck())
  })

  return connect(mapStateToProps, mapDispatchToProps)(Authentication)
}

export default AuthHOC
