import React       from 'react'
import { connect } from 'react-redux'

import { Redirect }  from 'react-router-dom'
import { authCheck } from '../actions/auth.action'


const AuthHOC = (Component) => {

  class Authentication extends React.Component {
    componentWillMount() {
      const { dispatch, isLoggedIn } = this.props
      if(isLoggedIn) dispatch(authCheck())
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

  return connect(mapStateToProps)(Authentication)
}

export default AuthHOC
