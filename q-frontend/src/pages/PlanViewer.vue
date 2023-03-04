<template>
  <q-page padding dark>
    <div id="canvas" v-if="planState && planState.nodes && planState.lines && planState.labels"
      :style="'background-color: ' + (colorTheme.themeData || {backgroundColor: '#001'}).backgroundColor  + '; '">
      <div :style="`transform: scale(${planState.scaleFactor || 0.8}); height: ${planState.planHeight * coordinateScalar}px; width: ${planState.planWidth * coordinateScalar}px; border: 1px solid white;`">
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
    </div>
    <div v-else>
      <q-inner-loading :showing="visible" :label="(planName || 'Plan wird geladen...')" label-class="text-white"
        class="bg-dark" label-style="font-size: 2em" color="white" size="7em" />
    </div>
  </q-page>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PlanViewer',
  props: {
    planName: String
  },
  data () {
    return {
      planState: {},
      visible: true,
      coordinateScalar: 15,
      colorTheme: {},
      hasBeenMounted: false,
      labelTypes: {

      }
    }
  },
  created () {
    axios.get('/api/planstates/' + this.$route.params.shortlink).then(response => {
      console.log('Planstate response data:', response.data)
      axios.get('/api/colorthemes/' + response.data.colorTheme, {
        'Access-Control-Allow-Origin': '*'
      }).then(response => {
        this.colorTheme = response.data
      }).catch(function (error) {
        console.log('Error fetching Color theme: ', error)
      })
      this.planState = response.data
      this.addCSS()

      for (const line of this.planState.lines) {
        line.segments = []
        for (const connections of line.connections) {
          for (let i = 0; i < connections.nodes.length - 1; i++) {
            const outboundStation = connections.nodes[i]
            const inboundStation = connections.nodes[i + 1]

            const from = this.getConnectionPoint(outboundStation)
            const to = this.getConnectionPoint(inboundStation)

            const dx = to[0] - from[0]
            const dy = to[1] - from[1]

            const direction = (360 + 90 - (Math.atan2(dx, dy)) * (180 / Math.PI)) % 360
            const length = Math.sqrt(dx ** 2 + dy ** 2)

            line.segments.push({
              left: this.getLeftShift(direction, line.width) + this.getX(from[0]) + 'px',
              top: this.getTopShift(direction, line.width) + this.getY(from[1]) + 'px',
              transform: `rotate(${direction}deg)`,
              width: line.width * this.coordinateScalar + length * this.coordinateScalar + 'px', // ((value.height * coordinate_scalar) || 16) + "px",
              height: (line.width) * this.coordinateScalar + 'px'
            })
          }
        }
      }

      this.visible = false
    })
  },
  methods: {
    getNodeStyle (nodeKey, node) {
      return `
        left: ${this.getStationLeft(node.location[0], node.marker.rotation || 0)};
        top: ${this.getStationTop(node.location[1], node.marker.rotation || 0)};
        width: ${this.getStationWidth(node.marker)};
        height: ${this.getStationHeight(node.marker)};
        transform: rotate(${-node.marker.rotation}deg);
      `
    },
    getLineSegmentStyle (segmentKey, segment) {
      return `
        left: ${segment.left};
        top: ${segment.top};
        transform: ${segment.transform};
        width: ${segment.width};
        height: ${segment.height};
      `
    },
    getLabelStyle (nodeKey, node, labelKey, label) {
      const conP = this.getConnectionPoint(this.planState.labels[node.label].anchor)
      const locX = conP[0]
      const locY = conP[1]
      return `top: ${this.getY(locY)}px; left: ${this.getX(locX)}px; position: absolute; color: white;`
    },
    getIndependentLabelStyle (lbl) {
      if (['left', 'right', 'left_ascending', 'right_ascending', 'left_descending', 'left_ascending'].includes(lbl.class)) {
        const conP = this.getConnectionPoint(lbl.anchor)
        const locX = conP[0]
        const locY = conP[1]
        return `top: ${this.getY(locY)}px; left: ${this.getX(locX)}px; position: absolute; color: white;`
      } else if (['span'].includes(lbl.class)) {
        if (lbl.anchor.coords) {
          return `
          top: ${this.getY(lbl.anchor.coords[1])}px;
          left: ${this.getX(lbl.anchor.coords[0])}px;
          width: ${this.coordinateScalar * lbl.anchor.width}px;
          height: ${this.coordinateScalar * lbl.anchor.height}px;
          font-size: ${this.coordinateScalar * lbl.anchor.height}px;
          text-align: center;
          vertical-align: middle;
          color: white;
          position: absolute;
        `
        } else {
          console.log('missing node for ', lbl)
        }
      } else {
        throw Error
      }
    },
    addCSS: function () {
      if (this.hasBeenMounted && this.planState.lines) {
        let mapstyle = document.getElementById('style')
        if (mapstyle === null) {
          console.log('Creating new mapstyle elment')
          mapstyle = document.createElement('style')
        }
        mapstyle.id = 'mapstyle'

        for (const [key, line] of Object.entries(this.planState.lines)) {
          const text = `
            .line${key} {
              background-color: ${line.color || 'white'};
              border-radius: ${line.width * this.coordinateScalar / 2}px;
              box-shadow: 0px 0px 3px 1px ${line.color};
              border-width: ${2}px;
              border-style: ${line.borderStyle || 'solid'};
              border-color: ${line.borderColor || line.color};
            }
        `
          mapstyle.innerText += text
        }

        for (const [lbl, style] of Object.entries(this.labelTypes)) {
          const stl = style.style

          mapstyle.innerText += `
          .${lbl} {
          `
          for (const [k, v] of Object.entries(stl)) {
            mapstyle.innerText += `${k}: ${v};`
          }

          mapstyle.innerText += '}'
        }

        document.body.appendChild(mapstyle)
      }
    },
    getX (x) {
      return ((this.planState.globalOffsetX || 20) + x) * this.coordinateScalar
    },
    getY (y) {
      return ((this.planState.globalOffsetY || 7) + y) * this.coordinateScalar
    },
    degToRad (x) {
      return x / (180 / Math.PI)
    },
    getStationTop (locationY, rotation) {
      return this.getY(locationY) - Math.sin(this.degToRad(45 - rotation)) * Math.SQRT2 * this.coordinateScalar / 2 + 'px'
    },
    getStationLeft (locationX, rotation) {
      return this.getX(locationX) - Math.cos(this.degToRad(45 - rotation)) * Math.SQRT2 * this.coordinateScalar / 2 + 'px'
    },
    getStationHeight (marker) {
      return (((marker.height || 1) - 1) * (marker.sizeFactor || 1) + 1) * this.coordinateScalar + 'px'
    },
    getStationWidth (marker) {
      return (((marker.width || 1) - 1) * (marker.sizeFactor || 1) + 1) * this.coordinateScalar + 'px'
    },
    getConnectionPoint (anchor) {
      if (typeof anchor.node === 'string') {
        if (anchor.node in this.planState.nodes) {
          const nodeId = anchor.node
          const conPX = anchor.xShift || 0
          const conPY = anchor.yShift || 0

          const node = this.planState.nodes[nodeId]
          let locX = node.location[0]
          let locY = node.location[1]
          const rotation = node.marker.rotation || 0
          const sizeFactor = node.marker.sizeFactor || 1

          locX += Math.sin(this.degToRad(90 - rotation)) * conPX * sizeFactor// * Math.SQRT2 * coordinateScalar / 2
          locY -= Math.cos(this.degToRad(90 - rotation)) * conPX * sizeFactor// * Math.SQRT2 * coordinateScalar / 2

          if (conPY) {
            locX += Math.sin(this.degToRad(rotation)) * conPY * sizeFactor// * Math.SQRT2 * coordinateScalar / 2
            locY += Math.cos(this.degToRad(rotation)) * conPY * sizeFactor// * Math.SQRT2 * coordinateScalar / 2
          }

          return [locX, locY]
        }
      } else {
        return [anchor.node[0] + (anchor.xShift || 0), anchor.node[1] + (anchor.yShift || 0)]
      }
    },
    getTopShift (direction, width) {
      return -Math.sin(this.degToRad(45 + direction)) * Math.SQRT2 * width * this.coordinateScalar / 2
    },
    getLeftShift (direction, width) {
      return -Math.cos(this.degToRad(45 + direction)) * Math.SQRT2 * width * this.coordinateScalar / 2
    }

  },
  mounted () {
    this.hasBeenMounted = true
    this.addCSS()
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
  }
}
</script>
