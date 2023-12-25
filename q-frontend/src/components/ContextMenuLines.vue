<template>
  <div class="row q-my-sm justify-center text-h6">
    Kontext-Menü: Linien
  </div>
  <!--<q-scroll-area :style="`
      height: calc(100% - 150px);
      margin-top: 150px;
      border-right: 1px solid #ddd;
    `">-->
    <q-list dark class="text-body1 text-white">
      <!--<q-item class="q-mx-sm">
        <q-item-section>
          <div class="row items-center no-wrap">
            <div class="col col-2">
              <div class="text-h6">Filter:</div>
            </div>
            <div class="col col-10">
              <q-input v-model="searchTerm" dense clearable color="white" outlined>
              </q-input>
            </div>
          </div>
        </q-item-section>
      </q-item>-->

      <template v-for="lineid of Object.keys(lines)" :key="lineid">
        <LineListItem :lineid="lineid"> </LineListItem>
      </template>
    </q-list>
    {{ lines }}
  <!--</q-scroll-area>-->
</template>

<script>
import LineListItem from './LineListItem.vue'
import { storeToRefs } from 'pinia'
import { ref, toRefs } from 'vue'
import { usePlanEditorStore } from 'src/stores/editor_store'

const planEditorStore = usePlanEditorStore()

const { lines } = storeToRefs(planEditorStore)

export default {
  setup () {
    toRefs(lines)
    return {
      lines,
      searchTerm: ref('')
    }
  },
  components: { LineListItem }
}
</script>
