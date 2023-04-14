<template>
  <div class="row q-my-sm justify-center text-h6 absolute-top">
    <div class="col col-grow q-px-sm">Kontext-Menü: Haltestellen</div>
    <div class="col col-shrink">
      <q-btn
        icon="add"
        dense
        size="md"
        outline
        color="green"
        @click="createNode"
      >
        <q-tooltip class="text-body1 no-wrap ">
          Neue Haltestelle
        </q-tooltip>
      </q-btn>
      <q-btn
        icon="expand_less"
        dense
        size="md"
        class="q-mx-md"
        outline
        @click="collapseAll"
      >
        <q-tooltip class="text-body1 no-wrap">Alles einklappen </q-tooltip>
      </q-btn>
      <q-btn
        icon="delete"
        dense
        size="md"
        outline
        color="red"
        class="q-mr-md"
        @click="deleteEverything"
      >
        <q-tooltip class="text-body1 no-wrap ">Alles löschen </q-tooltip>
      </q-btn>
    </div>
    <template v-if="this.selectedNodeIDs.length">
      <div class="text-h6">Auswahl bearbeiten</div>
      <div class="row items-center no-wrap">
        <div class="col col-3">
          <q-btn
            icon="layers_clear"
            @click.left="emptySelection"
            no-caps
            color="orange"
            >Auswahl leeren</q-btn
          >
        </div>
        <div class="col col-3">
          <q-btn icon="content_copy" @click.left="duplicateSelection" no-caps
            >Duplizieren</q-btn
          >
        </div>
        <div class="col col-3">
          <q-btn icon="polyline" no-caps
            >Verbinden
            <q-menu> Test </q-menu>
          </q-btn>
        </div>
        <div class="col col-grow"></div>
        <div class="col col-2">
          <q-btn
            icon="delete"
            no-caps
            color="red"
            round
            size="md"
            @click.left="deleteSelection"
          >
          </q-btn>
        </div>
      </div>
      <!--
      <template v-for="x of this.selectedNodeIDs" :key="x">
        <NodeListItem :nodeid="x"> </NodeListItem>
      </template>-->
    </template>
  </div>
  <q-scroll-area
    :style="`
      height: calc(100% - 150px);
      margin-top: 150px;
      border-right: 1px solid #ddd;
    `"
  >
    <q-list dark class="text-body1 text-white">
      <q-item class="q-mx-sm">
        <q-item-section>
          <div class="row items-center no-wrap">
            <div class="col col-2">
              <div class="text-h6">Filter:</div>
            </div>
            <div class="col col-10">
              <q-input
                v-model="searchTerm"
                dense
                clearable
                color="white"
                outlined
              >
              </q-input>
            </div>
          </div>
        </q-item-section>
      </q-item>

      <!--
    <hr
      dark
      v-if="this.selectedNodeIDs.length && this.unselectedNodeIDs.length"
      class="q-my-md q-mb-xl"
    />
    <template v-for="x of this.unselectedNodeIDs" :key="x">
      <NodeListItem :nodeid="x" v-if="fitsSearchTerm(x)"> </NodeListItem>
    </template>
  -->
      <template v-for="x of Object.keys(this.nodes)" :key="x">
        <NodeListItem :nodeid="x"> </NodeListItem>
      </template>
    </q-list>
  </q-scroll-area>
</template>

<script>
import { usePlanEditorStore } from 'src/stores/editor_store'
import { storeToRefs } from 'pinia'
import NodeListItem from './NodeListItem.vue'

const planEditorStore = usePlanEditorStore()

const { nodes, selectedNodeIDs, searchTerm, planState } = storeToRefs(planEditorStore)

export default {
  setup () {
    return {
      nodes,
      selectedNodeIDs,
      searchTerm,
      planState
    }
  },
  computed: {
    unselectedNodeIDs: function () {
      const res = []
      for (const node of Object.keys(nodes.value)) {
        if (!this.selectedNodeIDs.includes(node)) {
          res.push(node)
        }
      }
      return res
    }
  },
  methods: {
    deleteSelection () {
      if (
        window.confirm(
          `Sicher, dass die ${this.selectedNodeIDs.length} ausgewählten Haltestellen gelöscht werden sollen?`
        )
      ) {
        for (const nodeid of this.selectedNodeIDs) {
          delete this.nodes[nodeid]
        }
        this.selectedNodeIDs = []
      }
    },
    emptySelection: function () {
      this.selectedNodeIDs = []
    },
    deleteEverything: function () {
      if (
        window.confirm(
          `Sicher, dass alle ${Object.keys(this.nodes).length} Haltestellen gelöscht werden sollen?`
        )
      ) {
        this.nodes = {}
        this.planState.nodes = {}
      }
    },
    duplicateSelection: function () {}
  },
  components: { NodeListItem }
}
</script>
