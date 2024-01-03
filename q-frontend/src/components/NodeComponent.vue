<template>
  <div :class="'elabel e' + this.labelClass" v-if="labelVisible"
    :style="` border-radius: 0; top: ${topLabel}; left: ${leftLabel}; ${(selected && editorMode !== 'viewer' && editorMode !== 'settings') ? 'font-weight: bold; color: #31ccec' : ''}`">
    {{ nodeName }}
  </div>
  <div class="text-white emarker"
    :style="`top: ${topNode}; left: ${leftNode}; transform: rotate(${-rotation}deg); width: ${widthPixels}; height: ${heightPixels}; ${(selected && editorMode !== 'viewer' && editorMode !== 'settings') ? 'background-color: #31ccec;' : ''} ${(editorMode === 'nodes') ? 'cursor: ' + cursor + ';' : ''}`"
    v-if="nodeVisible" @mousedown.left.prevent="handleMouseDown">
  </div>
</template>

<style>
.emarker {
  border: 2px solid white;
  position: absolute;
  border-radius: 7px;
}

.emarker,
.eline_segment,
.elabel {
  position: absolute;
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
}

.eline_segment,
.emarker {
  transform-origin: top left;
}

.emarker {
  border-style: solid;
  border-color: #eef;
  color: #000;
  background-color: #004;
  transform-origin: top left;
  box-shadow: 0px 0px 3px 1px #aaf;
  box-sizing: border-box;
}

.elabel {
  transform-origin: right center;
  font-size: 12px;
  vertical-align: middle;
  white-space: nowrap;
  width: 0px;
}

.eleft,
.eleft_ascending,
.eleft_descending {
  direction: rtl;
  height: 15px;
  line-height: 15px;
  padding-right: 10px;
  transform: translateX(-10px);
}

.eleft_ascending {
  direction: rtl;
  transform: translateX(-10px) rotate(-45deg);
}

.eleft_descending {
  transform: translateX(-10px) rotate(45deg);
  text-align: right;
  direction: rtl;
}

.eright,
.eright_ascending,
.eright_descending {
  transform-origin: left center;
  width: 10px;
  padding-left: 10px;
  height: 15px;
  line-height: 15px;
}

.eright_ascending {
  transform-origin: left center;
  transform: rotate(-45deg);
}

.eright_descending {
  transform-origin: left center;
  transform: rotate(45deg);
}
</style>

<script>
import { storeToRefs } from 'pinia'
import { toRefs, ref } from 'vue'
import { usePlanEditorStore } from 'src/stores/editor_store'

const planEditorStore = usePlanEditorStore()

const { nodes, searchTerm, editorMode, coordinateScalar, globalOffsetX, selectedNodeIDs, globalOffsetY } =
  storeToRefs(planEditorStore)

