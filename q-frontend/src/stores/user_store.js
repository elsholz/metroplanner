import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useUserStore = defineStore('userStore', {
  state: () => {
    return {
      auth: ref({}),
      displayName: ref(undefined),
      bio: ref(undefined),
      profilePicture: ref(undefined),
      isPublic: ref(undefined),
      plansCreated: ref(undefined),
      profileLoaded: ref(false)
    }
  },
  actions: {
    init: async function (user, isAuthenticated, getAccessTokenSilently) {
      console.log('INIT called')
      this.auth = {
        isAuthenticated,
        getAccessTokenSilently,
        user
      }
    },
    loadUserProfile: async function () {
      console.log('Load User Profile called')
      if (this.auth.isAuthenticated && this.displayName === undefined) {
        const token = await this.auth.getAccessTokenSilently()

        console.log('Getting user profile info from API')
        await axios
          .get('/api/_user', {
            headers: { Authorization: `Bearer ${token}` }
          })
          .then((response) => {
            console.log('Response Data: ', response.data)
            this.displayName = response.data.displayName
            this.bio = response.data.bio
            this.isPublic = response.data.isPublic
            this.profilePicture = response.data.profilePicture
            this.plansCreated = response.data.plansCreated
            this.profileLoaded = true
          })
          .catch((reason) => {
            console.log(reason)
          })
      }
      console.log('Load user profile finished.')
    },
    updateUserProfile: async function (data) {
      console.log('Updating User Profile with data ', data)
      const token = await this.auth.getAccessTokenSilently()

      await axios
        .patch('/api/_user', data, {
          headers: { Authorization: `Bearer ${token}` }
        })
        .then((response) => {
          console.log('Response after updating profile:', response)
          console.log('New Userdata: ', response.data)
          const data = response.data
          this.displayName = data.displayName
          this.bio = data.bio
        })
        .catch((reason) => {
          console.log('error saving user data, reason: ', reason)
        })
    }
  }
})
