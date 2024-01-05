<template>
  <q-layout view="lHr LpR fFf">
    <template v-if="this.loaded">
      <q-header elevated class="bg-primary text-white">
        <q-toolbar>
          <q-btn dark icon="keyboard_arrow_left" color="negative" no-caps to="./">
            zurück
          </q-btn>
          <q-toolbar-title><span class="text-weight-thin">Plan bearbeiten: </span>{{ planDetails.planName
          }}</q-toolbar-title>

          <div>
            <q-btn no-caps color="green" class="q-mr-sm" @click="save" :disable="disable_save_button">
              speichern
            </q-btn>
            <q-btn no-caps color="indigo" @click="saveAndPublish" :disable="disable_publish_button">
              {{ (saved && !published) ? "veröffentlichen" : "speichern & veröffentlichen" }}
            </q-btn>
          </div>
        </q-toolbar>
      </q-header>

      <q-drawer v-model="leftDrawerOpen" side="left" bordered dark :width="65" class="column justify-between no-wrap"
        :behavior="'desktop'" no-swipe-backdrop :breakpoint="0" style="overflow: hidden;">
        <div>

          <div class="row q-my-md justify-center">Modus</div>
          <hr dark />
          <div class="row q-my-sm justify-center">
            <q-btn flat class="q-py-md" @click="setEditorMode('viewer')"
              :color="editorMode === 'viewer' ? 'secondary' : ''">
              <q-icon name="visibility" size="sm"></q-icon>
              <q-tooltip anchor="center right" self="center left" class="text-body2">
                Viewer
              </q-tooltip>
            </q-btn>
          </div>
          <div class="row q-my-sm justify-center">
            <q-btn flat class="q-py-md" @click="setEditorMode('settings')"
              :color="editorMode === 'settings' ? 'secondary' : ''">
              <q-icon name="settings" size="sm"></q-icon>
              <q-tooltip anchor="center right" self="center left" class="text-body2">
                Einstellungen
              </q-tooltip>
            </q-btn>
          </div>

          <hr dark />
          <div class="row q-my-md justify-center">
            <q-btn class="q-py-md" @click="setEditorMode('lines')"
              :color="editorMode === 'lines' ? 'secondary' : 'teal-10'">
              <q-icon name="clear_all" size="sm"></q-icon>
              <q-tooltip anchor="center right" self="center left" class="text-body2">
                Linien
              </q-tooltip>
            </q-btn>
          </div>

          <div class="row q-my-md justify-center">
            <q-btn class="q-py-md" @click="setEditorMode('nodes')"
              :color="editorMode === 'nodes' ? 'secondary' : 'teal-10'">
              <q-icon name="commit" size="sm"></q-icon>
              <q-tooltip anchor="center right" self="center left" class="text-body2">
                Haltestellen
              </q-tooltip>
            </q-btn>
          </div>

          <div class="row q-my-md justify-center">
            <q-btn class="q-py-md" @click="setEditorMode('labels')"
              :color="editorMode === 'labels' ? 'secondary' : 'teal-10'">
              <q-icon name="text_fields" size="sm"></q-icon>
              <q-tooltip anchor="center right" self="center left" class="text-body2">
                Beschriftungen
              </q-tooltip>
            </q-btn>
          </div>
        </div>
        <div class="row items-center justify-center q-my-sm">
          <q-btn round size="md" icon="question_mark" color="accent">
            <q-menu>
              <q-card>
                <q-card-section class="bg-purple-9 text-white">
                  <div class="text-body1">Tastenkombinationen:</div>
                </q-card-section>

                <q-markup-table>
                  <tbody>
                    <tr>
                      <td class="text-right">Linksklick:</td>
                      <td class="text-center">Einzelne Haltestelle auswählen oder Auswahl aufheben</td>
                    </tr>
                    <tr>
                      <td class="text-right">Strg + Linksklick:</td>
                      <td class="text-center">Haltestelle zur Auswahl hinzufügen oder von Auswahl entfernen</td>
                    </tr>
                    <tr>
                      <td class="text-right">Shift + Linksklick:</td>
                      <td class="text-center">Auswahl um alle Haltestellen auf kürzestem Pfad von zuletzt<br>ausgewählter
                        Haltestelle erweitern</td>
                    </tr>
                    <tr>
                      <td class="text-right">Strg + Shift + Linksklick:</td>
                      <td class="text-center">Alle Haltestellen auf dem kürzesten Pfad von zuletzt
                        ausgewählter<br>Haltestelle von Auswahl entfernen</td>
                    </tr>
                  </tbody>
                </q-markup-table>
              </q-card>
              <q-card class="column col col-grow">
                <q-card-section class="bg-green-9 text-white">
                  <div class="text-body1">Hilfe & Dokumentation:</div>
                </q-card-section>
                <div class="row justify-center q-my-sm">
                  <q-btn push  outline color="blue-2" no-caps icon="description">
                    Schnelleinstieg
                  </q-btn>
                  <q-btn push class="q-mx-sm"  outline color="blue-2" no-caps icon="play_arrow">
                    Video-Tutorial
                  </q-btn>
                  <q-btn push outline color="blue-2" no-caps icon="email">
                    Support
                  </q-btn>
                </div>
              </q-card>
            </q-menu>
          </q-btn>
        </div>
      </q-drawer>

      <q-page-container>
        <EditorCanvas ref="canvas" :store="this.planEditorStore" :planstateid="this.planstateId"
          :editorMode="this.editorMode">
        </EditorCanvas>
      </q-page-container>

      <q-drawer v-model="contextMenuOpen" side="right" bordered dark :width="500" no-swipe-open no-swipe-close
        no-swipe-backdrop :breakpoint="0">
        <keep-alive>
          <component :is="this.contextMenu"></component>
        </keep-alive>
      </q-drawer>

    </template>
    <template v-else>
      <q-inner-loading :showing="true" label="Planeditor wird geladen..." label-class="text-white" class="bg-primary"
        style="border: 3px solid #fff5; border-radius: 10px" label-style="font-size: 2.0em" color="white" size="5em" />
    </template>
  </q-layout>
