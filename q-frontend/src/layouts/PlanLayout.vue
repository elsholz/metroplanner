<template>
  <q-layout view="lHh lpR lFf">
    <q-header elevated class="bg-dark text-white" dark style="box-shadow: 0 0 5px 3px white;">
      <q-toolbar>
        <q-btn dense flat icon="menu" @click="toggleLeftDrawer" class="q-mr-sm" />
        <HeaderLogo> </HeaderLogo>
        <LoginContextButton> </LoginContextButton>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" side="left"
      behavior="mobile" bordered :width="400" class="text-body1" dark style="box-shadow: 0 0 10px 5px gray;">
      <q-scroll-area style="height: calc(100% - 150px); margin-top: 150px; ">
        <q-list padding>
          <q-item>
            <q-item-section>
              <q-text class="text-h5 q-pa-sm">
                {{ planData.planName }}
              </q-text>
            </q-item-section>
          </q-item>

          <q-separator class="q-my-lg" dark />

          <q-item>
            <q-item-section avatar class="q-ml-md">
              <q-icon name="clear_all" />
            </q-item-section>

            <q-item-section>
              Linien:
            </q-item-section>

            <q-item-section>
              {{ planData.currentNumberOfLines || 0 }}
            </q-item-section>
          </q-item>

          <q-item>
            <q-item-section avatar class="q-ml-md">
              <q-icon name="commit" />
            </q-item-section>

            <q-item-section>
              Haltestellen:
            </q-item-section>

            <q-item-section>
              {{ planData.currentNumberOfNodes || 0 }}
            </q-item-section>
          </q-item>

          <q-item>
            <q-item-section avatar class="q-ml-md">
              <q-icon name="polyline" />
            </q-item-section>

            <q-item-section>
              Verbindungen:
            </q-item-section>

            <q-item-section>
              {{ planData.currentNumberOfEdges || 0 }}
            </q-item-section>
          </q-item>

          <q-separator class="q-my-lg" dark />

          <q-item>
            <q-item-section>
              <div class="row">
                <div class="col-xs-6">
                  <q-icon name="visibility" size="sm" class="q-mx-md" />
                  {{ planStats.totalViewCount || 0 }}
                  <q-tooltip class="bg-accent text-body1">
                    Anzahl Aufrufe
                  </q-tooltip>
                </div>
                <div class="col-xs-6">
                  <q-icon name="favorite" size="sm" class="q-mx-md" />
                  {{ planData.likeCount || 0 }}
                  <q-tooltip class="bg-positive text-body1">
                    Anzahl Likes
                  </q-tooltip>
                </div>
              </div>
            </q-item-section>
          </q-item>

          <q-page-sticky position="bottom-left" :offset="[18, 18]">
            <q-fab v-model="fab2" label="Actions" external-label label-class="bg-grey-3 text-black text-body1"
              vertical-actions-align="left" color="primary" icon="keyboard_arrow_up" direction="up" persistent>
              <q-fab-action label-class="bg-grey-3 text-black text-body1" external-label color="primary"
                @click="onClick" icon="share" label="Email" />
              <q-fab-action label-class="bg-grey-3 text-black text-body1" external-label color="positive"
                @click="onClick" icon="favorite" label="Like" />
              <q-fab-action label-class="bg-grey-3 text-black text-body1" external-label color="negative"
                @click="onClick" icon="report" label="Report" />
            </q-fab>
          </q-page-sticky>
        </q-list>
      </q-scroll-area>

      <q-img class="absolute-top" style="height: 150px; border-bottom: 2px solid gray;">
        <div class="absolute-bottom">
          <div class="row q-pt-md">
            <div class="col-xs-6">
              Plan erstellt von:
              <div class="text-weight-bold text-h6">{{ planOwner.displayName || 'unbekannt' }}</div>
            </div>
            <div class="col-xs-grow">
            </div>
            <div class="col-shrink">
              <q-btn flat round :to="'/users/' + planOwner._id">
                <q-avatar size="72px" class="q-mb-sm">
                  <img
                    :src="planOwner.profilePicture || 'https://source.boringavatars.com/pixel/72/' + planOwner._id + '?colors=66f873,5a3dcf,99848a'">
                </q-avatar>
              </q-btn>
            </div>
          </div>

          <div class="row">
            <div class="col-xs-6">
              <q-icon name="auto_awesome" size="xs" class="q-mx-md" />
              {{ planData?.createdAt || '-' }}
              <q-tooltip class="bg-positive text-body1" :offset="[0, 35]">
                Erstellt am
              </q-tooltip>
            </div>
            <div class="col-xs-6">
              <q-icon name="edit" size="xs" class="q-mx-md" />
              {{ planData?.lastModifiedAt || '-' }}
              <q-tooltip class="bg-secondary text-body1" :offset="[0, 35]">
                Zuletzt bearbeitet am
              </q-tooltip>
            </div>
          </div>
        </div>
      </q-img>
    </q-drawer>

    <q-page-container>
      <!---<router-view  hello="world"/>-->
      <PlanViewer :planName="planName"></PlanViewer>

      <!--import PlanViewer from 'pages/PlanViewer.vue'-->
    </q-page-container>

  </q-layout>
</template>

<script>
import { toRaw, ref } from 'vue'
import axios from 'axios'
import PlanViewer from 'src/pages/PlanViewer.vue'
import HeaderLogo from 'src/components/HeaderLogo.vue'
import LoginContextButton from 'src/components/LoginContextButton.vue'

export default {
  setup () {
    const leftDrawerOpen = ref(false)
    return {
      leftDrawerOpen,
      toggleLeftDrawer () {
        console.log('Toggling left drawre open!')
        console.log(leftDrawerOpen.value)
        leftDrawerOpen.value = !leftDrawerOpen.value
        console.log(leftDrawerOpen.value)
      }
    }
  },
  data () {
    return {
      planData: {},
      planOwner: {},
      planStats: {},
      planName: null
    }
  },
  created () {
    console.log(this.$route.params.shortlink)
    axios.get('/api/plan/' + this.$route.params.shortlink).then(response => {
      console.log(response)
      const rawData = toRaw(response.data)
      console.log(rawData)
      this.planData = rawData
      this.planStats = { totalViewCount: rawData.totalViewCount }
      this.planData.createdAt = rawData.createdAt.slice(0, 10)
      this.planData.lastModifiedAt = rawData.lastModifiedAt.slice(0, 10)
      this.planName = this.planData.planName
      // console.log('raw, plan data, plan owner, planstats::', rawData, this.planData, this.planOwner, this.planStats)
      // console.log('planData.planName', this.planData.planName)
      /* axios.get('/api/user/' + this.planData.ownedBy).then(response => {
        this.planOwner = response.data
      }).catch(function (error) {
        console.log('Error fetching user profile: ', error)
      }) */
    })
  },
  mounted () {
  },
  components: { PlanViewer, HeaderLogo, LoginContextButton }
}
</script>
