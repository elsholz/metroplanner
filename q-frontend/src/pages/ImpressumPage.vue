<template>
  <q-page
    padding
    style="background-color: #001"
    dark
    class="justify-center flex row items-center"
  >
    <div class="column col col-lg-6 col-md-8 col-sm-12 text-body1 text-center">
      <div class="row q-pt-md text-white text-center">
        <div class="col-12">
          <h3>Impressum</h3>
        </div>
      </div>

      <div class="row text-white">
        <div class="col-12">Website wird betrieben von <br /></div>
      </div>
      <div class="row text-white">
        <div class="col-grow"></div>
        <div
          class="col-shrink q-mr-sm text-weight-bold text-h6"
          style="display: inline"
        >
          Hendrik Lankers
        </div>
        <div
          class="col-shrink q-mt-xs text-weight-thin"
          style="display: inline"
        >
          3D-Druck & Design
        </div>
        <div class="col-grow"></div>
      </div>

      <div class="row text-white">
        <div class="col-12">
          <q-avatar square size="350px" class="q-ma-sm">
            <img src="/images/profile_image.jpg" />
          </q-avatar>
        </div>
      </div>

      <div class="row text-white">
        <div class="col-12 q-mt-md">
          <span class="">Anschrift</span>
          <div class="text-weight-thin">Böckersche Straße 9</div>
          <div class="text-weight-thin">46487 Wesel</div>
        </div>
      </div>

      <div class="row text-white">
        <div class="col-12 q-mt-md">
          <span class="">Umsatzsteueridentifikationsnummer</span>
          <div class="text-weight-thin">...</div>
        </div>
      </div>

      <div class="row text-white q-mt-md">
        <div class="col-12">
          <span class="">Datenschutz und Privatsphäre</span>
          <div class="text-weight-thin">
            Hier steht die Datenschutzerklärung. Die ist natürlich
            sehr ausführlich und behandelt alle Fragen die eventuell auftauchen
            könnten.
          </div>
        </div>
      </div>

      <div class="row text-white q-my-xl">
        <div class="col">
          <div class="q-my-sm">Kontakt</div>
          <q-btn outline icon="mail" label="hdk.lks@pm.me" style="font-family: monospace; font-size: larger;"></q-btn></div>
      </div>
    </div>
  </q-page>
</template>

<script>
export default {
  setup () {
    return {}
  }
}
</script>
