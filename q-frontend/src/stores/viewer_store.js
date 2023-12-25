import axios from 'axios'
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const usePlanViewerStore = defineStore('viewerStore', {
  state: () => ({
    plans: ref({})
  }),

  actions: {
    getPlanInfo: async function (shortlink) {
      console.log('Load plan called for shortlink', shortlink)
      if (Object.hasOwn(this.plans, shortlink)) {
        if (Object.hasOwn(this.plans[shortlink], 'info')) {
          return this.plans[shortlink].info
        }
      } else {
        this.plans[shortlink] = {}
      }

      await axios.get('/api/plans/' + shortlink).then((response) => {
        // const rawData = toRaw(response.data)
        // console.log('Raw Data:', rawData)
        this.plans[shortlink].info = response.data
        this.plans[shortlink].info.shortlink = shortlink

        return this.plans[shortlink].info
      })
    },
    getPlanState: async function (shortlink) {
      console.log('Load plan called for shortlink', shortlink)
      if (Object.hasOwn(this.plans, shortlink)) {
        if (Object.hasOwn(this.plans[shortlink], 'state')) {
          return this.plans[shortlink].info
        }
      } else {
        this.plans[shortlink] = {}
      }

      await axios.get('/api/planstates/' + shortlink).then((response) => {
        this.plans[shortlink].state = response.data
        this.plans[shortlink].state.shortlink = shortlink
      })
    }
  }

})
