<template>
  <q-btn :to="'/p/' + planShortlink" no-caps>
    <q-item
      class="text-body1 q-my-sm"
      style="width: 100%; background-color: #003; border-radius: 10px"
    >
      <div
        class="row text-center justify-around items-center"
        style="width: 100%; min-height: 100px"
      >
        <template v-if="this.planInfo?.planName">
          <div class="column col-xs-6 col-sm-2">
            <q-item-section avatar squared>
              <div
                class="bg-secondary q-pa-md q-px-lg"
                style="border-radius: 10px"
              >
                <img
                  alt="Quasar logo"
                  src="/icons/mpl_logo.svg"
                  style="width: 100%; height: auto; max-height: 200px"
                />
              </div>
            </q-item-section>
          </div>
          <div
            class="col-xs-6 col-sm-8 text-left"
            style="display: block; overflow: hidden; text-overflow: ellipsis"
          >
            <q-item-label class="text-h6">
              {{ this.planInfo.planName }}
            </q-item-label>
            {{
              this.planInfo.planDescription.length > ($q.screen.gt.xs ? 250 : 190)
                ? this.planInfo.planDescription.slice(0, $q.screen.gt.xs ? 250 : 190) +
                  "..."
                : this.planInfo.planDescription
            }}
          </div>
          <div class="col-xs-6 col-md-2 col-sm-2 q-py-md">
            <template v-if="planShortlink">
              <q-btn no-caps class="bg-blue q-my-sm q-mx-sm" :to="'/p/' + planShortlink" v-if="planShortlink">
                <q-item-label class="text-white" caption>Details</q-item-label>
              </q-btn>
            </template>
            <template v-if="planId">
              <q-btn no-caps class="bg-purple q-my-sm q-mx-sm" :to="'/edit/' + planId">
                <q-item-label class="text-white" caption>Bearbeiten</q-item-label>
              </q-btn>
            </template>
          </div>
        </template>
        <template v-else>
          <q-inner-loading
            :showing="true"
            label="Wird geladen..."
            label-class="text-white"
            class="bg-primary"
            style="border: 3px solid #fff5; border-radius: 10px"
            label-style="font-size: 1em"
            color="white"
            size="1em"
          />
        </template>
      </div>
    </q-item>
  </q-btn>
</template>

<script>
import { ref } from 'vue'
import { usePlanViewerStore } from 'src/stores/viewer_store'

const planViewerStore = usePlanViewerStore()

export default {
  name: 'PlanListItem',
  setup: function () {
    return {
      planInfo: ref({})
    }
  },
  props: {
    planShortlink: String,
    planId: String,
    planName: String,
    planDescription: String
  },
  mounted: async function () {
    if (this.planName && this.planDescription) {
      this.planInfo = {
        planName: this.planName,
        planDescription: this.planDescription
      }
    } else {
      await planViewerStore.getPlanInfo(this.planShortlink)
      this.planInfo = planViewerStore.plans[this.planShortlink].info
      console.log(this.planInfo)
    }
  }
}
</script>
