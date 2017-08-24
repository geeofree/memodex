import React from 'react'
import { connect } from 'react-redux'
import AuthPage from './AuthPage'

import { authCheck } from '../../actions/auth.action'

const AuthHOC = (Component) => {

  class Authentication extends React.Component {

    componentWillMount() {
      const { dispatch, isLoggedIn } = this.props
      if(isLoggedIn) dispatch(authCheck())
    }

    render() {
      const { props } = this
      const { isLoggedIn, isFetching } = props

      return (
        isLoggedIn ? !isFetching && <Component {...props} /> : !isFetching && <AuthPage {...props}/>
      )
    }
  }

  const mapStateToProps = (state) => ({
    isLoggedIn: state.auth.authenticated,
    isFetching: state.auth.fetching
  })

  return connect(mapStateToProps)(Authentication)
}

export default AuthHOC
