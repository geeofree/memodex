import React from 'react'
import { connect } from 'react-redux'
import { Redirect } from 'react-router-dom'

import { authCheck } from '../../actions/auth.action'

import AuthView from '../auth/auth.view'
import ViewHOC from '../../HOC/view.hoc'


class LoginView extends React.Component {

  constructor(props) {
    super(props)
    this.state = { processing: true }
  }

  componentWillMount() {
    const { authCheck, location, hasVerifiedAccessToken } = this.props
    if(!location.state && hasVerifiedAccessToken) authCheck()
  }

  componentDidMount() {
    const { isVerifyingToken } = this.props
    if(!isVerifyingToken) this.setState({ processing: false })
  }

  render() {
    const { processing } = this.state
    const { hasVerifiedAccessToken, isVerifyingToken } = this.props
    const { referrer } = this.props.location.state || { referrer: '/dashboard' }

    return processing ? <h1>processing...</h1> : (
      hasVerifiedAccessToken ?
        // Redirect from referrer route or /dashboard if verified
        !isVerifyingToken && <Redirect to={{ pathname: referrer, state: { verified: true } }} /> :
        // Show Sign in form if not
        !isVerifyingToken && <AuthView />
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

export default ViewHOC(connect(mapStateToProps, mapDispatchToProps)(LoginView))
