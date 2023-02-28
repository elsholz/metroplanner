<template>
  <q-space></q-space>
  <q-btn
    v-if="isAuthenticated"
    :label="$q.screen.gt.sm ? user : ''"
    color="green-5"
    outline
    class="q-pa-sm q-px-md text-body1"
    icon="person"
  >
    <q-menu class="bg-green" :offset="[0, 5]" dark>
      <q-btn no-caps flat wrap class="q-ma-md">
        <div class="column">
          <div class="row">
            <div class="column col-12 items-center text-h6">
              {{ user }}
            </div>
          </div>
          <div class="row">
            <div class="column col-12 items-center text-h6">
              <q-avatar size="164px" class="q-ma-sm">
                <img src="/images/profile_image.jpg" />
              </q-avatar>
            </div>
          </div>
          <div class="row">
            <div
              class="column col-12 items-center text-body1 text-weight-light"
            >
              Profil öffnen
            </div>
          </div>
        </div>
      </q-btn>
      <div class="row">
        <div class="column col-12 items-center">
          <q-btn color="red" no-caps class="q-ma-md" push v-close-popup>
            Logout
          </q-btn>
        </div>
      </div>
    </q-menu>
  </q-btn>
  <q-btn
    v-else
    @click="login"
    no-caps
    :label="$q.screen.gt.sm ? 'Login' : ''"
    color="green-6"
    class="q-pa-sm q-px-md text-body1"
    icon="person"
  />
</template>

<script>
import { useAuth0 } from '@auth0/auth0-vue'

export default {
  setup () {
    const { loginWithRedirect, user, isAuthenticated } = useAuth0()
    return {
      login: () => {
        loginWithRedirect()
        console.log('User:', user)
        console.log('isAuthenticated:', isAuthenticated)
      },
      user,
      isAuthenticated
    }
  },

  data () {
    return {}
  }
}
</script>
