<template>
  <q-btn to="/p/wesel" flat no-caps>
    <q-item
      class="text-body1 q-my-sm"
      style="width: 100%; background-color: #003; border-radius: 10px"
    >
      <div class="row text-center justify-around items-center" style="width: 100%; min-height: 100px">
        <div class="column col-xs-12 col-sm-6 col-md-2">
          <q-item-section avatar squared>
            <div
              class="bg-secondary q-pa-md q-px-lg"
              style="border-radius: 10px"
            >
              <img
                alt="Quasar logo"
                src="/icons/mpl_logo.svg"
                style="width: 100px; height: 100px"
              />
            </div>
          </q-item-section>
        </div>
        <div class="col-xs-12 col-sm-6 col-md-9">
          <q-item-section>
            <q-item-label class="text-h6">
              {{ planName }}
            </q-item-label>
            Dies ist der Plan für Wesel
          </q-item-section>
        </div>
        <div class="col-xs-12 col-sm-6 col-md-1">
          <q-item-section side top>
            <q-btn no-caps class="bg-primary" to="/details/">
              <q-item-label class="text-white" caption>Details</q-item-label>
            </q-btn>
          </q-item-section>
        </div>
      </div>
    </q-item>
  </q-btn>
</template>

<script>
export default {
  name: 'PlanListItem',
  setup () {
    return {}
  },
  props: {
    planName: String
  }
  /* watch: {
    planName: function (newVal, oldVal) {
      console.log('Plan Name changed from ', oldVal, ' to ', newVal)
    }
  } */
}
</script>
