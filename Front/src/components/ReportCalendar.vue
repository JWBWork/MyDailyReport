<template>
  <q-date
    v-model="date"
    landscape
  />
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'

export default defineComponent({
  // name: 'ReportCalendar'
  setup () {
    const date = ref(new Date())
    return { date }
  },
})
</script>
