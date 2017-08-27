import React from 'react'
import { connect } from 'react-redux'
import { Redirect } from 'react-router-dom'

import { authCheck } from '../../actions/auth.action'

import AuthView from '../auth/auth.view'
import ViewHOC from '../../HOC/view.hoc'


class LoginView extends React.Component {

  componentDidMount() {
    const { isValidating } = this.props
    if(!isValidating) this.setState({ processing: false })
  }

  render() {
    const { isLoggedIn, isValidating } = this.props
    const { referrer } = this.props.location.state || { referrer: '/' }

    console.log(isValidating, isLoggedIn)

    return isValidating ? <h1>Processing..</h1> : (
      isLoggedIn ? <Redirect to={referrer} /> : <AuthView />
    )
  }
}

const mapStateToProps = ({ auth }) => ({
  isLoggedIn: auth.authenticated,
  isValidating: auth.validating
})

const mapDispatchToProps = (dispatch) => ({
  authCheck: () => dispatch(authCheck())
})

export default ViewHOC(connect(mapStateToProps, mapDispatchToProps)(LoginView))
