import axios from 'axios'
import { useAuth0 } from '@auth0/auth0-vue'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useUserStore } from './user_store'

export const usePlanEditorStore = defineStore('editorStore', {
  state: function () {
    const userStore = useUserStore()
    const planDetails = ref({})
    const planStates = ref({})

    return {
    // Planstates by planstateId
      planStates,
      // Plan Details by planId
      planDetails,
      userStore
    }
  },

  actions: {
    loadPlanDetails: async function (planid) {
      console.log('loadPlan called with planid ', planid)
      console.log('Getting Token')
      const userStore = useUserStore()
      const token = await userStore.auth.getAccessTokenSilently()
      console.log('Got token')
      await axios.get('/api/_plans/' + planid, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }).then((response) => {
        console.log('Received plan details: ', response.data)
        console.log('THis is this:', this)
        this.planDetails[planid] = response.data
      })
    },
    loadPlanState: async function (planstateid) {
      console.log('Editor load planstate called for planstateid', planstateid)
      const userStore = useUserStore()
      const token = await userStore.auth.getAccessTokenSilently()

      await axios.get('/api/_planstates/' + planstateid, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
      ).then((response) => {
        console.log('Received planstate: ', response.data)
        this.planStates[planstateid] = response.data
      })
    },

    savePlanState: async function (planstateid, publish) {
      const { getAccessTokenSilently } = useAuth0()
      const token = await getAccessTokenSilently()

      if (this.planstate[planstateid] !== undefined) {
        console.log(
          'Editor save planstate called for current planstate: ',
          this.planstate
        )
        await axios
          .post('/api/_planstates', this.planstate, {
            headers: { Authorization: `Bearer ${token}` }
          })
          .then((response) => {
            console.log('Planstate created successfully')
            console.log(response)
            return response
          })
      } else console.log('Error saving planstate')
    }
  }
})
