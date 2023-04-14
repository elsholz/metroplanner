<template>
  <div class="row q-my-sm justify-center text-h6">Einstellungen</div>
  <hr dark />

  <q-list dark class="text-body1 text-white">
    <q-item class="q-py-md">
      <q-item-section>
        <div class="text-h6 q-py-sm">Koordinatenverschiebung:</div>
        <div class="row items-center">
          <div class="col col-2 text-center">X:</div>
          <div class="col col-4">
            <q-input v-model.number="globalOffsetX" type="number" outlined color="white"> </q-input>
          </div>
          <div class="col col-2 text-center">Y:</div>
          <div class="col col-4">
            <q-input v-model.number="globalOffsetY" type="number" outlined color="white"> </q-input>
          </div>
        </div>
      </q-item-section>
    </q-item>
    <q-item class="q-py-md">
      <q-item-section>
        <div class="text-h6 q-py-sm">Plangröße:</div>
        <div class="row items-center">
          <div class="col col-2 text-center">Breite:</div>
          <div class="col col-4">
            <q-input v-model.number="planWidth" type="number" outlined color="white"> </q-input>
          </div>
          <div class="col col-2 text-center">Höhe:</div>
          <div class="col col-4">
            <q-input v-model.number="planHeight" type="number" outlined color="white"> </q-input>
          </div></div
      ></q-item-section>
    </q-item>
  </q-list>
</template>

<script>
import { usePlanEditorStore } from 'src/stores/editor_store'
import { storeToRefs } from 'pinia'
const planEditorStore = usePlanEditorStore()
const { planWidth, planHeight, globalOffsetX, globalOffsetY } =
  storeToRefs(planEditorStore)

export default {
  setup () {
    return {
      planWidth,
      planHeight,
      globalOffsetX,
      globalOffsetY
    }
  }
}
</script>
