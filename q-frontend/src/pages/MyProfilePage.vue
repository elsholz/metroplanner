<template>
  <q-page padding> {{ displayName }} </q-page>
</template>

<script>
import { useAuth0 } from '@auth0/auth0-vue'
import axios from 'axios'
import { ref } from 'vue'

const displayName = ref(undefined)

export default {
  name: 'MyProfilePage',
  setup () {
    return {
      displayName
    }
  },
  created: async function () {
    const { user, isAuthenticated, getAccessTokenSilently } = useAuth0()

    console.log(isAuthenticated, user)

    const token = await getAccessTokenSilently()

    await axios
      .get('/api/_user', { headers: { Authorization: `Bearer ${token}` } })
      .then((response) => {
        console.log('Response from user api:', response)
        this.displayName = 'Hendrik Test'
      })
      .catch(console.log)
  }
}
</script>
