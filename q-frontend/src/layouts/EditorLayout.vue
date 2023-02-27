<template>
  <q-layout view="lHr lpR fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />

        <!--<HeaderLogo absoluteLeft="false" absoluteCenter="false"></HeaderLogo>
        -->
        <q-toolbar-title>{{ planName }}</q-toolbar-title>

        <q-btn dense flat round icon="menu" @click="toggleRightDrawer" />
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      side="left"
      bordered
      :mini="leftDrawerMini"
    >
      <!-- drawer content -->
      Drawer Content
    </q-drawer>

    <q-drawer v-model="rightDrawerOpen" side="right" bordered>
      <!-- drawer content -->
      Drawer contetn
    </q-drawer>

      <PlanEditor></PlanEditor>
  </q-layout>
</template>

<script>
// import HeaderLogo from 'src/components/HeaderLogo.vue'
import PlanEditor from 'src/pages/PlanEditor.vue'
import { ref } from 'vue'

export default {
  setup () {
    const leftDrawerOpen = ref(true)
    const rightDrawerOpen = ref(false)
    const leftDrawerMini = ref(false)
    const planName = 'Liniennetzplan Wesel'
    return {
      planName,
      leftDrawerOpen,
      leftDrawerMini,
      toggleLeftDrawer () {
        leftDrawerMini.value = !leftDrawerMini.value
      },
      rightDrawerOpen,
      toggleRightDrawer () {
        rightDrawerOpen.value = !rightDrawerOpen.value
      }
    }
  },
  components: { PlanEditor }
}
</script>

<!--<script>
import { defineComponent } from 'vue'
import HeaderLogo from 'src/components/HeaderLogo.vue'
import LoginContextButton from 'src/components/LoginContextButton.vue'
import PageFooter from 'src/components/PageFooter.vue'

export default defineComponent({
  name: 'EditorLayout',
  setup () {
    const staging = process.env.Env === 'dev'
    return {
      staging
    }
  },
  components: { HeaderLogo, LoginContextButton, PageFooter }
})
</script>-->
