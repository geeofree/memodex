import React from 'react'
import { connect } from 'react-redux'
import { signin } from '../actions/auth.action'
import AuthHOC from '../HOC/AuthHOC'

const Application = () => <h1>Hello World!</h1>

const mapStateToProps = (state) => ({
  isFetching: state.auth.fetching
})

export default connect(mapStateToProps)(AuthHOC(Application))
