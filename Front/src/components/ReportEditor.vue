<template>
  <q-editor
    v-model="content"
    :placeholder="placeholder"
    :readonly="readonly"
    :content-class="{'line-break': 'pre',}"
    style="overflow-y: scroll"
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
