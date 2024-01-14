<template>
  <div class="row q-my-sm justify-center text-h6">
    Kontext-Menü: Beschriftungen
  </div>
  Alle Labels:
  {{ independentLabels }}
</template>

<script>
import { usePlanEditorStore } from 'src/stores/editor_store'
import { storeToRefs } from 'pinia'

const planEditorStore = usePlanEditorStore()

const { independentLabels } = storeToRefs(planEditorStore)

export default {
  setup () {
    return { independentLabels }
  }
}
</script>
