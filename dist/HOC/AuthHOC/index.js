import React from 'react'
import { connect } from 'react-redux'
import AuthPage from './AuthPage'

// import { validateToken } from '../../actions/auth.action'

const AuthHOC = (Component) => {

  class Authentication extends React.Component {
    componentWillMount() {
      const { dispatch } = this.props

      // dispatch(validateToken())
    }

    render() {

      const { props } = this
      const { isLoggedIn } = props

      return (
        isLoggedIn ? <Component {...props} /> : <AuthPage {...props}/>
      )
    }
  }

  const mapStateToProps = (state) => ({
    isLoggedIn: state.auth.authenticated
  })

  return connect(mapStateToProps)(Authentication)
}

export default AuthHOC
