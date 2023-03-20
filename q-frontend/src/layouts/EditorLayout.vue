<template>
  <q-layout view="lHr lpR fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <!--<q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />-->

        <!--<HeaderLogo absoluteLeft="false" absoluteCenter="false"></HeaderLogo>
        -->
        <q-btn
          dark
          icon="keyboard_arrow_left"
          color="negative"
          no-caps
          :to="'./'"
        >
          zurück
        </q-btn>
        <q-toolbar-title
          ><span class="text-weight-thin">Plan bearbeiten: </span
          >{{ planName }}</q-toolbar-title
        >

        <div>
          <q-btn no-caps color="green" class="q-mr-sm" @click="save">
            speichern
          </q-btn>
          <q-btn no-caps color="indigo" @click="saveAndPublish">
            speichern & veröffentlichen
          </q-btn>
        </div>

        <!--<q-btn dense flat round icon="menu" @click="toggleRightDrawer" />-->
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" side="left" bordered dark :width="65">
      <div class="row q-my-md justify-center">Modus</div>
      <hr dark />
      <div class="row q-my-md justify-center">
        <q-btn
          flat
          class="q-py-md"
          @click="setEditorMode('viewer')"
          :color="editorMode === 'viewer' ? 'secondary' : ''"
        >
          <q-icon name="visibility" size="sm"></q-icon>
          <q-tooltip
            anchor="center right"
            self="center left"
            class="text-body2"
          >
            Viewer
          </q-tooltip>
        </q-btn>
      </div>
      <hr dark />
      <div class="row q-my-md justify-center">
        <q-btn
          class="q-py-md"
          @click="setEditorMode('lines')"
          :color="editorMode === 'lines' ? 'secondary' : 'teal-10'"
        >
          <q-icon name="clear_all" size="sm"></q-icon>
          <q-tooltip
            anchor="center right"
            self="center left"
            class="text-body2"
          >
            Linien
          </q-tooltip>
        </q-btn>
      </div>

      <div class="row q-my-md justify-center">
        <q-btn
          class="q-py-md"
          @click="setEditorMode('nodes')"
          :color="editorMode === 'nodes' ? 'secondary' : 'teal-10'"
        >
          <q-icon name="commit" size="sm"></q-icon>
          <q-tooltip
            anchor="center right"
            self="center left"
            class="text-body2"
          >
            Haltestellen
          </q-tooltip>
        </q-btn>
      </div>

      <!--<div class="row q-my-md justify-center">
          <q-btn class="q-py-md" @click="setEditorMode('connections')" :color="editorMode === 'connections' ? 'secondary': 'primary'">
            <q-icon name="polyline" size="sm"></q-icon>
            <q-tooltip
              anchor="center right"
              self="center left"
              class="text-body2"
            >
              Verbindungen
            </q-tooltip>
          </q-btn>
        </div>-->

      <div class="row q-my-md justify-center">
        <q-btn
          class="q-py-md"
          @click="setEditorMode('labels')"
          :color="editorMode === 'labels' ? 'secondary' : 'teal-10'"
        >
          <q-icon name="text_fields" size="sm"></q-icon>
          <q-tooltip
            anchor="center right"
            self="center left"
            class="text-body2"
          >
            Beschriftungen
          </q-tooltip>
        </q-btn>
      </div>

      <q-page-sticky position="bottom-right" :offset="[3, 3]">
        <q-fab
          color="purple"
          class="q-btn-fab-mini"
          mini
          icon="keyboard_arrow_up"
          direction="up"
        >
          <q-fab-action
            color="indigo-10"
            @click="onClick"
            icon="palette"
            disable
          >
            <q-tooltip
              anchor="center right"
              self="center left"
              class="text-body2"
            >
              Farbschema ändern
            </q-tooltip>
          </q-fab-action>
        </q-fab>
      </q-page-sticky>
    </q-drawer>

    <q-drawer
      v-model="rightDrawerOpen"
      side="right"
      bordered
      dark
      :width="$q.screen.gt.sm ? 500 : 350"
    >
      <div class="row q-my-sm justify-center text-h6">
        Kontext-Menü:
        {{
          { lines: "Linien", nodes: "Haltestellen", labels: "Beschriftungen" }[
            this.editorMode
          ]
        }}
      </div>
      <hr dark />
      Test:
      {{ lines }}
    </q-drawer>
    <PlanEditor></PlanEditor>
  </q-layout>
</template>

<script>
// import HeaderLogo from 'src/components/HeaderLogo.vue'
// import PlanEditor from 'src/pages/PlanStateEditor.vue'
import { useAuth0 } from '@auth0/auth0-vue'
import { usePlanEditorStore } from 'src/stores/editor_store'
import { useUserStore } from 'src/stores/user_store'
import { ref } from 'vue'

export default {
  setup () {
    const leftDrawerOpen = ref(true)
    const rightDrawerOpen = ref(false)
    const leftDrawerMini = ref(false)
    const saving = ref(false)
    const lines = ref({})
    const editorMode = ref('viewer')
    const planName = 'Liniennetzplan Wesel'

    return {
      planName,
      leftDrawerOpen,
      leftDrawerMini,
      toggleLeftDrawer () {
        leftDrawerMini.value = !leftDrawerMini.value
      },
      rightDrawerOpen,
      toggleRightDrawer () {
        rightDrawerOpen.value = !rightDrawerOpen.value
      },
      openRightDrawer () {
        rightDrawerOpen.value = true
      },
      closeRightDrawer () {
        rightDrawerOpen.value = false
      },
      setEditorMode (newVal) {
        editorMode.value = newVal
        rightDrawerOpen.value = !(newVal === 'viewer')
      },
      planEditorStore: usePlanEditorStore(),
      userStore: useUserStore(),
      editorMode,
      lines,
      saving
    }
  },
  methods: {
    save: async function (publish) {
      this.saving = true
      publish = publish ?? false

      this.saving = false
    },
    saveAndPublish: async function () {
      await this.save(true)
    }
  },
  mounted: async function () {
    this.planId = this.$route.params.planid
    this.planstateId = this.$route.params.planstateid

    const { user, isAuthenticated, getAccessTokenSilently } = useAuth0()
    await this.userStore.init(user, isAuthenticated, getAccessTokenSilently)

    await this.planEditorStore.loadPlanDetails(this.planId)
    await this.planEditorStore.loadPlanState(this.planstateId)

    console.log(
      'Planstate loaded:',
      this.planEditorStore.planStates[this.planstateId]
    )
    this.lines = this.planEditorStore.planStates[this.planstateId].lines
  }

  // components: { PlanEditor }
}
</script>
