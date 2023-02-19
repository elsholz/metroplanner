<template>
  <q-toolbar-title>
    <q-btn no-caps flat class="text-h6 q-my-xs" to="/">
      <q-avatar square class="">
        <img src="/icons/favicon-128x128.png">
      </q-avatar>
      <div style="line-height:140%;" class="text-left q-mx-lg">
        Metroplanner
        <div class="text-weight-thin text-monospace bg-blue-grey-10" style="border-radius:5px; margin:0; line-height: 110%; color: #c70">
          <pre style="margin: 0"><code>ich-hab-Plan.de</code></pre>
        </div>
      </div>
    </q-btn>
  </q-toolbar-title>
</template>

<script>
export default {
  name: 'HeaderLogo',
  setup () {
    return {}
  }
}
</script>
