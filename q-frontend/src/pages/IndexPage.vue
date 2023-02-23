<template>
  <q-page class="doc-container flex flex-center bg-primary q-pb-xl">
    <div class="col text-white" style="max-width: 1000px;">
      <div class="q-my-xl">
        <div class="text-h6 text-center">
          Willkommen auf
        </div>
        <div class="text-h4 text-center">
          <pre><code style="color:#c70; background-color:#000; border-radius: 10px;"> ich-hab-Plan.de </code></pre>
        </div>
      </div>
      <!--<div class="q-my-lg text-h2 text-bold text-center">
        Metroplanner
      </div>-->

      <hr class="q-my-lg" />

      <div class="text-h4 q-ma-lg">
        Empfohlene Nahverkehrs-Pläne:
      </div>

      <q-list bordered padding separator class="text-white" style="width: 100%;">
        <PlanListItem v-for="plan in dummyPlans" :key="plan.planName" :planName="plan.planName" style="width: 100%;">
        </PlanListItem>
      </q-list>
    </div>
  </q-page>
</template>

<!--<script setup>
// import axios from 'axios'
//import { ref, onMounted, defineComponent } from 'vue'

//const el = ref()

onMounted(() => {
  //  console.log(el.value)

  // axios.get('https://catfact.ninja/fact').then(response => {
  /* axios.get('http://localhost:9000/api/plan/test').then(response => {
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
  */
})
</script>-->

<script>
import { defineComponent } from 'vue'
import PlanListItem from 'app/src/components/PlanListItem.vue'

export default defineComponent({
  name: 'IndexPage',
  data () {
    return {
      dummyPlans: [
        {
          shortLink: 'wesel',
          planName: 'Liniennetzplan Wesel',
          ownedBy: {
            displayName: 'Hendrik Lankers'
          },
          createdAt: '2022-12-30T21:03:03.444',
          lastModifiedAt: '2023-01-01T18:50:03.444',
          likeCount: 0,
          currentColorTheme: '634469a8ccfb6bf5a194fcca',
          currentNumberOfEdges: 385,
          currentNumberOfLabels: 232,
          currentNumberOfLines: 27,
          currentNumberOfNodes: 232,
          totalViewCount: 777
        }
      ]
    }
  },
  components: { PlanListItem }
})
</script>
