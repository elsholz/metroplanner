<template>
  <q-page padding>
    <!-- content
    Plan:
    <pre style="background-color: #333; color:#fff"><code ref="plan"></code></pre>
    Plan Data:
    <pre style="background-color: #333; color: #fff"><code ref="plandata"></code></pre>
    -->
    <div id="canvas" style="width:1000px; height:800px; overflow: auto;"
      v-if="planState && planState.nodes && planState.lines && planState.labels">
      <div id="lines">
        <h6>
          Lines:
        </h6>
        <div v-for="(value, key) in planState.lines" v-bind:key="key">
          {{ JSON.stringify(key) }}: {{ JSON.stringify(value) }}
        </div>
      </div>

      <div id="nodes">
        <h6>
          Nodes:
        </h6>
        <div v-for="(value, key) in planState.nodes" v-bind:key="key">
          {{ JSON.stringify(key) }}: {{ JSON.stringify(value) }}
        </div>
      </div>

      <div id="labels">
        <h6>
          Labels:
        </h6>
        <div v-for="(value, key) in planState.labels" v-bind:key="key">
          {{ JSON.stringify(key) }}: {{ JSON.stringify(value) }}
        </div>
      </div>
    </div>

    <pre style="background-color: #333; color:#fff"><code>{{ JSON.stringify(planState, null, 4) }}</code></pre>
  </q-page>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PlanViewer',
  data () {
    return {
      planState: {}
    }
  },
  created () {
    axios.get('/api/planstate/' + this.$route.params.shortlink).then(response => {
      // this.$refs.plandata.innerText += JSON.stringify(response.data, null, 4)
      // console.log(response)
      this.planState = response.data
    })
  },
  mounted () {
    // console.log('this.refs::', this.$refs.el)
    // console.log(this.$route.params.shortlink)

    /* axios.get('/api/plan/' + this.$route.params.shortlink).then(response => {
      this.$refs.plan.innerText += JSON.stringify(response.data, null, 4)
      console.log(response)
    }) */
    // axios.get('/api/planstate/' + this.$route.params.shortlink).then(response => {
    //   // this.$refs.plandata.innerText += JSON.stringify(response.data, null, 4)
    //   // console.log(response)
    // })

    // const mapstyle = document.createElement('style')
    // mapstyle.id = 'mapstyle'
    // mapstyle.innerText = `
    //   #nodes {
    //     background-color: #ccc;
    //   }
    // `
    // console.log('parent refs:', this.$parent)

    // console.log(mapstyle)
    // document.body.appendChild(mapstyle)
    // console.log(document.body)
  }
}
</script>
