<template>
  <!--<q-item :class="'q-my-sm q-mx-sm' + (this.fitsSearchTerm ? '' : ' hidden')" :style="
    selected // ? 'border: 3px solid #31CCEC; border-radius: 10px;'
      ? 'border: 3px solid #070; border-radius: 10px;'
      : 'border: 1px solid gray; border-radius: 10px;'
  ">-->
  <q-item :class="'q-my-sm q-mx-sm'" :style="`
      border: 3px solid ${lineColor}; border-radius: 10px;
  `">
    <q-item-section>
      <div class="row items-center no-wrap">
        <div class="column col-auto">
          <q-btn :icon="'expand_' + (expanded ? 'less' : 'more')" round dense size="md" glossy outline
            @click="toggleExpanded">
          </q-btn>
        </div>
        <!--<div class="column col-2 text-left q-ml-sm">
          <q-input autogrow dark outlined dense color="white" input-class="text-center text-body1" v-model="lineSymbol">
          </q-input>
        </div>-->
        <div class="column col-6 text-right q-mx-sm">
          <q-input autogrow dark outlined dense color="white" input-class="text-center text-h6" v-model="lineName">
          </q-input>
        </div>
        <div class="col col-grow">

        </div>
        <div class="col col-auto text-left text-body1">
          <q-btn icon="settings" dense round size="md">
            <q-menu fit>
              <q-list style="min-width: 150px" bordered>
                <q-item clickable @click.left="duplicateElement">
                  <q-item-section class="text-h6">Duplizieren</q-item-section>
                </q-item>
                <q-separator />
                <q-item clickable @click.left="deleteElement">
                  <q-item-section class="text-h6 text-negative">Löschen</q-item-section>
                </q-item>
                <q-separator />
              </q-list>
            </q-menu>
          </q-btn>
        </div>
      </div>
      <template v-if="expanded">
        <div class="row items-center q-my-sm q-mt-md">
          <div class="col col-3 text-center">Linienfarbe:</div>
          <div class="col col-4">
            <q-input v-model="lineColor" dense outlined color="white">
            </q-input>
          </div>
          <div class="col col-3 text-center">Linienbreite:</div>
          <div class="col col-2">
            <q-input v-model.number="lineWidth" dense type="number" step='0.1' outlined color="white">
            </q-input>
          </div>
        </div>

        <hr dark>

        <div class="row items-center q-my-sm">
          <div class="col col-2 text-center">Kante:</div>
          <div class="col col-2">
            <q-input v-model.number="locY" dense outlined color="white">
            </q-input>
          </div>
          <div class="col col-2 text-center">Breite:</div>
          <div class="col col-2">
            <q-input v-model.number="locX" dense type="number" outlined color="white">
            </q-input>
          </div>
          <div class="col col-2 text-center">Farbe:</div>
          <div class="col col-2">
            <q-input v-model.number="locY" dense outlined color="white">
            </q-input>
          </div>
        </div>

        <hr dark>
        <div class="row items-center q-my-sm text-body2">
          <div class="col col-12 text-left text-body1">Verbindungen:</div>
        </div>

        <div class="text-caption text-uppercase text-weight-light">
          Style:
        </div>

        <div class="text-caption text-uppercase text-weight-light">
          Beschriftung:
        </div>

        <div class="row items-center">
          <!--
            <div class="col col-4">
              <div class="row q-my-sm">
                <div class="col col-4 q-my-sm">
                  <q-icon size="sm">X</q-icon>
                  <q-tooltip class="text-body1 bg-indigo"> Offset X </q-tooltip>
                </div>
                <div class="col col-8">
                  <q-input v-model.number="shiftX" dense type="number" outlined color="white">
                  </q-input>
                </div>
              </div>
              <div class="row">
                <div class="col col-4 q-my-sm">
                  <q-icon size="sm">Y</q-icon>
                  <q-tooltip class="text-body1 bg-indigo"> Offset Y </q-tooltip>
                </div>
                <div class="col col-8">
                  <q-input v-model.number="shiftY" dense type="number" outlined color="white">
                  </q-input>
                </div>
              </div>
            </div>-->
        </div>
      </template>
    </q-item-section>
  </q-item>
</template>

<script>
import { usePlanEditorStore } from 'src/stores/editor_store'
import { storeToRefs } from 'pinia'
import { ref, toRefs } from 'vue'

const planEditorStore = usePlanEditorStore()

const { lines, searchTerm } = storeToRefs(planEditorStore)

export default {
  setup () {
    return {
      lines,
      width: undefined,
      expanded: ref(false),
      searchTerm,
      lineName: undefined,
      // lineSymbol: undefined,
      lineColor: undefined,
      lineWidth: undefined
    }
  },
  props: {
    lineid: String
  },
  created: function () {
    const reactiveLine = toRefs(this.lines[this.lineid])
    this.lineName = reactiveLine.name
    // this.lineSymbol = reactiveLine.symbol // this.lineid
    this.lineColor = reactiveLine.color
    this.lineWidth = reactiveLine.width

    /* if (this.nodes[this.nodeid].expanded === undefined) {
      this.nodes[this.nodeid].expanded = false
    }

    const reactiveNode = toRefs(this.nodes[this.nodeid])
    const reactiveLabel = toRefs(this.nodes[this.nodeid].label)

    this.nodeName = reactiveLabel.text
    this.expanded = reactiveNode.expanded
    this.labelClass = reactiveLabel.class
    this.labelVisible = reactiveNode.labelVisible
    this.nodeVisible = reactiveNode.nodeVisible

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

    // const reactiveAnchor = toRefs(this.nodes[this.nodeid].label.anchor)
    this.shiftX = reactiveLabel.shiftX
    this.shiftY = reactiveLabel.shiftY */
  },
  methods: {
    toggleExpanded: function () {
      this.expanded = !this.expanded
    }
    // toggleSelected: function () {
    //   if (this.selected) {
    //     this.selected = false
    //     this.selectedNodeIDs = this.selectedNodeIDs.filter(
    //       (v) => v !== this.nodeid
    //     )
    //   } else {
    //     this.selectedNodeIDs.push(this.nodeid)
    //     this.selected = true
    //   }
    // },
    // setLabelClass: function (cls) {
    //   this.labelClass = cls
    // },
    // deleteElement: function () {
    //   delete this.nodes[this.nodeid]
    //   this.selectedNodeIDs = this.selectedNodeIDs.filter(
    //     (e) => e !== this.nodeid
    //   )
    // },
    // duplicateElement: function () {
    //   this.nodes[this.nodeid + '_2'] = JSON.parse(
    //     JSON.stringify(this.nodes[this.nodeid])
    //   )
    //   this.selectedNodeIDs.push(this.nodeid + '_2')
    // }
  },
  watch: {
    // selectedNodeIDs: function (newVal) {
    //   if (newVal.length === 0) {
    //     this.selected = false
    //   }
    // }
  },
  computed: {
    // fitsSearchTerm: function () {
    //   return (
    //     !this.searchTerm ||
    //     this.nodeid.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
    //     this.nodes[this.nodeid]?.label?.text
    //       ?.toLowerCase()
    //       .includes(this.searchTerm.toLocaleLowerCase())
    //   )
    // }
  }

}
</script>
