import React       from 'react'
import { connect } from 'react-redux'

import FormInput     from '../../components/FormInput'
import FormSubmitBtn from '../../components/FormSubmit'

import { userSignin } from '../../actions/auth.action'


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
    this.setState({ [target.name]: target.value })
  }

  submitHandler(e) {
    e.preventDefault()

    const { username, password } = this.state
    const { userSignin } = this.props

    userSignin({ username, password })
  }

  render() {
    const { submitHandler, changeHandler } = this
    const { isFetching } = this.props

    return (
      <form onSubmit={submitHandler}>
        <FormInput title="Username" name="username" type="text" onChange={changeHandler}/>
        <FormInput title="Password" name="password" type="password" onChange={changeHandler}/>
        <FormSubmitBtn text="Sign in"/>
        { isFetching && <p>Loading...</p> }
      </form>
    )
  }
}

const mapStateToProps = (state) => ({
  isFetching: state.auth.fetching
})

const mapDispatchToProps = (dispatch) => ({
  userSignin: (userCredentials) => dispatch(userSignin(userCredentials))
})

export default connect(mapStateToProps, mapDispatchToProps)(AuthView)
