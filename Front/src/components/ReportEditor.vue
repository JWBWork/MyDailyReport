<template>
  <q-editor
    v-model="content"
    :placeholder="placeholder"
    min-height="5rem"
    height="85vh"
    :readonly="readonly"
    :content-class="{'line-break': 'pre',}"
  />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
  props: {
    readonly: {
      type: Boolean,
      default: false
    }
  },
  setup() {
    const content = ''
    return { content }
  },
  data () {
    return {
      placeholder: '...'
    }
  },
})
</script>
