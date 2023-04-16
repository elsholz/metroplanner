import axios from 'axios'
import { useAuth0 } from '@auth0/auth0-vue'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useUserStore } from './user_store'

export const usePlanEditorStore = defineStore('editorStore', {
  state: function () {
    const userStore = useUserStore()
    const planDetails = ref({})
    const planState = ref(undefined)
    const selectedNodeIDs = ref([])
    const nodes = ref({})
    const labels = ref({})
    const selectedLineIDs = ref(undefined)
    const selectedLabelIDs = ref(undefined)
    const planWidth = ref(0)
    const planHeight = ref(0)
    const globalOffsetX = ref(0)
    const globalOffsetY = ref(0)
    const coordinateScalar = ref(15)
    const searchTerm = ref('')
    const contextMenuOpen = ref(false)
    const lines = ref([])
    const editorMode = ref('viewer')

    return {
      planState,
      planDetails,
      userStore,
      selectedLabelIDs,
      selectedLineIDs,
      selectedNodeIDs,
      planWidth,
      planHeight,
      globalOffsetX,
      globalOffsetY,
      nodes,
      lines,
      labels,
      coordinateScalar,
      searchTerm,
      contextMenuOpen,
      editorMode
    }
  },

  actions: {
    loadPlanDetails: async function (planid) {
      console.log('loadPlan called with planid ', planid)
      console.log('Getting Token')
      const userStore = useUserStore()
      const token = await userStore.auth.getAccessTokenSilently()
      console.log('Got token')
      await axios
        .get('/api/_plans/' + planid, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        .then((response) => {
          console.log('Received plan details: ', response.data)
          this.planDetails = response.data
        })
    },

    loadPlanState: async function (planid, planstateid) {
      console.log(
        'Editor load planstate called for planid, planstateid',
        planid,
        planstateid
      )
      const userStore = useUserStore()
      const token = await userStore.auth.getAccessTokenSilently()

      await axios
        .get('/api/_plans/' + planid + '/_planstates/' + planstateid, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        .then((response) => {
          console.log('Received planstate: ', response.data)
          this.planState = response.data
          this.planHeight = this.planState.planHeight
          this.planWidth = this.planState.planWidth
          this.globalOffsetX = this.planState.globalOffsetX
          this.globalOffsetY = this.planState.globalOffsetY
          this.nodes = this.planState.nodes

          if (Array.isArray(this.planState.lines)) {
            const obj = {}
            for (const line of this.planState.lines) {
              obj[line.symbol] = line
              delete line.symbol
            }
            this.lines = obj
          } else {
            this.lines = this.planState.lines
          }
          delete this.planState.lines

          for (const k of Object.keys(this.nodes)) {
            const [x, y] = this.nodes[k].location

            this.nodes[k].marker.diagonalStretch = (this.nodes[k].marker.sizeFactor > 1) ?? false
            delete this.nodes[k].marker.sizeFactor

            this.nodes[k].locationX = x
            this.nodes[k].locationY = y
            this.nodes[k].labelVisible = true
            this.nodes[k].nodeVisible = true
            this.nodes[k].newNodeID = k
            this.nodes[k].selected = false

            if (!(typeof this.nodes[k].label === 'object')) {
              const labelKey = this.nodes[k].label
              try {
                delete this.planState.labels[labelKey]?.anchor?.node
                if (
                  Object.keys(this.planState.labels[labelKey].anchor).length ===
                  0
                ) {
                  delete this.planState.labels[labelKey]?.anchor
                }
              } catch {}
              this.nodes[k].label = this.planState.labels[labelKey]
              delete this.planState.labels[labelKey]
            }
            if (this.nodes[k].label === undefined) {
              this.nodes[k].label = {
                class: 'left',
                text: k
              }
            }
            this.nodes[k].label.shiftX = this.nodes[k].label.anchor?.shiftX ?? 0
            this.nodes[k].label.shiftY = this.nodes[k].label.anchor?.shiftY ?? 0
          }
          this.labels = this.planState.labels
          this.selectedNodeIDs = []
          delete this.planState.nodes
        })
    },

    savePlanState: async function (publish) {
      const { getAccessTokenSilently } = useAuth0()
      const token = await getAccessTokenSilently()

      if (this.planState !== undefined) {
        console.log(
          'Editor save planstate called for current planstate: ',
          this.planState
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
    },

    createNewPlan: async function (data) {
      console.log('Create plan called with data', data)
      const userStore = useUserStore()
      const token = await userStore.auth.getAccessTokenSilently()
      return await axios.post('/api/_plans', data, {
        headers: { Authorization: `Bearer ${token}` }
      })
      /* .then((response) => {
          console.log('Plan created successfully: ', response.data.planId)
          return response
        }) */
    }
  }
})
