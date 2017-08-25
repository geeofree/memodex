import Service from './base.service'

const { requestAuthToken, validateToken } = (() => {
  const { request } = Service()

  const requestAuthToken = (authPayload) => request.post('/token', authPayload)
  const validateToken = () => request.get('/token/validate')

  return { requestAuthToken, validateToken }
})()


export { requestAuthToken, validateToken }