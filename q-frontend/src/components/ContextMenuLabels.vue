<template>
  <div class="row q-my-sm justify-center text-h6">
    Kontext-Menü: Beschriftungen
  </div>
  Alle Labels:
  {{ labels }}
</template>

<script>
import { usePlanEditorStore } from 'src/stores/editor_store'
import { storeToRefs } from 'pinia'

const planEditorStore = usePlanEditorStore()

const { labels } = storeToRefs(planEditorStore)

export default {
  setup () {
    return { labels }
  }
}
</script>
