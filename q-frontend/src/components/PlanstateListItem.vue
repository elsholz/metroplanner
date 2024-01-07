<template>
  <q-btn @click="openConfirmMakeCurrentDialog" flat no-caps :style="this.statsOnly ? 'cursor: default;' : ''">
    <q-item class="text-body1 q-my-sm" :style="'width: 100%; background-color: #003; border-radius: 10px;' +
      (isCurrentState ?  'border: 2px solid #0a0;' : confirmMakeCurrent ? 'border: 2px solid purple;' : '')
      ">
      <q-dialog v-model="confirmMakeCurrent">
        <q-card class="bg-primary text-white" dark bordered>
          <q-card-section class="row items-center">
            <q-avatar icon="update" color="success" text-color="white" />
            <span class="q-ml-md text-body1">Den markierten Zustand zum aktuellen machen?</span>
          </q-card-section>

          <q-card-actions align="center">
            <q-btn no-caps outline label="Abbrechen" color="warning" v-close-popup />
            <q-btn no-caps outline label="Bestätigen" color="green" v-close-popup @click="makeCurrent"/>
          </q-card-actions>
        </q-card>
      </q-dialog>
      <div class="row text-center justify-around items-center" style="width: 100%; min-height: 100px">
        <div class="col-sm-4 col-md-3 items-center text-left"
          style="display: block; overflow: hidden; text-overflow: ellipsis" v-if="this.createdAt">
          <div class="row q-ma-sm q-my-md">
            <q-icon name="today" size="sm" class="q-mx-sm">
              <q-tooltip anchor="top middle" self="bottom middle" class="text-body2">Erstellt am (Datum)</q-tooltip>
            </q-icon>{{ createdAt.split("T")[0] }}
          </div>
          <div class="row q-ma-sm q-my-md">
            <q-icon name="schedule" size="sm" class="q-mx-sm">
              <q-tooltip class="text-body2">
                Erstellt um (Uhrzeit)</q-tooltip> </q-icon>{{ createdAt.split("T")[1].split(".")[0] }}
          </div>
        </div>

        <div :class="(this.actionsEnabled && this.createdAt) ? 'col-xs-4 col-sm-5 items-center' : 'col-12 items-center'"
          style="display: block; overflow: hidden; text-overflow: ellipsis">
          <div class="row">
            <div class="column col-6">
              <div class="row q-my-sm justify-center">
                <q-icon name="clear_all" size="sm">
                  <q-tooltip anchor="top middle" self="bottom middle" class="text-body2">
                    Anzahl Linien
                  </q-tooltip>
                </q-icon>
                : {{ numberOfLines || 0 }}
              </div>

              <div class="row q-my-sm justify-center">
                <q-icon name="commit" size="sm">
                  <q-tooltip class="text-body2">
                    Anzahl Haltestellen
                  </q-tooltip> </q-icon>: {{ numberOfNodes || 0 }}
              </div>
            </div>

            <div class="column col-6">
              <div class="row q-my-sm justify-center">
                <q-icon name="polyline" size="sm">
                  <q-tooltip anchor="top middle" self="bottom middle" class="text-body2">
                    Anzahl Verbindungen
                  </q-tooltip> </q-icon>: {{ numberOfEdges || 0 }}
              </div>

              <div class="row q-my-sm justify-center">
                <q-icon name="text_fields" size="sm">
                  <q-tooltip class="text-body2">
                    Anzahl Beschriftungen
                  </q-tooltip> </q-icon>:
                {{ numberOfLabels || 0 }}
              </div>
            </div>
          </div>
        </div>

        <div class="col-xs-12 col-sm-12 col-md-4 " v-if="this.actionsEnabled">
          <q-btn no-caps class="bg-blue-10 q-py-sm q-mt-sm q-mx-sm" :to="'/edit/' + this.planId + '/' + this.planstateId">
            Von hier bearbeiten
          </q-btn>
          <ForkButton class="q-mt-sm q-mx-sm" :planid="this.planId" :planstateid="this.planstateId"></ForkButton>
        </div>
      </div>
    </q-item>
  </q-btn>
</template>

<script>
import { ref } from 'vue'
import ForkButton from './ForkButton.vue'
import { useQuasar } from 'quasar'
import { usePlanEditorStore } from 'src/stores/editor_store'

const planEditorStore = usePlanEditorStore()

export default {
  name: 'PlanstateListItem',
  setup: function () {
    return {
      $q: useQuasar(),
      confirmMakeCurrent: ref(false)
    }
  },
  props: {
    statsOnly: Boolean,
    planstateId: String,
    planId: String,
    numberOfEdges: Number,
    numberOfLines: Number,
    numberOfNodes: Number,
    numberOfLabels: Number,
    isCurrentState: Boolean,
    createdAt: {
      type: String,
      default: undefined
    },
    actionsEnabled: {
      type: Boolean,
      default: true
    }
    // colorthemeName: String
  },
  methods: {
    openConfirmMakeCurrentDialog: async function (e, go) {
      e.preventDefault()
      if (!this.statsOnly) {
        this.confirmMakeCurrent = true
      }
    },
    makeCurrent: async function () {
      planEditorStore.savePlanInfo(this.planId, {
        currentState: this.planstateId
      })
    }
  },
  components: { ForkButton }
}
</script>
