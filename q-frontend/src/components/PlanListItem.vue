<template>

  <q-item class="text-body1">
    <q-btn to="/p/wesel" flat no-caps>
      <q-item-section avatar squared>
        <q-btn to="/p/wesel" flat class="bg-secondary">
          <img alt="Quasar logo" src="/icons/mpl_logo.svg" style="width: 100px; height: 100px">
        </q-btn>
      </q-item-section>

      <q-item-section>
        <q-item-label class="text-h6">
          {{ planName }}
        </q-item-label>
        Dies ist der Plan für Wesel
      </q-item-section>

      <q-item-section side top>
        <q-btn no-caps class="bg-primary" to="/details/">
          <q-item-label class="text-white" caption>Details</q-item-label>
        </q-btn>
      </q-item-section>
    </q-btn>
  </q-item>

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
