<template>
  <q-page
    class="doc-container flex justify-center bg-primary q-pb-xl text-white"
    dark
  >
    <div
      v-if="this.planDetailsLoaded && !this.saving"
      class="row justify-center"
      style="width: 100%"
    >
      <div class="column col-xs-12 col-sm-10 col-md-8 q-px-sm">
        <div class="row q-my-lg">
          <div class="column items-center justify-center col-12 text-white">
            <div class="text-h4 text-center q-mt-lg">Plandetails</div>
            <hr color="white" width="200px;" />
          </div>
        </div>
        <div class="row items-center justify-center">
          <div class="column col-xs-12 col-sm-10 col-md-6">
            <div class="column col-6 text-h6">Planname:</div>
            <div class="column col-6 text-white">
              <div class="q-my-sm">
                <q-input
                  :oninput="changePlanInfo"
                  dark
                  color="white"
                  outlined
                  v-model="planName"
                  input-class="text-h6"
                  input-style="text-align: center"
                  :rules="[
                    (val) => val.length <= 30 || 'Maximal 30 Zeichen erlaubt',
                  ]"
                />
              </div>
            </div>
          </div>
        </div>
        <div class="row items-center justify-center">
          <div class="column col-xs-12 col-sm-10 col-md-6">
            <div class="column col-6 text-h6">Planbeschreibung:</div>
            <div class="column col-6 text-white">
              <div class="q-my-sm">
                <q-input
                  :oninput="changePlanInfo"
                  dark
                  color="white"
                  outlined
                  v-model="planDescription"
                  autogrow
                  input-class="text-body1"
                  input-style="text-align: left"
                  :rules="[
                    (val) => val.length <= 250 || 'Maximal 250 Zeichen erlaubt',
                  ]"
                />
              </div>
            </div>
          </div>
        </div>
        <div
          class="row items-center justify-center text-body1"
          v-if="planInfoChanged"
        >
          <div
            class="column col-xs-6 col-sm-4 text-white items-center text-center"
          >
            <q-btn
              dark
              color="green"
              v-if="planInfoChanged"
              animate
              @click="savePlanInfo"
            >
              <div class="text-white text-body1">Änderungen speichern</div>
            </q-btn>
          </div>
        </div>

        <div class="row items-center justify-center text-body1">
          <div
            class="column col-xs-6 col-sm-4 text-white items-center text-center"
          >
            <q-icon name="clear_all" size="md" />
            Linien: {{ currentNumberOfLines || 0 }}
          </div>
          <div
            class="column col-xs-6 col-sm-4 text-white items-center text-center"
          >
            <q-icon name="commit" size="md" />
            Haltestellen: {{ currentNumberOfNodes || 0 }}
          </div>
        </div>

        <div class="row items-center justify-center text-body1">
          <div
            class="column col-xs-6 col-sm-4 text-white items-center text-center"
          >
            <q-icon name="polyline" size="md" />
            Verbindungen: {{ currentNumberOfEdges || 0 }}
          </div>
          <div
            class="column col-xs-6 col-sm-4 text-white items-center text-center no-wrap"
          >
            <q-icon name="text_fields" size="md" />
            Beschriftungen: {{ currentNumberOfLabels || 0 }}
          </div>
        </div>

        <div class="row items-center justify-center text-body1">
          <div
            class="column col-12 text-white items-center text-center q-mt-lg q-mb-xl"
          >
            <div class="q-mb-xs">Zuletzt bearbeitet:</div>
            <div>
              <q-icon name="today" size="md" class="q-mx-sm q-my-sm" />{{
                lastModifiedAt?.split(" ")[0]
              }}
              <q-icon name="schedule" size="md" class="q-mx-sm q-my-sm" />{{
                lastModifiedAt?.split(" ")[1]
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

            <div
              v-for="link in this.shortlinks"
              :key="link"
              class="row justify-center"
            >
              <q-btn flat no-caps :to="'/p/' + link._id">
                <div class="text-h6" style="font-family: monospace">
                  <span class="text-weight-thin"
                    >{{ this.windowOrigin }}/p/</span
                  ><span class="text-bold" style="text-decoration: underline">{{
                    link._id
                  }}</span>
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

            <div class="q-my-md"
                style="border: 2px solid #333; border-radius: 10px;"
            >
              <q-tabs
                v-model="tab"
                dense
                class="text-white"
                active-color="secondary"
                indicator-color="secondary"
                align="justify"
                narrow-indicator
              >
                <q-tab name="days" label="Aufrufe pro Tag" />
                <q-tab name="hours" dark label="Aufrufe pro Stunde" />
              </q-tabs>

              <q-separator />

              <q-tab-panels v-model="tab" animated class="bg-primary">
                <q-tab-panel dark name="days">
                  <div class="text-h6">Aufrufe pro Tag</div>
                  <ChartComponent :views="this.views.daily" :labels="true"></ChartComponent>
                </q-tab-panel>

                <q-tab-panel name="hours">
                  <div class="text-h6">Aufrufe pro Stunde</div>
                  <ChartComponent :views="this.views.hourly" :labels="false"></ChartComponent>
                </q-tab-panel>
              </q-tab-panels>
            </div>
          </div>
        </div>

        <div class="row">
          <div class="column col-12 text-white">
            <div class="row justify-center" style="width: 100%">
              <div class="text-h4">Historie</div>
            </div>
            <div class="row justify-center" style="width: 100%">
              <hr color="white" width="200px;" />
            </div>
            <div class="row justify-center" style="width: 100%">
              <q-list
                padding
                separator
                class="text-white"
                style="width: 100%"
                v-if="planstates"
              >
                <PlanstateListItem
                  v-for="planstate of planstates.slice().reverse()"
                  :key="planstate"
                  :planId="this.planId"
                  :planstateId="planstate.planstateid"
                  :numberOfEdges="planstate.numberOfEdges"
                  :numberOfNodes="planstate.numberOfNodes"
                  :numberOfLines="planstate.numberOfLines"
                  :numberOfLabels="planstate.numberOfLabels"
                  :isCurrentState="planstate.planstateid === currentState"
                  :createdAt="planstate.createdAt"
                  style="width: 100%"
                >
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
      <q-inner-loading
        :showing="true"
        label="Daten werden gespeichert…"
        label-class="text-green"
        class="bg-dark"
        label-style="font-size: 1.5em"
        color="white"
        size="7em"
      />
    </div>
    <div v-else>
      <q-inner-loading
        :showing="true"
        :label="planName || 'Planübersicht wird geladen'"
        label-class="text-white"
        class="bg-dark"
        label-style="font-size: 1.5em"
        color="white"
        size="7em"
      />
    </div>
  </q-page>
</template>

<script>
import ChartComponent from 'src/components/ChartComponent.vue'
import PlanstateListItem from 'src/components/PlanstateListItem.vue'
import { usePlanEditorStore } from 'src/stores/editor_store.js'
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
      console.log('PlanInfo Changed!')
      this.planInfoChanged = true
    }
  },
  created: async function () {
    this.planId = this.$route.params.planid

    await this.planEditorStore.loadPlanDetails(this.planId)
    const planDetails = this.planEditorStore.planDetails[this.planId]
    this.planDetailsLoaded = true

    this.currentNumberOfNodes = planDetails.currentNumberOfNodes
    this.currentNumberOfLines = planDetails.currentNumberOfLines
    this.currentNumberOfLabels = planDetails.currentNumberOfLabels
    this.currentNumberOfEdges = planDetails.currentNumberOfEdges
    this.lastModifiedAt = planDetails.lastModifiedAt
    this.planName = planDetails.planName
    this.planDescription = planDetails.planDescription
    this.currentState = planDetails.currentState
    this.planstates = planDetails.history
    this.shortlinks = planDetails.shortlinks
    this.shortlinks[0].active = true
    const views = planDetails.shortlinks[0].stats.views
    this.totalViewCount = planDetails.shortlinks[0].stats.totalCount

    this.views = {
      daily: [],
      hourly: []
    }
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
    for (const [timestamp, count] of Object.entries(viewsDaily)) {
      this.views.daily.push([parseInt(timestamp), count])
    }
    for (const [timestamp, count] of Object.entries(viewsHourly)) {
      this.views.hourly.push([parseInt(timestamp), count])
    }
    console.log('Views:', this.views)
  },
  components: { PlanstateListItem, ChartComponent }
}
</script>