export default {
  setup () {
    return {
      editorMode,
      nodes,
      globalOffsetX,
      globalOffsetY,
      nodeName: undefined,
      locX: ref(0),
      locY: ref(0),
      rotation: undefined,
      width: undefined,
      height: undefined,
      labelClass: undefined,
      shiftX: undefined,
      shiftY: undefined,
      selected: undefined,
      diagonalStretch: undefined,
      searchTerm,
      coordinateScalar,
      labelVisible: ref(undefined),
      nodeVisible: ref(undefined),
      selectedNodeIDs,
      dragInitialCoords: ref({}),
      initialLocation: ref(undefined),
      moved: false,
      cursor: ref('pointer')
    }
  },
  props: {
    nodeid: String
  },
  created: function () {
    const reactiveNode = toRefs(this.nodes[this.nodeid])
    const reactiveLabel = toRefs(this.nodes[this.nodeid].label)

    this.nodeName = reactiveLabel.text
    this.expanded = reactiveNode.expanded
    this.labelClass = reactiveLabel.class
    this.labelVisible = reactiveNode.labelVisible
    this.nodeVisible = reactiveNode.nodeVisible
    this.selected = reactiveNode.selected
    this.initialLocation = reactiveNode.initialLocation

    this.locX = reactiveNode.locX
    this.locY = reactiveNode.locY

    if (this.nodes[this.nodeid].marker.width === undefined) {
      this.nodes[this.nodeid].marker.width = 1
    }
    if (this.nodes[this.nodeid].marker.height === undefined) {
      this.nodes[this.nodeid].marker.height = 1
    }
    if (this.nodes[this.nodeid].marker.rotation === undefined) {
      this.nodes[this.nodeid].marker.rotation = 0
    }
    const reactiveMarker = toRefs(this.nodes[this.nodeid].marker)
    this.width = reactiveMarker.width
    this.height = reactiveMarker.height
    this.rotation = reactiveMarker.rotation
    this.diagonalStretch = reactiveMarker.diagonalStretch

    this.shiftX = reactiveLabel.shiftX
    this.shiftY = reactiveLabel.shiftY
  },
  computed: {
    leftNode: function () {
      return (
        this.getX(this.locX) -
        (Math.cos(this.degToRad(45 - this.rotation)) *
          Math.SQRT2 *
          this.coordinateScalar) /
        2 - this.coordinateScalar / 2 - 2 - 2 +
        'px'
      )
    },
    topNode: function () {
      return (
        this.getY(this.locY) -
        (Math.sin(this.degToRad(45 - this.rotation)) *
          Math.SQRT2 *
          this.coordinateScalar) /
        2 - this.coordinateScalar / 2 - 2 - 2 +
        'px'
      )
    },
    leftLabel: function () {
      return (
        this.getX(this.locX) - 1.0 * this.coordinateScalar + 3.5 +
        // this.shiftX * Math.cos(this.degToRad(90 + this.rotation)) * this.coordinateScalar - this.coordinateScalar +
        //  this.shiftX * (Math.cos(this.degToRad(45 - this.rotation)) *
        //   Math.SQRT2 *
        //   this.coordinateScalar) /
        // 2 - this.coordinateScalar / 2 - 2 - 2 +
        this.shiftX * this.coordinateScalar * (Math.sin(this.degToRad(90 - this.rotation))) * (this.diagonalStretch ? Math.SQRT2 : 1) +
        'px'
      )
    },
    topLabel: function () {
      return (
        this.getY(this.locY) - 1 * this.coordinateScalar - 4 -
        // this.shiftY * Math.sin(this.degToRad(90 + this.rotation)) * this.coordinateScalar - this.coordinateScalar +
        //  this.shiftY * (Math.sin(this.degToRad(45 - this.rotation)) *
        //   Math.SQRT2 *
        //   this.coordinateScalar) /
        // 2 - this.coordinateScalar / 2 - 2 +
        // - this.coordinateScalar / 2 - 2 +
        this.shiftX * this.coordinateScalar * (Math.cos(this.degToRad(-90 + this.rotation))) * (this.diagonalStretch ? Math.SQRT2 : 1) +
        'px'
      )
    },
    heightPixels () {
      return (
        (((this.height || 1) - 1) * (this.diagonalStretch ? Math.SQRT2 : 1) +
          1) *
        this.coordinateScalar +
        'px'
      )
    },
    widthPixels () {
      return (
        (((this.width || 1) - 1) * (this.diagonalStretch ? Math.SQRT2 : 1) +
          1) *
        this.coordinateScalar +
        'px'
      )
    }
  },
  methods: {
    degToRad (x) {
      return x / (180 / Math.PI)
    },
    getX (x) {
      return ((this.globalOffsetX) + x) * this.coordinateScalar
    },
    getY (y) {
      return ((this.globalOffsetY) + y) * this.coordinateScalar
    },
    handleDrag (event) {
      const diff = {
        x: Math.round((event.clientX - this.dragInitialCoords.x) / 15),
        y: Math.round((event.clientY - this.dragInitialCoords.y) / 15)
      }
      if (diff.x || diff.y) {
        this.moved = true
        console.log(diff)
      }

      for (const nodeid of this.selectedNodeIDs) {
        console.log(this.selectedNodeIDs, nodeid, this.nodes[nodeid])
        const newLoc = {
          x: this.nodes[nodeid].initialLocation[0] + diff.x,
          y: this.nodes[nodeid].initialLocation[1] + diff.y
        }
        this.nodes[nodeid].locX = newLoc.x
        this.nodes[nodeid].locY = newLoc.y
        console.log('New location for node', nodeid, ':', this.nodes[nodeid].locX)
      }
    },
    handleMouseDown (event) {
      this.cursor = 'move'
      console.log('adding event listener', event)
      this.dragInitialCoords = {
        x: event.clientX,
        y: event.clientY
      }
      // for (let nodeid of this.selectedNodeIDs){
      //   this.nodes[nodeid].initialLocation
      // }
      addEventListener('mousemove', this.handleDrag)
      addEventListener('mouseup', this.handleMouseUp)
    },
    handleMouseUp (event) {
      console.log('deregistering event handler', event)
      this.cursor = 'pointer'
      removeEventListener('mousemove', this.handleDrag)
      removeEventListener('mouseup', this.handleMouseUp)

      for (const nodeid of this.selectedNodeIDs) {
        this.nodes[nodeid].initialLocation = [
          this.nodes[nodeid].locX,
          this.nodes[nodeid].locY
        ]
      }

      if (this.editorMode === 'nodes' && !this.moved) {
        if (!event.shiftKey && !event.ctrlKey) {
          // create a new selection
          const unselect = this.selected
          for (const nodeid of this.selectedNodeIDs) {
            this.nodes[nodeid].selected = false
          }
          if (unselect && this.selectedNodeIDs.length === 1) {
            this.selectedNodeIDs = []
            this.selected = false
          } else {
            this.selectedNodeIDs = [this.nodeid]
            this.selected = true
          }
        } else if (event.shiftKey && !event.ctrlKey) {
          // expand selection to this node following paths
          console.log('Not implemented: following paths')
        } else if (!event.shiftKey && event.ctrlKey) {
          // add node to selection
          if (this.selected) {
            this.selected = false
            this.selectedNodeIDs = this.selectedNodeIDs.filter(
              (v) => v !== this.nodeid
            )
          } else {
            this.selectedNodeIDs.push(this.nodeid)
            this.selected = true
          }
        }
      }
      this.moved = false
    }
  }
}
</script>
