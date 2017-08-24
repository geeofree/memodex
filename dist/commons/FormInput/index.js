import React from 'react'
import './FormInput.style.sass'

export default (props) => (
  <div className="form-input-container">
    {props.title && <span className="form-input-title">{props.title}</span>}
    <input className="form-input" {...props} />
  </div>
)
