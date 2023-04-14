import { boot } from 'quasar/wrappers'
import axios from 'axios'
import axiosRetry from 'axios-retry'

export default boot(({ app }) => {
  axiosRetry(axios, {
    retries: 5,
    retryDelay: (retryCount) => {
      const delay = retryCount * 1000 + Math.random() * 1000 - 1000
      console.log('Retry number ' + retryCount, ' waiting ', delay, ' milliseconds')
      return delay
    },
    retryCondition: (error) => {
      return error.response.status === 503
    }
  })

  app.config.globalProperties.$axios = axios
})

export { }
