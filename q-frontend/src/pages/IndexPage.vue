<template>
  <q-page class="flex flex-center">
    <div class="nodescontainer" id="nodes" ref="el">
      ABC

    </div>
    <img alt="Quasar logo" src="~assets/quasar-logo-vertical.svg" style="width: 200px; height: 200px">
  </q-page>
</template>

<script setup>
// import axios from 'src/boot/axios'
import axios from 'axios'
import { ref, onMounted, defineComponent } from 'vue'

const el = ref()

onMounted(() => {
  console.log(el.value)

  // axios.get('https://catfact.ninja/fact').then(response => {
  axios.get('http://localhost:9000/api/plan/test').then(response => {
    el.value.innerText = response.data.planName
    console.log(response)
  })

  const mapstyle = document.createElement('style')
  mapstyle.id = 'mapstyle'
  mapstyle.innerText = `
  #nodes {
    background-color: #ccc;
  } 
  `

  console.log(mapstyle)
  document.body.appendChild(mapstyle)
  console.log(document.body)
})
</script>

<script>
export default defineComponent({
  name: 'IndexPage'
})
</script>
