<template>
  <q-page class="doc-container flex flex-center bg-primary q-pb-xl">
    <div class="col text-white" style="max-width: 1000px">
      <div class="row justify-center q-my-md">
        <div class="text-h6 text-center col-12">
          Willkommen auf der Metroplanner-Instanz
        </div>
        <div class="row justify-center">
          <div class="text-h4 text-center col-12">
            <pre><code style="color:#c70; background-color:#000; border-radius: 10px;"> {{ instanceName }} </code></pre>
          </div>
        </div>
        <div class="q-mt-lg row justify-center">
          <div class="text-body1 text-center column col-sm-8 col-xs-12 q-px-xs">
            Metroplanner ist ein Webtool zur Erstellung und zum Anzeigen von
            intuitiven und diagramm-ähnlichen Liniennetzplänen für den ÖPNV.
            Aufgrund der einfachen Bedienung eignet sich Metroplanner
            insbesondere zur Erstellung von Netzplänen in kleineren Städten und
            Gemeinden, die heute häufig noch keine derartigen Pläne besitzen.<br>
          </div>
        </div>
        <div class="q-mt-lg row justify-center">
          <div class="text-body1 text-center column col-12">
            <q-btn outline no-wrap no-caps to="/project" color="green">
              Über das Projekt
            </q-btn>
          </div>
        </div>
      </div>
      <!--<div class="q-my-lg text-h2 text-bold text-center">
        Metroplanner
      </div>-->

      <!----<hr class="q-my-lg" />-->

      <div class="text-h6 q-mx-lg q-mt-xl">Ausgewählte Nahverkehrs-Pläne:</div>

      <q-list padding separator class="text-white" style="width: 100%">
        <PlanListItem v-for="shortlink of plans" :key="shortlink" :planShortlink="shortlink" style="width: 100%">
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
    // planDescription = planViewerStore.plans[this.planShortlink].info.planDescription
    // planName = planViewerStore.plans[this.planShortlink].info.planName
    const instanceName = window.location.toString().replace('http://', '').replace('https://', '').split(':')[0].split('/')[0]

    return {
      plans: [
        'walsumbahn',
        'wesel',
        'showcase'
      ],
      instanceName
    }
  },
  components: { PlanListItem }

})
</script>
