import React from 'react'
import './FormSubmit.style.sass'

export default ({ text }) => (
  <button
    className="form-submit-btn"
    type="submit">
      {text || "Submit"}
  </button>
)
