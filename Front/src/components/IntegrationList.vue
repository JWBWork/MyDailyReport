<template>
  <q-expansion-item
    icon="fa-brands fa-github-alt"
    label="GitHub"
    overlay
  >
    <integration-list-item
      v-for="integration in integrations"
      :key="integration.name"
      :integration="integration"
    />
  </q-expansion-item>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { Integration } from 'components/models';
import IntegrationListItem from 'components/IntegrationListItem.vue'

export default defineComponent({
  props: {
    integrations: {
      type: Array as () => Integration[],
      required: true
    }
  },
  components: {
    IntegrationListItem
  },
  setup() {
    return {
    }
  }
  // name: 'IntegrationList'
})
</script>
