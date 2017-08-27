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
    const { authCheck, location, isLoggedIn } = this.props
    if(!location.state && isLoggedIn) authCheck()
  }

  componentDidMount() {
    const { isValidating } = this.props
    if(!isValidating) this.setState({ processing: false })
  }

  render() {
    const { processing } = this.state
    const { isLoggedIn, isValidating } = this.props
    const { referrer } = this.props.location.state || { referrer: '/dashboard' }

    return processing ? <h1>processing...</h1> : (
      isLoggedIn ? !isValidating && <Redirect to={referrer} /> : !isValidating && <AuthView />
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
