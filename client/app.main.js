import React from 'react'
import './app.style.sass'

import AuthHOC from './HOC/auth.hoc'

const Application = () => <h1>Hello World!</h1>

export default AuthHOC(Application)
