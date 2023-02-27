import axios from 'axios'
import { defineStore } from 'pinia'
import { ref, toRaw } from 'vue'

export const usePlanViewerStore = defineStore('planViewerStore', {
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
        const rawData = toRaw(response.data)
        console.log('Raw Data:', rawData)
        this.plans[shortlink].info = rawData
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
        const rawData = toRaw(response.data)
        console.log('Raw Data:', rawData)
        this.plans[shortlink].state = rawData
        this.plans[shortlink].state.shortlink = shortlink
      })
    }
  }

})
