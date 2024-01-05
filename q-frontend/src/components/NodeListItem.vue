<template>
  <q-item :class="'q-my-sm q-mx-sm' + (this.fitsSearchTerm ? '' : ' hidden')" :style="
    selected
      ? 'border: 1px solid #070; border-radius: 10px; box-shadow: 0 0 3px 0 lime;'
      : 'border: 1px solid gray; border-radius: 10px;'
  ">
    <q-item-section>
      <div class="row items-center no-wrap">
        <div class="col col-auto">
          <q-btn rounded v-model="selected" :color="selected ? 'secondary' : ''" dense flat size="md"
            :icon="selected ? 'radio_button_checked': 'radio_button_unchecked'" @click="toggleSelected">
            <q-tooltip anchor="top middle" self="bottom middle">
              {{ selected ? "Unselect" : "Select" }} {{ nodeName }}
            </q-tooltip>
          </q-btn>
        </div>
        <div class="col col-3 text-left text-body1">
          <q-input autogrow dark outlined dense color="white" input-class="text-center text-body2" v-model="newNodeID">
          </q-input>
        </div>
        <div class="col col-6 text-right q-mx-sm">
          <q-input autogrow dark outlined dense color="white" input-class="text-center text-h6" v-model="nodeName">
          </q-input>
        </div>
        <div class="col col-shrink q-mr-sm text-left text-body1">
          <q-btn icon="settings" dense round size="md">
            <q-menu fit>
              <q-list style="min-width: 150px" bordered>
                <q-item clickable @click.left="duplicateElement">
                  <q-item-section class="text-body1">Duplizieren</q-item-section>
                </q-item>
                <q-separator />
                <q-item clickable @click.left="deleteElement">
                  <q-item-section class="text-body1 text-negative">Löschen</q-item-section>
                </q-item>
                <q-separator />
              </q-list>
            </q-menu>
          </q-btn>
        </div>
        <div class="col col-shrink">
          <q-btn :icon="'expand_' + (expanded ? 'less' : 'more')" round dense size="md" glossy outline
            @click="toggleExpanded">
          </q-btn>
        </div>
      </div>
      <template v-if="expanded">
        <div class="row items-center q-my-sm">
          <div class="col col-2 q-mx-md text-center">Koordinaten:</div>
          <div class="col col-1 text-right q-mx-sm">X:</div>
          <div class="col col-3">
            <q-input v-model.number="locX" dense type="number" outlined color="white">
            </q-input>
          </div>
          <div class="col col-1 text-right q-mx-sm">Y:</div>
          <div class="col col-3">
            <q-input v-model.number="locY" dense type="number" outlined color="white">
            </q-input>
          </div>
        </div>

        <div class="row q-my-sm items-center center">
          <div class="column col-4 items-center">
            <q-toggle dense v-model="labelVisible" color="purple" :icon="labelVisible ? 'visibility' : 'visibility_off'"
              label="Beschriftung" size="lg" class="text-body2" />
          </div>
          <div class="column col-4 items-center">
            <q-toggle dense v-model="nodeVisible" color="indigo" :icon="nodeVisible ? 'visibility' : 'visibility_off'"
              label="Markierung" size="lg" class="text-body2" />
          </div>
          <div class="column col-4 items-center">
            <q-toggle dense v-model="diagonalStretch" color="green" :disable="!nodeVisible" label="Diagonal" size="lg"
              class="text-body2" />
          </div>
        </div>

        <template v-if="nodeVisible">
          <div class="text-caption text-uppercase text-weight-light">
            Markierung:
          </div>

          <div class="row items-center q-mb-sm">
            <div class="col col-2 text-center">Rotation:</div>
            <div class="col col-2">
              <q-input v-model.number="rotation" dense step=45 suffix="°" type="number" outlined color="white">
              </q-input>
            </div>
            <div class="col col-2 text-center">Breite:</div>
            <div class="col col-2">
              <q-input v-model.number="width" dense type="number" outlined color="white">
              </q-input>
            </div>
            <div class="col col-2 text-center">Höhe:</div>
            <div class="col col-2">
              <q-input v-model.number="height" dense type="number" outlined color="white">
              </q-input>
            </div>
          </div>
        </template>
        <template v-if="labelVisible">
          <div class="text-caption text-uppercase text-weight-light">
            Beschriftung:
          </div>
          <div class="row items-center">
            <div class="col col-8" style="height: 170px">
              <q-btn no-caps round size="25px" outline :color="labelClass === 'center' ? 'info' : ''"
                @click.left="setLabelClass('center')" style="
                    width: 40px;
                    height: 40px;
                    transform: translateX(110px) translateY(47.5px);
                    transform-origin: middle left;
                  ">
                center
              </q-btn>
              <q-btn no-caps size="15px" outline :color="labelClass === 'left' ? 'info' : ''"
                @click.left="setLabelClass('left')" style="width: 50px; transform: translateX(-25px) translateY(50px)">
                left
              </q-btn>
              <q-btn no-caps size="15px" outline :color="labelClass === 'left_descending' ? 'info' : ''"
                @click.left="setLabelClass('left_descending')" style="
                    width: 50px;
                    transform: translateX(-50px) translateY(-5px) rotate(45deg);
                  ">
                l-desc
              </q-btn>
              <q-btn no-caps size="15px" outline :color="labelClass === 'left_ascending' ? 'info' : ''"
                @click.left="setLabelClass('left_ascending')" style="
                    width: 50px;
                    transform: translateX(-100px) translateY(100px) rotate(-45deg);
                  ">
                l-asc
              </q-btn>

              <q-btn no-caps size="15px" outline :color="labelClass === 'right' ? 'info' : ''"
                @click.left="setLabelClass('right')" style="width: 50px; transform: translateX(-30px) translateY(50px)">
                right
              </q-btn>
              <q-btn no-caps size="15px" outline :color="labelClass === 'right_ascending' ? 'info' : ''"
                @click.left="setLabelClass('right_ascending')" style="
                    width: 50px;
                    transform: translateX(170px) translateY(-60px) rotate(-45deg);
                  ">
                r-asc
              </q-btn>
              <q-btn no-caps size="15px" outline :color="labelClass === 'right_descending' ? 'info' : ''"
                @click.left="setLabelClass('right_descending')" style="
                    width: 50px;
                    transform: translateX(120px) translateY(45px) rotate(45deg);
                  ">
                r-desc
              </q-btn>
            </div>
            <div class="col col-4">
              <!--<div class="row">
              <div class="col col-4 q-py-xs">
                <q-icon name="format_size" size="md">
                  <q-tooltip class="text-body1 bg-indigo">
                    Schriftgröße
                  </q-tooltip>
                </q-icon>
              </div>
              <div class="col col-8">
                <q-input
                  v-model.number="labelFontSize"
                  dense
                  type="number"
                  outlined
                  color="white"
                >
                </q-input>
              </div>
            </div>-->
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
            </div>
          </div>
        </template>
      </template>
    </q-item-section>
  </q-item>
