import React       from 'react'
import { connect } from 'react-redux'

import { signin }  from '../../actions/auth.action'

import FormInput     from '../../commons/FormInput'
import FormSubmitBtn from '../../commons/FormSubmit'


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
        <FormInput title="Username" name="username" type="text" onChange={changeHandler}/>
        <FormInput title="Password" name="password" type="password" onChange={changeHandler}/>
        <FormSubmitBtn text="Sign in"/>
      </form>
    )
  }
}

const mapStateToProps = (state) => ({
  isFetching: state.auth.fetching
})

export default connect(mapStateToProps)(AuthView)
