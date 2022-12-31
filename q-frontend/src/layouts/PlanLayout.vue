<template>
  <q-layout view="lHh lpR lFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat icon="menu" @click="toggleLeftDrawer" />

        <q-toolbar-title>
          Metroplanner
        </q-toolbar-title>
        <q-btn label="Login" color="green-6" class="q-pa-sm q-px-md text-body1" icon="person" />
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" side="left" behavior="mobile" bordered :width="400" class="text-body1">
      <q-scroll-area style="height: calc(100% - 150px); margin-top: 150px; border-right: 1px solid #ddd">
        <q-list padding>
          <q-item>
            <q-item-section>
              <q-text class="text-h5 q-pa-sm">
                {{ planData.planName }}
              </q-text>
            </q-item-section>
          </q-item>

          <q-separator class="q-my-lg" />

          <q-item>
            <q-item-section avatar class="q-ml-md">
              <q-icon name="clear_all" />
            </q-item-section>

            <q-item-section>
              Linien:
            </q-item-section>

            <q-item-section>
              {{ planData.numberOfLines || 0 }}
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
              {{ planData.numberOfNodes || 0 }}
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
              {{ planData.numberOfEdges || 0 }}
            </q-item-section>
          </q-item>

          <q-separator class="q-my-lg" />

          <q-item>
            <q-item-section>
              <div class="row">
                <div class="col-xs-6">
                  <q-icon name="visibility" size="sm" class="q-mx-md" />
                  {{ planStats.totalCount || 0 }}
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

      <q-img class="absolute-top" style="height: 150px">
        <div class="absolute-bottom bg-primary">
          <div class="row q-pt-md">
            <div class="col-xs-6">
              Plan erstellt von:
              <div class="text-weight-bold text-h6">{{ planOwner.displayName }}</div>
            </div>
            <div class="col-xs-grow">
            </div>
            <div class="col-shrink">
              <q-btn flat round :to="'/users/' + planOwner._id">
                <q-avatar size="72px" class="q-mb-sm">
                  <img :src="planOwner.profilePicture || 'https://source.boringavatars.com/pixel/72/' + planOwner._id + '?colors=66f873,5a3dcf,99848a'">
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
      <router-view />
    </q-page-container>

    <!--
    <q-footer class="bg-grey-8 text-white">
      <q-toolbar>
        <q-toolbar-title>
          Metroplanner
        </q-toolbar-title>
      </q-toolbar>
    </q-footer>-->

  </q-layout>
</template>

<script>
import { toRaw, ref } from 'vue'
import axios from 'axios'

export default {
  setup () {
    const leftDrawerOpen = ref(false)

    return {
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  },
  data () {
    return {
      planData: {},
      planOwner: {},
      planStats: {}
    }
  },
  created () {
    axios.get('/api/plan/' + this.$route.params.shortlink).then(response => {
      const rawData = toRaw(response.data)
      this.planData = rawData.plan
      this.planStats = rawData.stats
      this.planData.createdAt = rawData.plan.createdAt.slice(0, 10)
      this.planData.lastModifiedAt = rawData.plan.lastModifiedAt.slice(0, 10)
      // console.log('raw, plan data, plan owner, planstats::', rawData, this.planData, this.planOwner, this.planStats)
      // console.log('planData.planName', this.planData.planName)

      axios.get('/api/user/' + this.planData.ownedBy).then(response => {
        this.planOwner = response.data
        console.log('plan data, plan owner, planstats::', this.planData, this.planOwner, this.planStats)
      })
    })
  },
  mounted () {
  }
}
</script>
