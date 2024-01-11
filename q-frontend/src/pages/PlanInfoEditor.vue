<template>
  <q-page class="doc-container flex justify-center bg-primary q-pb-xl text-white" dark>
    <div v-if="this.planDetailsLoaded && !this.saving" class="row justify-center" style="width: 100%">
      <div class="row justify-left" style="width: 100%">
        <q-btn dark icon="keyboard_arrow_left" class="q-ma-md" color="negative" no-caps to="/profile">
          zurück
        </q-btn>
      </div>
      <div class="column col-12 q-px-sm">
        <div class="row q-mb-md">
          <div class="column items-center justify-center col-12 text-white">
            <div class="text-h4 text-center q-mt-lg">Plandetails</div>
            <hr color="white" width="200px;" />
          </div>
        </div>
        <div class="row items-center justify-center">
          <div class="column col-xs-11 col-sm-9 col-md-5">
            <div class="column col-6 text-h6">Planname:</div>
            <div class="column col-6 text-white">
              <div class="q-my-sm">
                <q-input :oninput="changePlanInfo" dark color="white" outlined v-model="planName" input-class="text-h5"
                  input-style="text-align: center" :rules="[
                    (val) => val.length <= 50 || 'Maximal 50 Zeichen erlaubt',
                  ]" />
              </div>
            </div>
          </div>
        </div>
        <div class="row items-center justify-center">
          <div class="column col-xs-12 col-sm-10 col-md-6">
            <div class="column col-6 text-h6">Planbeschreibung:</div>
            <div class="column col-6 text-white">
              <div class="q-my-sm">
                <q-input :oninput="changePlanInfo" dark color="white" outlined v-model="planDescription" autogrow
                  input-class="text-body1" input-style="text-align: left" :rules="[
                    (val) => val.length <= 250 || 'Maximal 250 Zeichen erlaubt',
                  ]" />
              </div>
            </div>
          </div>
        </div>
        <div class="row items-center justify-center text-body1" v-if="planInfoChanged">
          <div class="column col-xs-6 col-sm-4 text-white items-center text-center">
            <q-btn dark no-caps color="positive" v-if="planInfoChanged" animate @click="savePlanInfo">
              <div class="text-white text-body1">Änderungen speichern</div>
            </q-btn>
          </div>
        </div>

        <div class="row items-center justify-center text-body1">
          <div class="column col-xs-6 col-sm-4 text-white items-center text-center">
            <q-icon name="clear_all" size="md" />
            Linien: {{ currentNumberOfLines || 0 }}
          </div>
          <div class="column col-xs-6 col-sm-4 text-white items-center text-center">
            <q-icon name="commit" size="md" />
            Haltestellen: {{ currentNumberOfNodes || 0 }}
          </div>
        </div>

        <div class="row items-center justify-center text-body1">
          <div class="column col-xs-6 col-sm-4 text-white items-center text-center">
            <q-icon name="polyline" size="md" />
            Verbindungen: {{ currentNumberOfEdges || 0 }}
          </div>
          <div class="column col-xs-6 col-sm-4 text-white items-center text-center no-wrap">
            <q-icon name="text_fields" size="md" />
            Beschriftungen: {{ currentNumberOfLabels || 0 }}
          </div>
        </div>

        <div class="row items-center justify-center text-body1">
          <div class="column col-12 text-white items-center text-center q-mt-lg q-mb-sm">
            <div class="q-mb-xs">Erstellt:</div>
            <div>
              <q-icon name="today" size="md" class="q-mx-sm q-my-sm" />{{
                createdAt?.split("T")[0]
              }}
              <q-icon name="schedule" size="md" class="q-mx-sm q-my-sm" />{{
                createdAt?.split("T")[1]?.split('.')[0]
              }}
            </div>
          </div>
          <div class="column col-12 text-white items-center text-center q-mb-xl">
            <div class="q-mb-xs">Zuletzt bearbeitet:</div>
            <div>
              <q-icon name="today" size="md" class="q-mx-sm q-my-sm" />{{
                lastModifiedAt?.split("T")[0]
              }}
              <q-icon name="schedule" size="md" class="q-mx-sm q-my-sm" />{{
                lastModifiedAt?.split("T")[1]?.split('.')[0]
              }}
            </div>
          </div>
        </div>

        <div class="row q-mb-xl">
          <div class="column col-12 text-white">
            <div class="row justify-center" style="width: 100%">
              <div class="text-h4">Links</div>
            </div>
            <div class="row justify-center" style="width: 100%">
              <hr color="white" width="200px;" />
            </div>

            <div v-for="link in this.shortlinks" :key="link" class="row justify-center q-mt-md">
              <q-btn flat no-caps rounded class="bg-grey-9" :to="'/p/' + link.shortlink">
                <div class="text-body1 text-mono">
                  {{ this.windowOrigin }}/p/{{ link.shortlink }}
                </div>
              </q-btn>
            </div>
          </div>
        </div>

        <div class="row q-mb-xl">
          <div class="column col-12 text-white">
            <div class="row justify-center" style="width: 100%">
              <div class="text-h4">Statistik</div>
            </div>
            <div class="row justify-center" style="width: 100%">
              <hr color="white" width="200px;" />
            </div>
            <div class="row justify-center" style="width: 100%">
              <div class="text-h6">
                Gesamtzahl Aufrufe: {{ this.totalViewCount }}
              </div>
            </div>

            <div class="q-my-md" style="border: 2px solid #333; border-radius: 10px" v-if="views">
              <q-tabs v-model="tab" dense class="text-white" active-color="secondary" indicator-color="secondary"
                align="justify" narrow-indicator>
                <q-tab name="hours" dark label="Stunde" />
                <q-tab name="days" label="Tag" />
                <q-tab name="months" label="Monat" />
                <q-tab name="years" label="Jahr" />
              </q-tabs>

              <q-separator />

              <q-tab-panels v-model="tab" animated class="bg-primary">
                <q-tab-panel dark name="years">
                  <div class="text-h6">Aufrufe pro Jahr</div>
                  <ChartComponent :views="this.views.yearly" :labels="true"></ChartComponent>
                </q-tab-panel>

                <q-tab-panel dark name="months">
                  <div class="text-h6">Aufrufe pro Monat</div> <!-- 12 or 36 -->
                  <ChartComponent :views="this.views.monthly" :labels="true"></ChartComponent>
                </q-tab-panel>

                <q-tab-panel dark name="days">
                  <div class="text-h6">Aufrufe pro Tag</div> <!-- 32 -->
                  <ChartComponent :views="this.views.daily" :labels="true"></ChartComponent>
                </q-tab-panel>

                <q-tab-panel name="hours">
                  <div class="text-h6">Aufrufe pro Stunde</div> <!-- 24 -->
                  <ChartComponent :views="this.views.hourly" :labels="false"></ChartComponent>
                </q-tab-panel>
              </q-tab-panels>
            </div>
          </div>
        </div>

        <div class="row justify-center">
          <div class="column col-12 col-md-10 col-lg-8 text-white">
            <div class="row justify-center" style="width: 100%">
              <div class="text-h4">Historie</div>
            </div>
            <div class="row justify-center" style="width: 100%">
              <hr color="white" width="200px;" />
            </div>
            <div class="row justify-center" style="width: 100%">
              <q-list padding separator class="text-white" style="width: 100%" v-if="planstates">
                <PlanstateListItem v-for="planstate of planstates.slice().reverse()" :key="planstate"
                  :planId="this.planId" :planstateId="planstate.planstateId" :numberOfEdges="planstate.numberOfEdges"
                  :numberOfNodes="planstate.numberOfNodes" :numberOfLines="planstate.numberOfLines"
                  :numberOfLabels="planstate.numberOfLabels" :isCurrentState="planstate.planstateId === currentState"
                  :createdAt="planstate.createdAt" style="width: 100%">
                </PlanstateListItem>
              </q-list>
              <div v-else>
                Es liegen noch keine Plandaten in der Historie vor.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else-if="this.saving">
      <q-inner-loading :showing="true" label="Daten werden gespeichert…" label-class="text-green" class="bg-dark"
        label-style="font-size: 1.5em" color="white" size="7em" />
    </div>
    <div v-else>
      <q-inner-loading :showing="true" :label="planName || 'Planübersicht wird geladen'" label-class="text-white"
        class="bg-dark" label-style="font-size: 1.5em" color="white" size="7em" />
    </div>
  </q-page>
