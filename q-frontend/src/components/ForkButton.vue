<template>
  <q-btn
    dark
    icon="fa fa-light fa-code-fork"
    class="bg-yellow-10 q-py-sm"
    :to="linkTo"
  >
    <q-tooltip class="text-body2" color="orange-10">Neuen Plan erstellen und Initialzustand hiervon ableiten (Fork)</q-tooltip>
  </q-btn>
</template>

<script>
export default {
  setup () {
    return {}
  },
  props: {
    planstateid: String,
    planid: String,
    shortlink: String
  },
  computed: {
    linkTo: function () {
      return this.planid ? `/edit/${this.planid}/${this.planstateid}/fork` : `/p/${this.shortlink}/fork`
    }
  }
}
</script>
