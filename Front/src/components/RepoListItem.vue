<template>
  <!-- TODO: delete? no longer used? -->
  <q-expansion-item
    icon="book"
    label="Repo name"
  >
    <q-item-section>
      <q-item-label overline>OVERLINE</q-item-label>
      <!-- move these to a repo-file-patch componenet that takes RepoFilePatch model -->
      <q-item-label>description? something something</q-item-label>
    </q-item-section>

    <q-item-section
      side
      top
    >
      <q-item-label caption>5 min ago</q-item-label>
    </q-item-section>
  </q-expansion-item>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
  // name: 'ComponentName'
})
</script>

<style></style>
