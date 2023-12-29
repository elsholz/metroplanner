<template>
  <q-btn :to="'/p/' + planShortlink" no-caps>
    <q-item class="text-body1 q-my-sm" style="width: 100%; background-color: #003; border-radius: 10px">
      <div class="row text-center justify-around items-center" style="width: 100%; min-height: 100px">
        <template v-if="this.planInfo?.planName">
          <div class="column col-xs-6 col-sm-2">
            <q-item-section avatar squared>
              <div class="bg-secondary q-pa-md q-px-lg" style="border-radius: 10px">
                <img alt="Quasar logo" src="/icons/mpl_logo.svg" style="width: 100%; height: auto; max-height: 200px" />
              </div>
            </q-item-section>
          </div>
          <div class="col-xs-6 col-sm-8 text-left" style="display: block; overflow: hidden; text-overflow: ellipsis">
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
            <template v-if="planShortlink && !planId">
              <q-btn no-caps class="bg-blue q-my-sm q-mx-sm" :to="'/p/' + planShortlink" v-if="planShortlink">
                <q-item-label class="text-white" caption>Details</q-item-label>
              </q-btn>
            </template>
            <template v-if="planId">
              <q-btn no-caps class="bg-positive q-my-sm q-mb-xs q-mx-sm" :to="'/edit/' + planId" glossy push>
                <q-item-label class="text-white" caption>Bearbeiten</q-item-label>
              </q-btn>
              <q-btn no-caps outline to="/" class="q-my-xs q-mx-sm" color="negative" @click="openConfirmDeletionDialog" size="sm">
                <q-item-label class="text-negative" caption>Löschen</q-item-label>
              </q-btn>
              <q-dialog v-model="confirmDeletion">
                <q-card class="bg-negative text-white">
                  <q-card-section class="row items-center">
                    <q-avatar icon="delete" color="red" text-color="white" />
                    <span class="q-ml-md text-body1">Löschen von</span>
                    <span class="q-mx-sm text-italic text-h6 text-bold">{{ this.planName }}</span>
                    <span class="q-mr-sm text-body1">bestätigen?</span>
                  </q-card-section>

                  <q-card-actions align="center">
                    <q-btn no-caps outline label="Abbrechen" color="gray" v-close-popup />
                    <q-btn no-caps flat label="Karte unwiderruflich löschen" color="grey-13" @click="this.deletePlan" v-close-popup />
                  </q-card-actions>
                </q-card>
              </q-dialog>
            </template>
          </div>
        </template>
        <template v-else>
          <q-inner-loading :showing="true" label="Wird geladen..." label-class="text-white" class="bg-primary"
            style="border: 3px solid #fff5; border-radius: 10px" label-style="font-size: 1em" color="white" size="1em" />
        </template>
      </div>
    </q-item>
  </q-btn>
</template>

<script>
import { ref } from 'vue'
import { usePlanViewerStore } from 'src/stores/viewer_store'
import { useUserStore } from 'src/stores/user_store'
import { useQuasar } from 'quasar'

const planViewerStore = usePlanViewerStore()
const userStore = useUserStore()

export default {
  name: 'PlanListItem',
  setup: function () {
    return {
      planInfo: ref({}),
      $q: useQuasar(),
      confirmDeletion: ref(false),
      abortDeletion: ref(false)
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
  },
  methods: {
    openConfirmDeletionDialog: async function (e, go) {
      e.preventDefault()
      this.confirmDeletion = true
    },
    deletePlan: async function () {
      console.log('Deletion requested for plan', this.planName, this.planId)
      this.$q.notify({
        message: `»${this.planName}« wird in Kürze gelöscht...`,
        spinner: true,
        timeout: 7000,
        progress: true,
        type: 'negative',
        actions: [
          {
            // icon: 'abort',
            label: 'abbrechen',
            color: 'white',
            'aria-label': `Löschen vom Plan "${this.planName}" abbrechen`,
            handler: () => { this.abortDeletion = true }
          }
        ],
        onDismiss: async () => {
          if (this.abortDeletion) {
            console.log('Deletion has been aborted', this.planName, this.planId)
            this.abortDeletion = false
          } else {
            console.log('Deletion will be committed', this.planName, this.planId)
            await userStore.deletePlan(this.planId, this.planName)
          }
        }
      })
    }
  }
}
</script>