</template>

<script>
import { usePlanEditorStore } from 'src/stores/editor_store'
import { storeToRefs } from 'pinia'
import { toRefs, ref } from 'vue'

const planEditorStore = usePlanEditorStore()

const { nodes, selectedNodeIDs, searchTerm } = storeToRefs(planEditorStore)

export default {
  setup () {
    return {
      nodes,
      selectedNodeIDs,
      nodeName: undefined,
      locX: undefined,
      locY: undefined,
      rotation: undefined,
      width: undefined,
      diagonalStretch: undefined,
      height: undefined,
      expanded: undefined,
      labelClass: undefined,
      shiftX: undefined,
      shiftY: undefined,
      selected: undefined,
      searchTerm,
      labelVisible: ref(undefined),
      nodeVisible: undefined,
      idFieldOpen: ref(false),
      newNodeID: ref(undefined)
    }
  },
  props: {
    nodeid: String
  },
  created: function () {
    if (this.nodes[this.nodeid].expanded === undefined) {
      this.nodes[this.nodeid].expanded = false
    }

    const reactiveNode = toRefs(this.nodes[this.nodeid])
    const reactiveLabel = toRefs(this.nodes[this.nodeid].label)

    this.newNodeID = reactiveNode.newNodeID
    this.nodeName = reactiveLabel.text
    this.expanded = reactiveNode.expanded
    this.labelClass = reactiveLabel.class
    this.labelVisible = reactiveNode.labelVisible
    this.nodeVisible = reactiveNode.nodeVisible
    this.selected = reactiveNode.selected

    this.locY = reactiveNode.locY
    this.locX = reactiveNode.locX

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
    this.shiftY = reactiveLabel.shiftY
  },
  methods: {
    toggleExpanded: function () {
      this.expanded = !this.expanded
    },
    openIdMenu: function () { this.idFieldOpen = true },
    toggleSelected: function () {
      if (this.selected) {
        this.selected = false
        this.selectedNodeIDs = this.selectedNodeIDs.filter(
          (v) => v !== this.nodeid
        )
      } else {
        this.selectedNodeIDs.push(this.nodeid)
        this.selected = true
      }
    },
    setLabelClass: function (cls) {
      this.labelClass = cls
    },
    deleteElement: function () {
      delete this.nodes[this.nodeid]
      this.selectedNodeIDs = this.selectedNodeIDs.filter(
        (e) => e !== this.nodeid
      )
    },
    duplicateElement: function () {
      this.nodes[this.nodeid + '_2'] = JSON.parse(
        JSON.stringify(this.nodes[this.nodeid])
      )
      this.selectedNodeIDs.push(this.nodeid + '_2')
    }
  },
  watch: {
    selectedNodeIDs: function (newVal) {
      if (newVal.length === 0) {
        this.selected = false
      }
    }
  },
  computed: {
    fitsSearchTerm: function () {
      return (
        !this.searchTerm ||
        this.nodeid.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
        this.nodes[this.nodeid]?.label?.text
          ?.toLowerCase()
          .includes(this.searchTerm.toLocaleLowerCase())
      )
    }
  }

}
</script>
