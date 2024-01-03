<template>
  <q-page>
    <div :style="'width:' +
      (planWidth * coordinateScalar + 100 + (contextMenuOpen ? 522.25 : 0)) +
      'px; height:' +
      (planHeight * coordinateScalar + 100) +
      'px;'
      ">
      <div
        :style="'width:' +
          (planWidth * coordinateScalar - 4) +
          'px; height:' +
          (planHeight * coordinateScalar - 4) +
          'px; background-color: #002; border: 2px solid white; position: absolute; left: ' + (50 - 2) + 'px; top: ' + (50 - 2) + 'px;'">
        <template v-for="line in this.lines" :key="line">
          <template v-for="connection in line.connections" :key="connection">
            <template v-if="connection.nodes.length > 1">
              <template v-for="n in (connection.nodes.length - 1)" :key="n">
                <LineSegmentComponent :color="line.color" :from="connection.nodes[n - 1]" :to="connection.nodes[n]"
                  :lineWidth="line.width || 0.5" :borderWidth="line.borderWidth" :borderStyle="line.borderStyle" :borderColor="line.borderColor"></LineSegmentComponent>
              </template>
            </template>
          </template>
        </template>

        <template v-for="k in Object.keys(this.nodes)" :key="k">
          <NodeComponent :nodeid="k"></NodeComponent>
        </template>

        <!--<div
        :style="`width: ${coordinateScalar}px; height: ${coordinateScalar}px; position: absolute; left: ${
          coordinateScalar * ((globalOffsetX % planWidth) - 0.5)
        }px; top: ${
          coordinateScalar * ((globalOffsetY % planHeight) - 0.5)
        }px; font-size: ${coordinateScalar}px;`"
        icon="add"
      >
      </div>-->
      </div>
    </div>
  </q-page>

  <!--{{ this.planEditorStore.planStates[this.planstateid] }}-->
  <!--
    <div id="canvas" v-if="planState && planState.nodes && planState.lines && planState.labels"
      :style="'background-color: ' + (colorTheme.themeData || {backgroundColor: '#001'}).backgroundColor  + '; '">
      <div id="lines">
        <div v-for="(line, key) in planState.lines" v-bind:key="key" style="z-index: 10;">
          <div v-for="(segment, segmentKey) in line.segments" v-bind:key="segmentKey"
            :style="getLineSegmentStyle(segmentKey, segment)" :class="'line_segment line' + key">
          </div>
        </div>
      </div>

      <div id="nodes">
        <div v-for="(node, nodeKey) in planState.nodes" v-bind:key="nodeKey" :id="nodeKey"
          :style="getNodeStyle(nodeKey, node)" class="marker">
        </div>
      </div>

      <div id="labels">
        <div v-for="(lbl, lblKey) in planState.labels" :key="lblKey">
          <div v-if="lbl.anchor.node" :style="getLabelStyle(lbl.anchor.node, planState.nodes[lbl.anchor.node])">
            <div :class="'label ' + lbl.class">
              {{ lbl.text }}
            </div>
          </div>
          <div v-else :class="'label ' + lbl.class" :style="getIndependentLabelStyle(lbl)">
            {{ lbl.text }}
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <q-inner-loading :showing="visible" :label="(planName || 'Plan wird geladen...')" label-class="text-white"
        class="bg-dark" label-style="font-size: 2em" color="white" size="7em" />
    </div>-->
</template>

<script>
import { ref } from 'vue'

import { usePlanEditorStore } from 'src/stores/editor_store'
import NodeComponent from 'src/components/NodeComponent.vue'
import { storeToRefs } from 'pinia'
import LineSegmentComponent from 'src/components/LineSegmentComponent.vue'

const planEditorStore = usePlanEditorStore()

const {
  planState,
  planWidth,
  planHeight,
  nodes,
  lines,
  coordinateScalar,
  globalOffsetX,
  globalOffsetY,
  contextMenuOpen
} = storeToRefs(planEditorStore)

export default {
  name: 'EditorCanvas',
  setup: function () {
    return {
      planEditorStore
    }
  },
  props: {},
  data () {
    return {
      visible: true,
      planState,
      lines,
      coordinateScalar,
      globalOffsetX,
      globalOffsetY,
      colorTheme: {},
      hasBeenMounted: false,
      labelTypes: {},
      noClickHandler: ref(false),
      planWidth,
      planHeight,
      contextMenuOpen,
      nodes
    }
  },
  methods: {
    clickEvent: function (event) {
      console.log(event)
    }
    // getNodeStyle (nodeKey, node) {
    //   return `
    //     left: ${this.getStationLeft(node.location[0], node.marker.rotation || 0)};
    //     top: ${this.getStationTop(node.location[1], node.marker.rotation || 0)};
    //     width: ${this.getStationWidth(node.marker)};
    //     height: ${this.getStationHeight(node.marker)};
    //     transform: rotate(${-node.marker.rotation}deg);
    //   `
    // },
    // getLineSegmentStyle (segmentKey, segment) {
    //   return `
    //     left: ${segment.left};
    //     top: ${segment.top};
    //     transform: ${segment.transform};
    //     width: ${segment.width};
    //     height: ${segment.height};
    //   `
    // },
    // getLabelStyle (nodeKey, node, labelKey, label) {
    //   const conP = this.getConnectionPoint(this.planState.labels[node.label].anchor)
    //   const locX = conP[0]
    //   const locY = conP[1]
    //   return `top: ${this.getY(locY)}px; left: ${this.getX(locX)}px; position: absolute; color: white;`
    // },
    // getIndependentLabelStyle (lbl) {
    //   if (['left', 'right', 'left_ascending', 'right_ascending', 'left_descending', 'left_ascending'].includes(lbl.class)) {
    //     const conP = this.getConnectionPoint(lbl.anchor)
    //     const locX = conP[0]
    //     const locY = conP[1]
    //     return `top: ${this.getY(locY)}px; left: ${this.getX(locX)}px; position: absolute; color: white;`
    //   } else if (['span'].includes(lbl.class)) {
    //     if (lbl.anchor.coords) {
    //       return `
    //       top: ${this.getY(lbl.anchor.coords[1])}px;
    //       left: ${this.getX(lbl.anchor.coords[0])}px;
    //       width: ${this.coordinateScalar * lbl.anchor.width}px;
    //       height: ${this.coordinateScalar * lbl.anchor.height}px;
    //       font-size: ${this.coordinateScalar * lbl.anchor.height}px;
    //       text-align: center;
    //       vertical-align: middle;
    //       color: white;
    //       position: absolute;
    //     `
    //     } else {
    //       console.log('missing node for ', lbl)
    //     }
    //   } else {
    //     throw Error
    //   }
    // },
    // addCSS: function () {
    //   if (this.hasBeenMounted && this.planState.lines) {
    //     let mapstyle = document.getElementById('style')
    //     if (mapstyle === null) {
    //       console.log('Creating new mapstyle elment')
    //       mapstyle = document.createElement('style')
    //     }
    //     mapstyle.id = 'mapstyle'
    //     for (const [key, line] of Object.entries(this.planState.lines)) {
    //       const text = `
    //         .line${key} {
    //           background-color: ${line.color || 'white'};
    //           border-radius: ${line.width * this.coordinateScalar / 2}px;
    //           box-shadow: 0px 0px 3px 1px ${line.color};
    //           border-width: ${2}px;
    //           border-style: ${line.borderStyle || 'solid'};
    //           border-color: ${line.borderColor || line.color};
    //         }
    //     `
    //       mapstyle.innerText += text
    //     }
    //     for (const [lbl, style] of Object.entries(this.labelTypes)) {
    //       const stl = style.style
    //       mapstyle.innerText += `
    //       .${lbl} {
    //       `
    //       for (const [k, v] of Object.entries(stl)) {
    //         mapstyle.innerText += `${k}: ${v};`
    //       }
    //       mapstyle.innerText += '}'
    //     }
    //     document.body.appendChild(mapstyle)
    //   }
    // },
    // getX (x) {
    //   return (20 + x) * this.coordinateScalar
    // },
    // getY (y) {
    //   return (7 + y) * this.coordinateScalar
    // },
    // degToRad (x) {
    //   return x / (180 / Math.PI)
    // },
    // getStationTop (locationY, rotation) {
    //   return this.getY(locationY) - Math.sin(this.degToRad(45 - rotation)) * Math.SQRT2 * this.coordinateScalar / 2 + 'px'
    // },
    // getStationLeft (locationX, rotation) {
    //   return this.getX(locationX) - Math.cos(this.degToRad(45 - rotation)) * Math.SQRT2 * this.coordinateScalar / 2 + 'px'
    // },
    // getStationHeight (marker) {
    //   return (((marker.height || 1) - 1) * (marker.sizeFactor || 1) + 1) * this.coordinateScalar + 'px'
    // },
    // getStationWidth (marker) {
    //   return (((marker.width || 1) - 1) * (marker.sizeFactor || 1) + 1) * this.coordinateScalar + 'px'
    // },
    // getConnectionPoint (anchor) {
    //   if (typeof anchor.node === 'string') {
    //     if (anchor.node in this.planState.nodes) {
    //       const nodeId = anchor.node
    //       const conPX = anchor.xShift || 0
    //       const conPY = anchor.yShift || 0
    //       const node = this.planState.nodes[nodeId]
    //       let locX = node.location[0]
    //       let locY = node.location[1]
    //       const rotation = node.marker.rotation || 0
    //       const sizeFactor = node.marker.sizeFactor || 1
    //       locX += Math.sin(this.degToRad(90 - rotation)) * conPX * sizeFactor// * Math.SQRT2 * coordinateScalar / 2
    //       locY -= Math.cos(this.degToRad(90 - rotation)) * conPX * sizeFactor// * Math.SQRT2 * coordinateScalar / 2
    //       if (conPY) {
    //         locX += Math.sin(this.degToRad(rotation)) * conPY * sizeFactor// * Math.SQRT2 * coordinateScalar / 2
    //         locY += Math.cos(this.degToRad(rotation)) * conPY * sizeFactor// * Math.SQRT2 * coordinateScalar / 2
    //       }
    //       return [locX, locY]
    //     }
    //   } else {
    //     return [anchor.node[0] + (anchor.xShift || 0), anchor.node[1] + (anchor.yShift || 0)]
    //   }
    // },
    // getTopShift (direction, width) {
    //   return -Math.sin(this.degToRad(45 + direction)) * Math.SQRT2 * width * this.coordinateScalar / 2
    // },
    // getLeftShift (direction, width) {
    //   return -Math.cos(this.degToRad(45 + direction)) * Math.SQRT2 * width * this.coordinateScalar / 2
    // }
  },
  mounted () {
    // this.addCSS()
    // console.log('this.refs::', this.$refs.el)
    // console.log(this.$route.params.shortlink)
    /* axios.get('/api/plan/' + this.$route.params.shortlink).then(response => {
          this.$refs.plan.innerText += JSON.stringify(response.data, null, 4)
          console.log(response)
        }) */
    // axios.get('/api/planstate/' + this.$route.params.shortlink).then(response => {
    //   // this.$refs.plandata.innerText += JSON.stringify(response.data, null, 4)
    //   // console.log(response)
    // })
  },
  watch: {
    planName: function (newVal, oldVal) {
      console.log('Plan Name changed from ', oldVal, ' to ', newVal)
    }
  },
  components: { NodeComponent, LineSegmentComponent }
}
</script>
