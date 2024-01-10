<template>
  <q-toolbar-title
    :class="
      $q.screen.gt.xs
        ? this.absoluteLeft === true
          ? 'absolute-left'
          : ''
        : 'absolute-center'
    "
  >
    <q-btn no-caps flat class="text-h6" to="/">
      <template v-if="$q.screen.gt.xs">
        <q-avatar square>
          <img src="/icons/favicon-128x128.png" />
        </q-avatar>
        <div style="line-height: 140%" class="text-center">
          <div class="row">
            <div class="text-bold q-pt-sm text-h5 q-pl-sm">METROPLANNER</div>
            <div
              class="text-weight-thin q-pl-lg text-monospace q-pt-sm"
              style="margin: 0; line-height: 110%; color: #c70"
            >
              <pre
                style="margin: 0; border-radius: 10px"
                class="bg-blue-grey-10 q-pa-xs q-px-sm"
              ><code>{{ instanceName }}</code></pre>
            </div>
          </div>
        </div>
      </template>
      <template v-else>
        <div class="no-wrap row">
          <div class="col col-auto q-pt-sm q-pr-sm">
            <q-avatar square size="md" style="margin: 0; padding: 0">
              <img src="/icons/favicon-128x128.png" />
            </q-avatar>
          </div>
          <div class="col col-10">
            <div style="margin-bottom: 0">METROPLANNER</div>
            <div
              class="text-weight-thin text-monospace bg-blue-grey-10 q-mt-xl"
              style="
                border-radius: 5px;
                margin: 0;
                margin-top: -5px;
                line-height: 110%;
                color: #c70;
              "
            >
              <pre style="margin: 0"><code>{{ instanceName }}</code></pre>
            </div>
          </div>
        </div>
      </template>
    </q-btn>
  </q-toolbar-title>
</template>

<script>
export default {
  name: 'HeaderLogo',
  setup () {
    const instanceName = window.location.toString().replace('http://', '').replace('https://', '').split(':')[0].split('/')[0]
    return { instanceName }
  },
  props: {
    absoluteLeft: Boolean
  }
}
</script>
