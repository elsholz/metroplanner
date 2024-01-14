<template>
  <div class="row q-my-sm justify-center text-h6 absolute-top">
    <div class="col col-grow q-px-sm">Kontext-Menü: Haltestellen</div>
    <div class="col col-shrink">
      <q-btn class="q-mr-md" icon="add" dense size="md" outline color="green" @click="createNode">
        <q-tooltip class="text-body1 no-wrap ">
          Neue Haltestelle
        </q-tooltip>
      </q-btn>
      <!--<q-btn icon="expand_less" dense size="md" class="q-mx-md" outline @click="collapseAll">
        <q-tooltip class="text-body1 no-wrap">Alles einklappen </q-tooltip>
      </q-btn>-->
      <q-btn icon="delete" dense size="md" outline color="red" class="q-mr-md" @click="deleteEverything">
        <q-tooltip class="text-body1 no-wrap ">Alles löschen </q-tooltip>
      </q-btn>
    </div>
    <!--<div class="text-h6">Auswahl bearbeiten</div>-->
    <div class="row items-center no-wrap q-pt-md q-px-sm">
      <div class="col col-2">
        <q-btn icon="layers_clear" dense @click.left="emptySelection" no-caps flat color="orange">
          Auswahl leeren
        </q-btn>
      </div>
      <div class="col col-2">
        <q-btn icon="content_copy" dense @click.left="duplicateSelection" flat no-caps>
          Duplizieren
        </q-btn>
      </div>
      <div class="col col-2">
        <q-btn icon="polyline" flat dense no-caps>
          Verbinden
          <q-menu> Test </q-menu>
        </q-btn>
      </div>
      <div class="col col-2">
        <q-btn icon="add" dense @click.left="addNodes" flat no-caps>
          Einfügen
        </q-btn>
      </div>
      <div class="col col-2">
        <q-btn icon="remove" dense @click.left="addNodes" flat no-caps>
          sonstiges
        </q-btn>
      </div>
      <div class="col col-grow"></div>
      <div class="col col-auto q-pa-sm">
        <q-btn icon="delete" no-caps color="red" round size="md" @click.left="openConfirmSelectionDeletionDialog"
          :disable="!this.selectedNodeIDs.length">
        </q-btn>
      </div>
      <q-dialog v-model="confirmDeletion">
        <q-card class="bg-negative text-white">
          <q-card-section class="row items-center">
            <q-avatar icon="delete" color="red" text-color="white" />
            <span class="q-ml-md text-body1">Löschen von</span>
            <span class="q-mx-sm text-bold text-h6 text-bold">{{ this.selectedNodeIDs.length }}</span>
            <span class="q-mr-sm text-body1">Haltestellen bestätigen?</span>
          </q-card-section>

          <q-card-actions align="center">
            <q-btn no-caps outline label="Abbrechen" color="gray" v-close-popup />
            <q-btn no-caps flat label="Haltestellen löschen" color="grey-13" @click="deleteSelection" v-close-popup />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>

    <div class="row items-center items-justify no-wrap q-mx-md q-pt-sm" style="width: 100%">
      <div class="col col-shrink q-mx-xs">
        <div class="text-body1">Filter:</div>
      </div>
      <div class="col col-4 q-mx-xs">
        <q-input debounce="250" v-model="searchTerm" dense clearable color="white" outlined>
        </q-input>
      </div>
      <div class="col col-grow bg-red">t</div>
      <div clas="col col-2">
        Button
      </div>
    </div>
    <hr dark />
    <!--
      <template v-for="x of this.selectedNodeIDs" :key="x">
        <NodeListItem :nodeid="x"> </NodeListItem>
      </template>-->
  </div>
  <q-scroll-area style="height: calc(100% - 200px); margin-top: 200px; border-right: 1px solid #ddd;">
    <q-list dark class="text-body1 text-white">
      <!----
      <q-item class="q-mx-sm">
        <q-item-section>
          <div class="row items-center no-wrap">
            <div class="col col-2">
              <div class="text-h6">Filter:</div>
            </div>
            <div class="col col-10">
              <q-input debounce v-model="searchTerm" dense clearable color="white" outlined>
              </q-input>
            </div>
          </div>
        </q-item-section>
      </q-item>
    -->

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
// import { toRefs } from 'vue'
import NodeListItem from './NodeListItem.vue'
import { ref } from 'vue'

const planEditorStore = usePlanEditorStore()

const { nodes, selectedNodeIDs, searchTerm, planState, lines } = storeToRefs(planEditorStore)

export default {
  setup () {
    return {
      nodes,
      selectedNodeIDs,
      lines,
      searchTerm,
      planState,
      confirmDeletion: ref(false)
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
    openConfirmSelectionDeletionDialog: async function (e, go) {
      e.preventDefault()
      this.confirmDeletion = true
    },
    deleteSelection () {
      planEditorStore.deleteNodes(this.selectedNodeIDs)
      this.selectedNodeIDs = []
    },
    emptySelection: function () {
      this.selectedNodeIDs = []
    },
    //     collapseAll: function () {
    //       for (const nodeid of this.nodes.keys()) {
    //         const reactiveNode = toRefs(this.nodes[nodeid])
    //         reactiveNode.expanded = false
    //       }
    //     },
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
    duplicateSelection: function () { }
  },
  components: { NodeListItem }
}
</script>
