<template>
  <div :class="'elabel e' + this.labelClass" v-if="labelVisible" :style="`
        border-radius: 0;
        top: ${topLabel};
        left: ${leftLabel};
        ${(selected && editorMode !== 'viewer' && editorMode!=='settings') ? 'font-weight: bold; color: #31ccec' : ''}
      `">
    {{ nodeName }}
  </div>
  <div class="text-white emarker" :style="`
        top: ${topNode};
        left: ${leftNode};
        transform: rotate(${-rotation}deg);
        width: ${widthPixels};
        height: ${heightPixels};
        ${(selected && editorMode !== 'viewer' && editorMode !=='settings') ? 'background-color: #31ccec;' : ''}
        ${(editorMode==='nodes') ? 'cursor: pointer;' : ''}
      `" v-if="nodeVisible"
      @click.left.prevent="handleClick">
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
      selectedNodeIDs
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

    this.locY = reactiveNode.locationY
    this.locX = reactiveNode.locationX

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
    handleClick (event) {
      if (this.editorMode === 'nodes') {
        if (!event.shiftKey && !event.ctrlKey) {
        // create a new selection
          for (const nodeid of this.selectedNodeIDs) {
            this.nodes[nodeid].selected = false
          }
          this.selectedNodeIDs = [this.nodeid]
          this.selected = true
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
    }
  }
}
</script>
