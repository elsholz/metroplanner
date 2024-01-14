<template>
  <q-page class="doc-container flex justify-center bg-primary q-pb-xl" dark>
    <div v-if="plansCreated" class="row justify-center" style="width: 100%">
      <div class="column items-center justify-center col-12 text-white">
        <div class="text-h4 text-center q-mt-lg">
          Dein Profil
        </div>
          <hr color="white" width="200px;" />
      </div>
    </div>

    <div v-if="plansCreated" class="row justify-center" style="width: 100%">
      <div class="column col-xs-11 col-sm-8 text-white items-center">
        <div class="">
          <q-btn flat round @click="showProfilePictureDialog = true">
            <q-avatar size="196px" class="q-mb-sm">
              <img
                :src="
                  profilePicture ||
                  'https://source.boringavatars.com/pixel/72/' +
                    userId +
                    '?colors=66f873,5a3dcf,99848a'
                "
              />
            </q-avatar>
          </q-btn>
        </div>
        <div style="width: 300px">
          <q-menu v-model="showProfilePictureDialog" dark>
            <q-list style="width: 300px">
              <!---<q-item clickable class="text-info">-->
              <!--<q-icon name="upload" size="sm" class="q-py-xs q-pr-sm" />
                <q-item-section>Profilbild hochladen </q-item-section>-->
              <q-uploader
                dark
                style="max-width: 300px"
                url="http://localhost:4444/upload"
                label="Profilbild hochladen"
                accept=".jpg, .png, image/*"
                :filter="checkFileSize"
                @rejected="onRejected"
              />
              <!--</q-item>-->
              <q-separator />
              <q-item
                clickable
                v-close-popup
                class="text-red"
                v-if="profilePicture"
              >
                <q-icon name="delete" size="sm" class="q-py-xs q-pr-sm" />
                <q-item-section>Profilbild löschen </q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </div>
      </div>
    </div>
    <div v-if="plansCreated" class="row justify-center" style="width: 100%">
      <div class="column col-xs-6 col-sm-4 col-md-3 col-lg-2 text-white">
        <div class="q-my-sm">
          <q-input
            :oninput="changeProfile"
            dark
            color="white"
            rounded
            outlined
            v-model="displayName"
            label="Anzeigename"
            input-class="text-h6"
            input-style="text-align: center"
            :rules="[(val) => val.length <= 20 || 'Maximal 20 Zeichen erlaubt']"
          />
        </div>
      </div>
    </div>

    <div
      v-if="plansCreated"
      class="row justify-center q-mb-lg"
      style="width: 100%"
    >
      <div class="column col-xs-11 col-sm-8 col-md-6 text-white">
        <div>
          <q-input
            :oninput="changeProfile"
            color="white"
            dark
            v-model="bio"
            filled
            autogrow
            label="Profilbeschreibung"
            input-class="text-body1"
            :rules="[
              (val) => val.length <= 200 || 'Maximal 200 Zeichen erlaubt',
            ]"
          />
        </div>
      </div>
    </div>
    <q-btn dark color="green" v-if="profileChanged" animate>
      <div class="text-white text-body1">Profil speichern</div>
    </q-btn>

    <div v-if="plansCreated" class="row justify-center" style="width: 100%">
      <div class="column col-xs-10 text-white">
        <div class="text-h6 q-my-sm">Deine Pläne:</div>
        <q-card dark>
          <q-tabs
            dark
            v-model="tab"
            dense
            indicator-color="info"
            align="justify"
            style="background-color: #003"
          >
            <q-tab name="created" label="Erstellt" />
            <q-tab name="liked" label="Favorisiert" />
          </q-tabs>

          <q-separator />

          <q-tab-panels v-model="tab" animated dark class="bg-primary">
            <q-tab-panel name="created">
              <div class="text-h6">Erstellte Pläne</div>
              <q-list
                padding
                separator
                class="text-white"
                style="width: 100%"
                v-if="plansCreated?.length"
              >
                <PlanListItem
                  v-for="plan of plansCreated"
                  :key="plan"
                  :planShortlink="plan.planShortlink"
                  :planId="plan.planId"
                  style="width: 100%"
                >
                </PlanListItem>
              </q-list>
              <div v-else>Es wurden noch keine Pläne von dir erstellt.</div>
            </q-tab-panel>

            <q-tab-panel name="liked">
              <div class="text-h6">Favorisierte Pläne</div>
              <q-list
                padding
                separator
                class="text-white"
                style="width: 100%"
                v-if="plansLiked?.length"
              >
                <PlanListItem
                  v-for="shortlink of plansLiked"
                  :key="shortlink"
                  :planShortlink="shortlink"
                  style="width: 100%"
                >
                </PlanListItem>
              </q-list>
              <div v-else>Es wurden noch keine Pläne von dir favorisiert.</div>
            </q-tab-panel>
          </q-tab-panels>
        </q-card>
      </div>
      <q-page-sticky position="bottom-right" :offset="[18, 18]">
        <q-btn fab icon="add" color="green" />
        <q-tooltip> Add new plan</q-tooltip>
      </q-page-sticky>
    </div>
    <div v-else>
      <q-inner-loading
        :showing="true"
        :label="planName || 'Dein Profil wird geladen'"
        label-class="text-white"
        class="bg-dark"
        label-style="font-size: 1.5em"
        color="white"
        size="7em"
      />
    </div>
  </q-page>
</template>

<script>
import { useAuth0 } from '@auth0/auth0-vue'
import axios from 'axios'
import PlanListItem from 'src/components/PlanListItem.vue'
import { ref } from 'vue'

const displayName = ref(undefined)
const bio = ref(undefined)
const plansCreated = ref([])
const plansLiked = ref([])
const profilePicture = ref('')
const userId = ref('')
const profileChanged = ref(false)
const showProfilePictureDialog = ref(false)

export default {
  name: 'MyProfilePage',
  setup () {
    function checkFileSize (files) {
      // check that file size is below 1 MB
      return files.filter((file) => file.size < 2 ** 20)
    }
    return {
      checkFileSize,
      displayName,
      bio,
      userId,
      profilePicture,
      plansCreated,
      profileChanged,
      plansLiked,
      showProfilePictureDialog,
      tab: ref('created')
    }
  },
  methods: {
    changeProfile: function () {
      console.log('Profile Changed!')
      this.profileChanged = true
    }
  },
  created: async function () {
    this.displayName = 'Hendrik'
    this.plansCreated = [
      {
        planId: '64031adae96fbf2d07a6a849',
        planShortlink: 'walsumbahn'
      }
    ]
    this.bio = 'Hendriks coole Bio'
    const { user, isAuthenticated, getAccessTokenSilently } = useAuth0()
    console.log(isAuthenticated, user)
    const token = await getAccessTokenSilently()
    await axios
      .get('/api/_user', { headers: { Authorization: `Bearer ${token}` } })
      .then((response) => {
        console.log('Response from user api:', response)
        this.displayName = 'Hendrik Test'
      })
      .catch(console.log)
  },
  components: { PlanListItem }
}
</script>
