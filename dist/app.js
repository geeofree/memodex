import React from 'react'
import ReactDOM, { render } from 'react-dom'
import './app.style.sass'

const HelloWorld = () => <h1>Hello World!</h1>
const root = document.getElementById('root')

render(<HelloWorld />, root)
