<template>
  <q-layout view="lHh lpR lFf">
    <q-header
      elevated
      class="bg-dark text-white"
      dark
      style="box-shadow: none; border-width: 0 0 2px 0; border-style: solid; border-color: #31ccec;"
    >
      <q-toolbar>
        <q-btn
          dense
          flat
          icon="menu"
          @click="toggleLeftDrawer"
          class="q-mr-sm"
        />
        <HeaderLogo :absoluteLeft="false"> </HeaderLogo>
        <!---<LoginContextButton> </LoginContextButton>-->
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      side="left"
      behavior="mobile"
      bordered
      :width="400"
      class="text-body1"
      dark
      style="box-shadow: 0 0 10px 5px gray"
    >
      <template v-if="planInfo.planName != undefined">
        <q-scroll-area style="height: calc(100% - 150px); margin-top: 150px">
          <q-list padding>
            <q-item>
              <q-item-section>
                <div class="row">
                  <div class="column col-10">
                    <q-text class="text-h5 q-pa-sm">
                      {{ planInfo.planName }}
                    </q-text>
                  </div>
                  <div class="column col-2">
                    <ForkButton :shortlink="this.$route.params.shortlink"></ForkButton>
                  </div>
                  <div class="column col-12">
                    <q-text class="text-body1 q-pa-sm">
                      {{ planInfo.planDescription }}
                    </q-text>
                  </div>
                </div>
              </q-item-section>
            </q-item>

            <q-separator class="q-my-lg" dark />

            <q-item>
              <q-item-section avatar class="q-ml-md">
                <q-icon name="clear_all" />
              </q-item-section>

              <q-item-section> Linien: </q-item-section>

              <q-item-section>
                {{ planInfo.currentNumberOfLines || 0 }}
              </q-item-section>
            </q-item>

            <q-item>
              <q-item-section avatar class="q-ml-md">
                <q-icon name="commit" />
              </q-item-section>

              <q-item-section> Haltestellen: </q-item-section>

              <q-item-section>
                {{ planInfo.currentNumberOfNodes || 0 }}
              </q-item-section>
            </q-item>

            <q-item>
              <q-item-section avatar class="q-ml-md">
                <q-icon name="polyline" />
              </q-item-section>

              <q-item-section> Verbindungen: </q-item-section>

              <q-item-section>
                {{ planInfo.currentNumberOfEdges || 0 }}
              </q-item-section>
            </q-item>

            <q-item>
              <q-item-section avatar class="q-ml-md">
                <q-icon name="text_fields" />
              </q-item-section>

              <q-item-section> Beschriftungen: </q-item-section>

              <q-item-section>
                {{ planInfo.currentNumberOfLabels || 0 }}
              </q-item-section>
            </q-item>

            <q-separator class="q-my-lg" dark />

            <q-item>
              <q-item-section>
                <div class="row">
                  <div class="col-xs-6">
                    <q-icon name="visibility" size="sm" class="q-mx-md">
                    </q-icon>
                    {{ planInfo.totalViewCount || 0 }}
                    <q-tooltip
                      class="bg-indigo text-body1"
                      anchor="top middle"
                      self="bottom middle"
                      style="white-space: nowrap"
                    >
                      Anzahl Aufrufe
                    </q-tooltip>
                  </div>
                  <div class="col-xs-6">
                    <q-icon name="favorite" size="sm" class="q-mx-md"> </q-icon>
                    {{ planInfo.likeCount || 0 }}
                    <q-tooltip
                      class="bg-green text-body1"
                      anchor="top middle"
                      self="bottom middle"
                      style="white-space: nowrap"
                    >
                      Anzahl Likes
                    </q-tooltip>
                  </div>
                </div>
              </q-item-section>
            </q-item>

            <q-separator class="q-mb-lg" dark />

            <q-item>
              <q-item-section>
                <div class="row">
                  <!--<div class="col-2">
                    <q-btn
                      icon="report"
                      color="red"
                      outline
                    ></q-btn>
                  </div>-->
                  <div class="col-6">
                    <q-btn
                      icon="favorite"
                      color="purple"
                      @click="toggleFavorite"
                      >Favorisieren</q-btn
                    >
                  </div>
                  <div class="col-6">
                    <q-btn icon="share" color="green" @click="copyLink"
                      >Link kopieren</q-btn
                    >
                  </div>
                </div>
              </q-item-section>
            </q-item>

            <!--<q-page-sticky position="bottom-left" :offset="[18, 18]">
              <q-fab
                v-model="fab2"
                label="Actions"
                external-label
                label-class="bg-grey-3 text-black text-body1"
                vertical-actions-align="left"
                color="primary"
                icon="keyboard_arrow_up"
                direction="up"
                persistent
              >
                <q-fab-action
                  label-class="bg-grey-3 text-black text-body1"
                  external-label
                  color="primary"
                  @click="onClick"
                  icon="share"
                  label="Email"
                />
                <q-fab-action
                  label-class="bg-grey-3 text-black text-body1"
                  external-label
                  color="positive"
                  @click="onClick"
                  icon="favorite"
                  label="Like"
                />
                <q-fab-action
                  label-class="bg-grey-3 text-black text-body1"
                  external-label
                  color="negative"
                  @click="onClick"
                  icon="report"
                  label="Report"
                />
              </q-fab>
            </q-page-sticky>-->
          </q-list>
        </q-scroll-area>

        <q-img
          class="absolute-top"
          style="height: 150px; border-bottom: 2px solid gray"
        >
          <div class="absolute-bottom">
            <div class="row q-pt-md">
              <div class="col-xs-6">
                Plan erstellt von:
                <div class="text-weight-bold text-h6">
                  {{ planInfo.planOwner?.displayName || "unbekannt" }}
                </div>
              </div>
              <div class="col-xs-grow"></div>
              <div class="col-shrink">
                <q-btn
                  flat
                  round
                  :to="'/users/' + planInfo.planOwner?._id"
                  :disable="planInfo.planOwner == undefined"
                >
                  <q-avatar size="72px" class="q-mb-sm">
                    <img
                      :src="
                        planInfo.planOwner?.profilePicture ||
                        'https://source.boringavatars.com/pixel/72/' +
                          planInfo.planOwner?._id +
                          '?colors=66f873,5a3dcf,99848a'
                      "
                    />
                  </q-avatar>
                </q-btn>
              </div>
            </div>

            <div class="row">
              <div class="col-xs-6">
                <q-icon name="auto_awesome" size="xs" class="q-mx-md" />
                {{ planInfo?.createdAt.slice(0, 10) || "-" }}
                <q-tooltip class="bg-positive text-body1" :offset="[0, 35]">
                  Erstellt am
                </q-tooltip>
              </div>
              <div class="col-xs-6">
                <q-icon name="edit" size="xs" class="q-mx-md" />
                {{ planInfo?.lastModifiedAt.slice(0, 10) || "-" }}
                <q-tooltip class="bg-secondary text-body1" :offset="[0, 35]">
                  Zuletzt bearbeitet am
                </q-tooltip>
              </div>
            </div>
          </div>
        </q-img>
      </template>
      <template v-else>
        <q-inner-loading
          :showing="true"
          label="Plandaten werden geladen..."
          label-class="text-white"
          class="bg-primary"
          style="border: 3px solid #fff5; border-radius: 10px"
          label-style="font-size: 1em"
          color="white"
          size="1em"
        />
      </template>
    </q-drawer>

    <q-page-container>
      <PlanViewer :planName="planName"></PlanViewer>
    </q-page-container>
  </q-layout>
