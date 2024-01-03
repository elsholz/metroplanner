<template>
  <div
    :style="`background-color: ${color}; height: ${height}; width: ${width}; top: ${top}; left: ${left}; transform: ${transform}; border-radius: ${(borderRadius || lineWidth) / 2 * coordinateScalar}px; border-style: ${borderStyle || 'solid'}; border-width: ${(borderWidth * coordinateScalar) || 2}px; border-color: ${borderColor || color}; box-shadow: 0px 0px 3px 1px ${color};`"
    class="line_segment">
  </div>
</template>

<style>
.marker,
.line_segment,
.label,
.wrapper,
.regularStop {
  position: absolute;
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
  border-radius: 8px;
}

.line_segment,
.marker {
  transform-origin: top left;
}
</style>

<script>
import { storeToRefs } from 'pinia'
import { usePlanEditorStore } from 'src/stores/editor_store'
import { ref, toRaw } from 'vue'

const planEditorStore = usePlanEditorStore()

const { nodes, coordinateScalar, globalOffsetX, globalOffsetY } =
  storeToRefs(planEditorStore)

export default {
  setup () {
    return {
      coordinateScalar,
      globalOffsetX,
      globalOffsetY,
      nodes,
      fromNode: ref(undefined),
      toNode: ref(undefined)
    }
  },
  props: {
    from: Object,
    to: Object,
    lineWidth: Number,
    color: String,
    borderStyle: String,
    borderRadius: Number,
    borderColor: String,
    borderWidth: Number
  },
  created: function () {
    this.fromNode = this.nodes[this.from.node] ?? this.from
    this.toNode = this.nodes[this.to.node] ?? this.to

    // if (this.fromNode.locationX === undefined || this.toNode.locationX === undefined) {
    //   console.log('FROM Node, TO Node', this.fromNode, this.toNode)
    // }
  },
  computed: {
    length: function () {
      const [dx, dy] = this.delta
      return Math.sqrt(dx ** 2 + dy ** 2)
    },
    transform: function () {
      return `rotate(${this.direction}deg)`
    },
    width: function () {
      return this.lineWidth * this.coordinateScalar + this.length * this.coordinateScalar + 'px' // ((value.height * coordinate_scalar) || 16) + "px"
    },
    height: function () {
      return this.lineWidth * this.coordinateScalar + 'px'
    },
    delta: function () {
      // const from = this.getConnectionPoint(this.from)
      // const to = this.getConnectionPoint(this.to)
      const f = { ...this.from, node: this.fromNode }
      const from = this.getConnectionPoint(f)
      const t = { ...this.to, node: this.toNode }
      const to = this.getConnectionPoint(t)

      const dx = to[0] - from[0]
      const dy = to[1] - from[1]

      return [dx, dy]
    },
    direction: function () {
      const [dx, dy] = this.delta
      return (360 + 90 - (Math.atan2(dx, dy)) * (180 / Math.PI)) % 360
    },
    left: function () {
      // const from = this.getConnectionPoint(this.from)
      const f = { ...this.from, node: this.fromNode }
      const from = this.getConnectionPoint(f)
      return this.getLeftShift(this.direction, this.lineWidth) + this.getX(from[0]) - 4 - 15 / 2 + 'px'
    },
    top: function () {
      // const from = this.getConnectionPoint(this.from)
      const f = { ...this.from, node: this.fromNode }
      const from = this.getConnectionPoint(f)
      return this.getTopShift(this.direction, this.lineWidth) + this.getY(from[1]) - 4 - 15 / 2 + 'px'
    }
  },

  methods: {
    getX (x) {
      return ((this.globalOffsetX) + x) * this.coordinateScalar
    },
    getY (y) {
      return ((this.globalOffsetY) + y) * this.coordinateScalar
    },
    getTopShift (direction, width) {
      return -Math.sin(this.degToRad(45 + direction)) * Math.SQRT2 * width * this.coordinateScalar / 2
    },
    getLeftShift (direction, width) {
      return -Math.cos(this.degToRad(45 + direction)) * Math.SQRT2 * width * this.coordinateScalar / 2
    },
    degToRad (x) {
      return x / (180 / Math.PI)
    },
    getConnectionPoint: function (anchor) {
      // console.log('Anchor:', anchor, anchor.node.locationX)
      if (anchor.node.locX !== undefined) {
        // if (anchor.node in this.nodes) {
        // const nodeId = anchor.node
        const conPX = anchor.xShift || 0
        const conPY = anchor.yShift || 0

        const node = anchor.node // this.nodes[nodeId]
        // let locX = node.location[0]
        // let locY = node.location[1]
        let locX = node?.locX || 0
        let locY = node?.locY || 0
        const rotation = node?.marker?.rotation || 0
        const sizeFactor = node?.marker?.diagonalStretch ? Math.SQRT2 : 1

        locX += Math.sin(this.degToRad(90 - rotation)) * conPX * sizeFactor// * Math.SQRT2 * coordinateScalar / 2
        locY -= Math.cos(this.degToRad(90 - rotation)) * conPX * sizeFactor// * Math.SQRT2 * coordinateScalar / 2

        if (conPY) {
          locX += Math.sin(this.degToRad(rotation)) * conPY * sizeFactor// * Math.SQRT2 * coordinateScalar / 2
          locY += Math.cos(this.degToRad(rotation)) * conPY * sizeFactor// * Math.SQRT2 * coordinateScalar / 2
        }

        return [locX, locY]
        // }
      } else {
        return [toRaw(anchor.node).node[0], toRaw(anchor.node).node[1]]
      }
    }
  },
  watch: {
  }

}
</script>
