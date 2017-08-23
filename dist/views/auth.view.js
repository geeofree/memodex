import React from 'react'
import { connect } from 'react-redux'
import { signin } from '../actions/auth.action'

class AuthView extends React.Component {
  constructor(props) {
    super(props)

    this.submitHandler = this.submitHandler.bind(this)
    this.changeHandler = this.changeHandler.bind(this)

    this.state = {
      username: '',
      password: ''
    }
  }

  changeHandler(e) {
    const { target } = e

    this.setState({
      [target.name]: target.value
    })
  }

  submitHandler(e) {
    e.preventDefault()
    const { username, password } = this.state
    const { dispatch } = this.props

    dispatch(signin({ username, password }))
  }

  render() {
    const { submitHandler, changeHandler } = this

    return (
      <form onSubmit={submitHandler}>
        <input name="username" type="text" onChange={changeHandler}/>
        <input name="password" type="password" onChange={changeHandler}/>
        <button>Submit</button>
      </form>
    )
  }
}

const mapStateToProps = (state) => ({
  isFetching: state.auth.fetching
})

export default connect(mapStateToProps)(AuthView)
