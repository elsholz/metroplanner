<template>
  <q-btn v-if="loggedIn" :label="user.displayName" color="green-5" outline class="q-pa-sm q-px-md text-body1" icon="person" />
  <q-btn v-else @click="login" v-label="Login" color="green-6" class="q-pa-sm q-px-md text-body1" icon="person" />
</template>

<script>
import { useAuth0 } from '@auth0/auth0-vue'
export default {
  setup () {
    const { loginWithRedirect } = useAuth0()
    return {
      login: () => {
        loginWithRedirect()
      }
    }
  },

  data () {
    return {
      loggedIn: false,
      user: {
        displayName: 'Hendrik Lankers'
      }
    }
  }

}
</script>
