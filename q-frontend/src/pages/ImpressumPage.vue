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
        <div class="col-12 q-py-sm">Angaben gemäß §5 TMG:<br /></div>
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
        <div class="col-12 q-mt-md">
          <div class="text-weight-thin">Böckersche Straße 9</div>
          <div class="text-weight-thin">46487 Wesel</div>
        </div>
      </div>

      <div class="q-mt-lg row justify-center">
        <div class="column">
          <q-btn outline no-wrap no-caps to="/project" color="green" class="text-bold text-h6">
            Über das Projekt
          </q-btn>
        </div>
      </div>

      <div class="row text-white q-my-lg">
        <div class="col">
          <div class="q-my-sm">Kontakt:</div>
          <q-btn
            outline
            icon="mail"
            label="hdk.lks@pm.me"
            href="mailto:hdk.lks@pm.me"
            class="text-h6 text-mono"
          ></q-btn>
        </div>
      </div>

      <div class="row text-white justify-center">
        <div class="column col-12 col-sm-6 q-mt-lg">
          <span class=""
            >Umsatzsteueridentifikationsnummer gemäß § 27 a
            Umsatzsteuergesetz:</span
          >
          <div class="text-weight-thin">D E 3 4 8 5 9 4 6 4 5</div>
        </div>
      </div>

      <div class="row text-white q-mt-lg">
        <div class="col-12 q-py-md">
          <q-btn flat to="/privacy" color="info"> Datenschutzerklärung </q-btn>
        </div>
        <div class="col-12 q-py-md q-pb-xl">
          <q-btn flat to="/liability" color="info"> Haftungsausschluss </q-btn>
        </div>
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
