import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'
import { Notify } from 'quasar'

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
            this.displayName = response.data.displayName || this.auth.user.name
            this.bio = response.data.bio
            this.isPublic = response.data.isPublic
            this.profilePicture = response.data.profilePicture || this.auth.user.picture
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
          Notify.create({
            message: 'Profil erfolgreich gespeichert',
            timeout: 3000,
            type: 'info'
          })
        })
        .catch((reason) => {
          console.log('error saving user data, reason: ', reason)
          Notify.create({
            message: `Fehler beim Speichern des Profils: ${reason}`,
            timeout: 5000,
            type: 'warning'
          })
        })
    },
    deletePlan: async function (planId, planName) {
      const token = await this.auth.getAccessTokenSilently()
      await axios
        .delete('/api/_plans/' + planId, {
          headers: { Authorization: `Bearer ${token}` }
        })
        .then(response => {
          this.plansCreated.forEach((element, index, array) => {
            if (element.planId === planId) {
              this.plansCreated.splice(index, 1)
              Notify.create(
                {
                  message: `»${planName}« wurde gelöscht.`,
                  timeout: 5000,
                  type: 'info'
                }
              )
            }
          })
        })
        .catch((reason) => {
          Notify.create(
            {
              message: `Fehler beim löschen von »${planName}«! ${reason}`,
              timeout: 10000,
              type: 'warning'
            }
          )
        })
    },
    createNewPlan: async function (data) {
      console.log('Create plan called with data', data)
      const token = await this.auth.getAccessTokenSilently()
      return await axios.post('/api/_plans', data, {
        headers: { Authorization: `Bearer ${token}` }
      })
    }
  }
})
