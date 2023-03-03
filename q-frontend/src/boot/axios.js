import { boot } from 'quasar/wrappers'
import axios from 'axios'
import axiosRetry from 'axios-retry'

export default boot(({ app }) => {
  axiosRetry(axios, {
    retries: 5,
    retryDelay: (retryCount) => {
      console.log('Retry number ' + retryCount)
      return retryCount * 1000
    },
    retryCondition: (error) => {
      return error.response.status === 503
    }
  })

  app.config.globalProperties.$axios = axios
})

export { }
