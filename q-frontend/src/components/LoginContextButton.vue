<template>
  <q-space></q-space>
  <!--<q-btn :icon="$q.dark.isActive ? 'light_mode' : 'dark_mode'" @click="toggleDarkMode" outline class="q-mr-sm q-py-sm">
  </q-btn>-->
  <q-btn
    v-if="isAuthenticated"
    :label="$q.screen.gt.sm ? ( userStore.displayName || user.name ) : ''"
    color="green-5"
    outline
    class="q-pa-sm q-px-md text-body1"
    icon="person"
  >
    <q-menu class="bg-green" :offset="[0, 5]">
      <q-btn no-caps flat wrap class="q-ma-md" to="/profile">
        <div class="column">
          <div class="row">
            <div class="column col-12 items-center text-h6">
              {{ userStore.displayName || user.name }}
            </div>
          </div>
          <div class="row">
            <div class="column col-12 items-center text-h6">
              <q-avatar size="164px" class="q-ma-sm">
                <img :src="
                    this.userStore.profilePicture ||
                    'https://source.boringavatars.com/pixel/72/' +
                      this.user.sub +
                      '?colors=66f873,5a3dcf,99848a'
                " />
              </q-avatar>
            </div>
          </div>
          <q-tooltip class="text-body2">
            Profil öffnen
          </q-tooltip>
        </div>
      </q-btn>
      <div class="row">
        <div class="column col-12 items-center">
          <CreatePlanButton color="white"></CreatePlanButton>
          <q-btn color="red" no-caps class="q-ma-md" push v-close-popup @click="logout">
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
import { useUserStore } from 'src/stores/user_store'
import CreatePlanButton from './CreatePlanButton.vue'

const userStore = useUserStore()

export default {
  setup () {
    const { loginWithRedirect, user, isAuthenticated, getAccessTokenSilently, logout } = useAuth0()
    userStore.init(user, isAuthenticated, getAccessTokenSilently)
    userStore.loadUserProfile()
    return {
      login: async () => {
        loginWithRedirect()
      },
      user,
      isAuthenticated,
      userStore,
      logout: function () {
        logout({ logoutParams: { returnTo: window.origin } })
      }
    }
  },
  methods: {
    toggleDarkMode: function () {
      console.log('Toggling dark mode', this.$q.dark.isActive)
      this.$q.dark.toggle()
    }
  },
  watch: {
    isAuthenticated: async function (newValue) {
      console.log('Is Authenticated changed! ', newValue)
      await this.userStore.loadUserProfile()
    }
  },
  components: { CreatePlanButton }
}
</script>