</template>

<style>
hr {
  width: 20%;
}
</style>

<script>
import ChartComponent from 'src/components/ChartComponent.vue'
import PlanstateListItem from 'src/components/PlanstateListItem.vue'
import { usePlanEditorStore } from 'src/stores/editor_store'
import { ref } from 'vue'

const planEditorStore = usePlanEditorStore()

export default {
  name: 'PlanInfoEditor',
  setup () {
    return {
      planId: ref(undefined),
      planName: ref(undefined),
      planDescription: ref(undefined),

      currentState: ref(undefined),
      currentNumberOfNodes: ref(undefined),
      currentNumberOfLines: ref(undefined),
      currentNumberOfLabels: ref(undefined),
      currentNumberOfEdges: ref(undefined),

      totalViewCount: ref(undefined),
      lastModifiedAt: ref(undefined),

      shortlinks: ref(undefined),

      windowOrigin: window.location.origin,
      planInfoChanged: ref(false),
      saving: ref(false),
      tab: ref('days'),

      planstates: ref([]),
      planEditorStore,
      planDetailsLoaded: ref(false)
    }
  },
  methods: {
    changePlanInfo: function () {
      this.planInfoChanged = true
    },
    savePlanInfo: async function (event) {
      console.log(this.planName, this.planDescription)
      console.log('button press to save plan info', event)
      this.planEditorStore.savePlanInfo(this.planId, {
        planDescription: this.planDescription,
        planName: this.planName
      })
    }
  },
  created: async function () {
    this.planId = this.$route.params.planid

    await this.planEditorStore.loadPlanDetails(this.planId)
    const planDetails = this.planEditorStore.planDetails

    this.currentNumberOfNodes = planDetails.currentNumberOfNodes
    this.currentNumberOfLines = planDetails.currentNumberOfLines
    this.currentNumberOfLabels = planDetails.currentNumberOfLabels
    this.currentNumberOfEdges = planDetails.currentNumberOfEdges
    this.lastModifiedAt = planDetails.lastModifiedAt
    this.createdAt = planDetails.createdAt
    this.planName = planDetails.planName
    this.planDescription = planDetails.planDescription
    this.currentState = planDetails.currentState
    this.planstates = planDetails.history
    this.shortlinks = planDetails.shortlinks
    this.shortlinks[0].active = true
    const views = planDetails.shortlinks[0]?.stats?.views
    this.totalViewCount = planDetails.shortlinks[0]?.stats?.totalCount ?? 0

    const viewsDaily = {}
    const viewsHourly = {}

    for (const [datehour, count] of Object.entries(views)) {
      // const [d, t] = datehour.split('T')
      const [d, hour] = datehour.split('T')
      const [year, month, day] = d.split('-')
      const dayTimestamp = new Date(
        parseInt(year),
        parseInt(month) - 1,
        parseInt(day)
      ).getTime()
      const hourTimestamp = new Date(
        parseInt(year),
        parseInt(month) - 1,
        parseInt(day),
        parseInt(hour)
      ).getTime()

      if (!viewsDaily[dayTimestamp]) {
        viewsDaily[dayTimestamp] = 0
      }
      viewsDaily[dayTimestamp] += count
      viewsHourly[hourTimestamp] = count
    }

    this.views = Object.keys(viewsDaily).length ? {
      daily: [],
      hourly: []
    }
      : undefined

    for (const [timestamp, count] of Object.entries(viewsDaily).slice(-31)) {
      this.views.daily.push([parseInt(timestamp), count])
    }
    for (const [timestamp, count] of Object.entries(viewsHourly).slice(-24)) {
      this.views.hourly.push([parseInt(timestamp), count])
    }
    console.log('Views:', this.views)
    this.planDetailsLoaded = true
  },
  components: { PlanstateListItem, ChartComponent }
}
</script>
