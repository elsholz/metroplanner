<template>
  <q-page
    padding
    style="background-color: #001"
    dark
    class="justify-center flex row items-center"
  >
    <div class="column col col-lg-8 col-md-10 col-sm-12 text-body1 text-center">
      <div class="row q-pt-md text-white text-justify">
        <div class="col-12">
          <DataProtectionDeclaration></DataProtectionDeclaration>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import DataProtectionDeclaration from 'src/components/DataProtectionDeclaration.vue'

export default {
  name: 'PrivacyPage',
  components: { DataProtectionDeclaration }
}
</script>
