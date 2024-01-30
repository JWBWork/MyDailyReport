<template>
  <q-editor
    v-model="editor"
    :placeholder="placeholder"
    min-height="5rem"
    height="85vh"
    :readonly="readonly"
  />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
  props: {
    new_summary: String,
    readonly: {
      type: Boolean,
      default: false
    }
  },
  setup() {
    const editor = ''
    return { editor }
  },
  data () {
    return {
      placeholder: '...'
    }
  },
  watch: {
    new_summary: {
      immediate: true,
      handler (val) {
        if (val === this.editor) {
          return
        } else if (!val) {
          console.log('new_summary is empty')
          this.editor = ''
        } else {
          // TODO: move pre to style?
          this.editor = `<pre>${val}</pre>`
        }
      }
    },
  }
})
</script>
