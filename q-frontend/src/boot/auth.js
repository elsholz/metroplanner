import { boot } from 'quasar/wrappers'
import { createAuth0 } from '@auth0/auth0-vue'

// "async" is optional;
// more info on params: https://v2.quasar.dev/quasar-cli/boot-files
export default boot(async ({ app, router, store, Vue }) => {
  // const app = createApp(App);

  app.use(
    createAuth0({
      domain: 'dev-twa5tnu1.eu.auth0.com',
      clientId: '8mxekg7iDQSgxabarihl5KfynOjirudy',
      authorizationParams: {
        redirect_uri: window.location.origin
      }
    })
  )

// app.mount('#app');
})