</template>

<script>
// import HeaderLogo from 'src/components/HeaderLogo.vue'
// import PlanEditor from 'src/pages/PlanStateEditor.vue'
import { useAuth0 } from '@auth0/auth0-vue'
import { usePlanEditorStore } from 'src/stores/editor_store'
import { useUserStore } from 'src/stores/user_store'
import EditorCanvas from 'src/pages/EditorCanvas.vue'
import { ref } from 'vue'
import ContextMenuLines from 'src/components/ContextMenuLines.vue'
import ContextMenuLabels from 'src/components/ContextMenuLabels.vue'
import ContextMenuNodes from 'src/components/ContextMenuNodes.vue'
import ContextMenuSettings from 'src/components/ContextMenuSettings.vue'
import { storeToRefs } from 'pinia'

export default {
  setup () {
    const planEditorStore = usePlanEditorStore()
    const { contextMenuOpen, planDetails, editorMode } = storeToRefs(planEditorStore)
    const leftDrawerOpen = true
    const leftDrawerMini = false
    const saving = ref(false)
    const saved = ref(false)
    const published = ref(false)
    const changed = ref(false)
    const loaded = ref(false)
    const planstate = ref(undefined)

    return {
      planDetails,
      leftDrawerOpen,
      leftDrawerMini,
      contextMenuOpen,

      planEditorStore: usePlanEditorStore(),
      userStore: useUserStore(),
      editorMode,
      // lines,
      // nodes,
      saving,
      saved,
      published,
      changed,
      loaded,
      planstate
    }
  },
  computed: {
    contextMenu: function () {
      return {
        lines: 'ContextMenuLines',
        nodes: 'ContextMenuNodes',
        labels: 'ContextMenuLabels',
        settings: 'ContextMenuSettings'
      }[this.editorMode]
    },
    disable_save_button: function () {
      return false // return this.saved || !this.changed || this.saving
    },
    disable_publish_button: function () {
      return false // return this.published || !this.changed || this.saving
    }
  },
  methods: {
    save: async function (publish) {
      this.saving = true
      publish = publish ?? false

      this.saving = false

      await this.planEditorStore.savePlanState(publish)

      this.changed = false
    },
    saveAndPublish: async function () {
      await this.save(true)
    },
    toggleLeftDrawer () {
      this.leftDrawerMini = !this.leftDrawerMini
    },
    setEditorMode (newVal) {
      this.editorMode = newVal
      // const oldVal = this.contextMenuOpen
      this.contextMenuOpen = !(newVal === 'viewer')

      // if (this.contextMenuOpen && !oldVal) {
      //   // TODO: Scroll container 500px to the right, if already scrolled to the right.
      //   // this.$refs.canvas.
      // }
    }
  },
  mounted: async function () {
    this.planId = this.$route.params.planid
    this.planstateId = this.$route.params.planstateid

    const { user, isAuthenticated, getAccessTokenSilently } = useAuth0()
    await this.userStore.init(user, isAuthenticated, getAccessTokenSilently)

    await this.planEditorStore.loadPlanDetails(this.planId)
    await this.planEditorStore.loadPlanState(this.planId, this.planstateId)

    this.loaded = true

    console.log('Planstate loaded:', this.planEditorStore.planState)
    this.planstate = this.planEditorStore.planState
  },

  components: {
    EditorCanvas,
    ContextMenuLabels,
    ContextMenuLines,
    ContextMenuNodes,
    ContextMenuSettings
  }
}
</script>
