import Service from './base.service'

export const { requestAuthToken, validateToken } = (() => {
  const { serviceAction } = Service()

  const requestAuthToken = serviceAction(request => authPayload =>  request.post('/token', authPayload))
  const validateToken = serviceAction(request => () => request.post('/token/validate'))

  return { requestAuthToken, validateToken }
})()