</template>

<script>
// import { toRaw, ref } from 'vue'
import { ref } from 'vue'
import PlanViewer from 'src/pages/PlanViewer.vue'
import HeaderLogo from 'src/components/HeaderLogo.vue'
import { usePlanViewerStore } from 'src/stores/viewer_store'
import ForkButton from 'src/components/ForkButton.vue'

const planViewerStore = usePlanViewerStore()

export default {
  name: 'ViewerLayout',
  setup () {
    const leftDrawerOpen = ref(false)
    const planInfo = ref({})
    const shortlink = ref('')

    return {
      leftDrawerOpen,
      toggleLeftDrawer () {
        console.log('Toggling left drawre open!')
        console.log(leftDrawerOpen.value)
        leftDrawerOpen.value = !leftDrawerOpen.value
        console.log(leftDrawerOpen.value)
      },
      planInfo,
      shortlink
    }
  },
  created: async function () {
    this.shortlink = this.$route.params.shortlink

    await planViewerStore.getPlanInfo(this.shortlink)

    this.planInfo = planViewerStore.plans[this.shortlink].info
  },
  mounted () {},
  methods: {
    toggleFavorite: async function () {},
    copyLink: function () {
      navigator.clipboard.writeText(window.location)
    }
  },
  components: { PlanViewer, HeaderLogo, ForkButton }
}
</script>
