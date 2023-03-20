<template>
  <q-page
    class="doc-container flex justify-center bg-primary q-pb-xl text-white"
    padding
    dark
  >
    <div class="row justify-center" style="width: 100%" v-if="this.loaded">
      <div class="column col-xs-12 col-sm-10 col-md-8 q-px-sm">
        <div class="row q-my-lg">
          <div class="column items-center justify-center col-12 text-white">
            <div class="text-h4 text-center q-mt-lg">Neuen Plan erstellen</div>
            <hr color="white" width="200px;" />
          </div>
        </div>
        <div class="row items-center justify-center">
          <div class="column col-6">
            <div class="column col-6 text-h6">Planname:</div>
            <div class="column col-6 text-white">
              <div class="q-my-sm">
                <q-input
                  dark
                  color="white"
                  outlined
                  v-model="planName"
                  input-class="text-h6"
                  input-style="text-align: center"
                  :rules="[
                    (val) => val.length <= 20 || 'Maximal 20 Zeichen erlaubt',
                  ]"
                />
              </div>
            </div>
          </div>
        </div>
        <div class="row items-center justify-center">
          <div class="column col-xs-12 col-sm-6">
            <div class="column col-6 text-h6">Planbeschreibung:</div>
            <div class="column col-6 text-white">
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
        <div class="row items-center justify-center q-my-lg q-mt-xl">
          <div class="column">
            <q-btn color="teal-9" push glossy class="text-h6" icon-right="check">
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
    <div v-else>
      <q-inner-loading
        :showing="true"
        :label="planName || 'Daten werden geladen'"
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
import { ref } from 'vue'

export default {
  name: 'CreatePlanPage',
  setup () {
    return {
      loaded: ref(true),
      planName: ref('Neuer Plan'),
      planDescription: ref('Beschreibung des neuen Plans.')
    }
  },
  computed: {
    forked: function () {
      return !!(
        this.$route.params?.planstateid || this.$route.params?.shortlink
      )
    }
  }
}
</script>
