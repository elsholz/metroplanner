<template>
  <q-page
    class="doc-container flex justify-center bg-primary q-pb-xl text-white"
    padding
    dark
  >
    <div class="row justify-center" style="width: 100%" v-if="this.loaded && !this.creating">
      <div class="column col-xs-12 col-sm-10 col-md-8 q-px-sm">
        <div class="row q-my-md">
          <div class="column items-center justify-center col-12 text-white">
            <div class="text-h4 text-center q-mt-lg">Neuen Plan erstellen</div>
            <hr color="white" width="200px;" />
          </div>
        </div>
        <div class="row items-center justify-center">
          <div class="column col-6">
            <div class="text-h6">Planname:</div>
            <div class="text-white">
              <div class="q-my-sm">
                <q-input
                  dark
                  color="white"
                  outlined
                  v-model="planName"
                  input-class="text-h6"
                  input-style="text-align: center"
                  :rules="[
                    (val) => val.length <= 50 || 'Maximal 50 Zeichen erlaubt',
                  ]"
                />
              </div>
            </div>
          </div>
        </div>
        <div class="row items-center justify-center">
          <div class="column col-xs-12 col-sm-6">
            <div class="text-h6">Planbeschreibung:</div>
            <div class="text-white">
              <div class="q-my-sm">
                <q-input
                  dark
                  color="white"
                  outlined
                  v-model="planDescription"
                  autogrow
                  input-class="text-body1"
                  input-style="text-align: left"
                  :rules="[
                    (val) => val.length <= 200 || 'Maximal 200 Zeichen erlaubt',
                  ]"
                />
              </div>
            </div>
          </div>
        </div>

        <div class="row items-center justify-center">
          <div class="column col-xs-12 col-sm-6">
            <div class="text-h6 text-center">Anfänglicher Planinhalt</div>
            <hr color="white" width="200px;" />
            <div class="text-body1 text-center text-italic" v-if="!this.forked">Leer</div>
            <PlanstateListItem
              :statsOnly="true"
              :planId="undefined"
              :planstateId="undefined"
              :numberOfEdges="this.numberOfEdges || 0"
              :numberOfNodes="this.numberOfNodes || 0"
              :numberOfLines="this.numberOfLines || NaN"
              :numberOfLabels="this.numberOfLabels || 0"
              :isCurrentState="false"
              :actionsEnabled="false"
              style="width: 100%"
              v-else
            >
            </PlanstateListItem>
          </div>
        </div>

        <div class="row items-center justify-center ">
          <div class="column">
            <q-btn
              color="teal-9"
              push
              glossy
              class="text-body1"
              icon-right="check"
              @click="createPlan()"
            >
              Plan erstellen
            </q-btn>
          </div>
        </div>

        <!--
        <div class="row" v-if="forked">
          <div class="column col-12 text-white">
            <div class="row justify-center" style="width: 100%">
              <div class="text-h4">Initialer Planzustand</div>
            </div>
            <div class="row justify-center" style="width: 100%">
              <hr color="white" width="200px;" />
            </div>
            <div class="row justify-center" style="width: 100%">
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
            </div>
          </div>
        </div>-->
      </div>
    </div>
    <div v-else-if="this.creating">
      <q-inner-loading
        :showing="true"
        label="Plan wird erstellt..."
        class="bg-dark"
        label-style="font-size: 1.5em"
        color="white"
        size="7em"
      />
    </div>
<div v-else>
      <q-inner-loading
        :showing="true"
        label="Daten werden geladen"
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
import PlanstateListItem from 'src/components/PlanstateListItem.vue'
import { ref } from 'vue'
import { usePlanEditorStore } from 'src/stores/editor_store'
import { usePlanViewerStore } from 'src/stores/viewer_store'
import { useUserStore } from 'src/stores/user_store'

export default {
  name: 'CreatePlanPage',
  setup () {
    return {
      loaded: ref(false),
      creating: ref(false),
      planName: ref('Neuer Plan'),
      planDescription: ref('Beschreibung des neuen Plans.'),
      currentNumberOfNodes: ref(undefined),
      currentNumberOfLines: ref(undefined),
      currentNumberOfLabels: ref(undefined),
      currentNumberOfEdges: ref(undefined),
      colorTheme: ref('colorful-dl')
    }
  },
  created: async function () {
    if (this.forked) {
      let planStateDetails
      if (this.$route?.params?.planstateid) {
        const planstateid = this.$route.params.planstateid
        const planid = this.$route.params.planid
        const planEditorStore = usePlanEditorStore()
        await planEditorStore.loadPlanState(planid, planstateid)
        planStateDetails = planEditorStore.planState
      } else {
        const shortlink = this.$route.params.shortlink
        const planViewerStore = usePlanViewerStore()
        await planViewerStore.getPlanState(shortlink)
        planStateDetails = planViewerStore.plans[shortlink].state
      }
      console.log('details about forked plan:', planStateDetails)
      this.numberOfNodes = planStateDetails?.numberOfNodes
      this.numberOfLines = planStateDetails?.numberOfLines
      this.numberOfLabels = planStateDetails?.numberOfLabels
      this.numberOfEdges = planStateDetails?.numberOfEdges
    }
    this.loaded = true
  },
  computed: {
    forked: function () {
      return !!(
        this.$route.params?.planstateid || this.$route.params?.shortlink
      )
    }
  },
  methods: {
    createPlan: async function () {
      console.log('Creating plan...')
      this.creating = true

      const userStore = useUserStore()
      await userStore.createNewPlan({
        planName: this.planName,
        planDescription: this.planDescription,
        colorTheme: this.colorTheme,
        forkFrom: this.forked ? {
          planstateId: this.$route.params.planstateid,
          planId: this.$route.params.planid,
          shortlink: this.$route.params.shortlink
        } : undefined
      }).then((response) => {
        console.log('Response: ', response)
        const planId = response.data.planId

        this.$router.push({
          path: `/edit/${planId}`
        })
      })
    }
  },
  components: { PlanstateListItem }
}
</script>
