<template>
  <q-layout view="hHh lpR fff">
    <q-header elevated>
      <q-toolbar>
        <HeaderLogo :absolute-left='true'> </HeaderLogo>
        <LoginContextButton> </LoginContextButton>
      </q-toolbar>
      <q-toolbar-title v-if="staging" class="text-center rounded-border text-h6"
        style="background-color: #ff7c; color: black;">
        ! Entwicklungs-Umgebung !
      </q-toolbar-title>
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
