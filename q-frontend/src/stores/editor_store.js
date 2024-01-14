import axios from 'axios'
import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import { useUserStore } from './user_store'
import { Notify } from 'quasar'

export const usePlanEditorStore = defineStore('planEditorStore', {
  state: function () {
    const userStore = useUserStore()
    const planDetails = ref({})
    const planState = ref(undefined)
    const selectedNodeIDs = ref([])
    const planId = ref('')
    const planstateId = ref('')
    const selectedLineIDs = ref(undefined)
    const selectedLabelIDs = ref(undefined)
    const planWidth = ref(0)
    const planHeight = ref(0)
    const globalOffsetX = ref(0)
    const globalOffsetY = ref(0)
    const coordinateScalar = ref(15)
    const searchTerm = ref('')
    const contextMenuOpen = ref(false)
    const editorMode = ref('viewer')
    const saved = ref(true)
    const published = ref(true)
    const nodes = ref({})
    const lines = ref({})
    const independentLabels = ref({})
    const initialLoadFinished = ref(false)

    function onChange (event) {
      console.log('Changed!', event, initialLoadFinished)
      if (initialLoadFinished.value) {
        saved.value = false
        published.value = false
      }
    }

    watch([
      nodes,
      lines,
      independentLabels,
      planHeight,
      planWidth,
      globalOffsetX,
      globalOffsetY
    ], onChange, { deep: true })

    return {
      saved,
      published,
      initialLoadFinished,
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
      independentLabels,
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

            // if (!(typeof this.nodes[k].label === 'object')) {
            //   const labelKey = this.nodes[k].label
            //   try {
            //     delete this.planState.labels[labelKey]?.anchor?.node
            //     if (
            //       Object.keys(this.planState.labels[labelKey].anchor).length ===
            //       0
            //     ) {
            //       delete this.planState.labels[labelKey]?.anchor
            //     }
            //   } catch {}
            //   this.nodes[k].label = this.planState.labels[labelKey]
            //   delete this.planState.labels[labelKey]
            // }
            if (this.nodes[k].label === undefined) {
              this.nodes[k].label = {
                class: 'left',
                text: k
              }
            }
            this.nodes[k].label.shiftX = this.nodes[k].label.anchor?.shiftX ?? this.nodes[k].label.anchor?.xShift ?? 0
            this.nodes[k].label.shiftY = this.nodes[k].label.anchor?.shiftY ?? this.nodes[k].label.anchor?.yShift ?? 0
          }
          this.independentLabels = this.planState.independentLabels
          this.selectedNodeIDs = []
          delete this.planState.nodes
          delete this.planState.independentLabels
        })
    },

    savePlanState: async function (publish) {
      const userStore = useUserStore()
      const token = await userStore.auth.getAccessTokenSilently()

      const lines = {}
      for (const [lineid, line] of Object.entries(this.lines)) {
        console.log(lineid, line)
        const newLine = {}

        newLine.name = line.name
        newLine.color = line.color
        newLine.width = line.width
        newLine.border_width = line.border_width
        newLine.border_style = line.border_style
        newLine.border_color = line.border_color
        newLine.connections = line.connections

        lines[lineid] = newLine
      }

      const nodes = {}
      for (const [nodeid, node] of Object.entries(this.nodes)) {
        console.log(nodeid, node)
        const newNode = {}
        newNode.location = [node.locX, node.locY]

        newNode.marker = {}
        newNode.marker.width = node.marker.width
        newNode.marker.height = node.marker.height
        newNode.marker.sizeFactor = node.marker.diagonalStretch ? Math.sqrt(2) : 1
        newNode.marker.rotation = node.marker.rotation

        newNode.label = {}
        newNode.label.class = node.label.class
        newNode.label.text = node.label.text
        newNode.label.styling = node.label.styling
        newNode.label.anchor = {}
        newNode.label.anchor.xShift = node.label.shiftX
        newNode.label.anchor.yShift = node.label.shiftY

        nodes[nodeid] = newNode
      }

      const independentLabels = {}
      for (const [labelid, label] of Object.entries(this.independentLabels)) {
        console.log(labelid, label)

        const newLabel = {}

        newLabel.anchor = label.anchor
        newLabel.text = label.text
        newLabel.width = label.width
        newLabel.height = label.height
        newLabel.styling = label.styling

        independentLabels[labelid] = newLabel
      }

      const data = {
        lines,
        nodes,
        independentLabels,

        planWidth: this.planWidth,
        planHeight: this.planHeight,
        globalOffsetX: this.globalOffsetX,
        globalOffsetY: this.globalOffsetY,
        makeCurrent: publish
        // labelsOrdering: [],
        // linesOrdering: [],
        // nodesOrdering: []
        // colorTheme: "colorful-dl"
      }

      console.log('savePlanState called. This data will be saved:', data)

      await axios
        .post(`/api/_plans/${this.planId}/_planstates`, data, {
          headers: { Authorization: `Bearer ${token}` }
        })
        .then((response) => {
          console.log('Planstate created successfully')
          console.log(response)
          return response
        }).catch((response) => {
          console.log('Error posting planstate:', response)
        })
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
    },

    deleteNodes: function (nodes) {
      const newLines = {}
      for (const [lineid, line] of Object.entries(this.lines)) {
        const newConnections = []
        for (const anchors of Object.values(line.connections)) {
          newConnections.push({ nodes: anchors.nodes.filter((a) => !nodes.includes(a.node)) })
        }
        line.connections = newConnections
        newLines[lineid] = line
      }
      this.lines = newLines
      const newNodes = {}
      for (const [nodeid, node] of Object.entries(this.nodes)) {
        if (!nodes.includes(nodeid)) {
          newNodes[nodeid] = node
        }
      }
      this.nodes = newNodes
    }
  }
})
