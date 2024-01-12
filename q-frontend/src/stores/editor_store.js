import axios from 'axios'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useUserStore } from './user_store'
import { Notify } from 'quasar'

export const usePlanEditorStore = defineStore('planEditorStore', {
  state: function () {
    const userStore = useUserStore()
    const planDetails = ref({})
    const planState = ref(undefined)
    const selectedNodeIDs = ref([])
    const nodes = ref({})
    const planId = ref('')
    const planstateId = ref('')
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
      planId,
      planstateId,
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
          this.planId = planid
          this.planstateId = planstateid

          // if (Array.isArray(this.planState.lines)) {
          //   const obj = {}
          //   for (const line of this.planState.lines) {
          //     obj[line.name] = line
          //     delete line.name
          //   }
          //   this.lines = obj
          // } else {
          this.lines = this.planState.lines
          // }
          // delete this.planState.lines

          for (const k of Object.keys(this.nodes)) {
            const [x, y] = this.nodes[k].location

            this.nodes[k].marker.diagonalStretch = (this.nodes[k].marker.sizeFactor > 1) ?? false
            delete this.nodes[k].marker.sizeFactor

            this.nodes[k].locX = x
            this.nodes[k].locY = y
            this.nodes[k].labelVisible = true
            this.nodes[k].nodeVisible = true
            this.nodes[k].newNodeID = k
            this.nodes[k].selected = false
            this.nodes[k].initialLocation = [x, y]

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
            this.nodes[k].label.shiftX = this.nodes[k].label.anchor?.shiftX ?? this.nodes[k].label.anchor?.xShift ?? 0
            this.nodes[k].label.shiftY = this.nodes[k].label.anchor?.shiftY ?? this.nodes[k].label.anchor?.yShift ?? 0
          }
          this.labels = this.planState.labels
          this.selectedNodeIDs = []
          delete this.planState.nodes
        })
    },

    savePlanState: async function (publish) {
      const userStore = useUserStore()
      const token = await userStore.auth.getAccessTokenSilently()

      console.log('savePlanState called. This is planState:', this.planState)

      if (this.planState !== undefined) {
        console.log(
          'Editor save planstate called for current planstate: ',
          this.planState
        )
        await axios
          .post(`/api/_plans/${this.planId}/_planstates`, this.planState, {
            headers: { Authorization: `Bearer ${token}` },
            params: {
              'make-current': publish || false
            }
          })
          .then((response) => {
            console.log('Planstate created successfully')
            console.log(response)
            return response
          })
      } else console.log('Error saving planstate')
    },

    savePlanInfo: async function (planId, data) {
      const userStore = useUserStore()
      const token = await userStore.auth.getAccessTokenSilently()
      await axios
        .patch('/api/_plans/' + planId, data, {
          headers: { Authorization: `Bearer ${token}` }
        })
        .then(response => {
          this.planDetails.currentState = response.currentState ?? this.planDetails.currentState
          this.planDetails.planName = response.planName ?? this.planDetails.planName
          this.planDetails.planDescription = response.planDescription ?? this.planDetails.planDescription

          Notify.create(
            {
              message: 'Änderungen wurden gespeichert.',
              timeout: 5000,
              type: 'info'
            }
          )
        })
        .catch((reason) => {
          Notify.create(
            {
              message: `Fehler! ${reason}`,
              timeout: 10000,
              type: 'warning'
            }
          )
        })
    }
  }
})
