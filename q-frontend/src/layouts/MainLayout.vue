<template>
  <q-layout view="hHh lpR fff">
    <q-header
      elevated
      class="bg-dark text-white"
      dark
      style="box-shadow: 0 0 5px 3px white"
    >
      <q-toolbar>
        <HeaderLogo> </HeaderLogo>
        <LoginContextButton> </LoginContextButton>
      </q-toolbar>
      <q-toolbar v-if="staging">
        <q-toolbar-title class="text-center text-h4 q-pa-md" style="background-color: #770; color: #fff;">
          Staging-Umgebung: Nicht verwenden
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>

    <PageFooter></PageFooter>
  </q-layout>
</template>

<script>
import { defineComponent } from 'vue'
import HeaderLogo from 'src/components/HeaderLogo.vue'
import LoginContextButton from 'src/components/LoginContextButton.vue'
import PageFooter from 'src/components/PageFooter.vue'

export default defineComponent({
  name: 'MainLayout',
  setup () {
    const staging = process.env.Env === 'dev'
    return {
      staging
    }
  },
  components: { HeaderLogo, LoginContextButton, PageFooter }
})
</script>
