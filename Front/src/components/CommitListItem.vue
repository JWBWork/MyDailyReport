<template>
  <div class="row items-top">
    <div class="col q-mt-xs">
      <q-checkbox v-model="selected"/>
    </div>
    <div class="col-11">
      <q-expansion-item
        expand-icon-toggle
        expand-separator
        icon="commit"
        :label="commit.message"
      >
        <div class="commit">
          <div v-for="file in commit.files" v-bind:key="file.raw_url">
              <q-item-label overline>
                <q-icon :name="status_icon(file.status)"/> {{file.filename}}
              </q-item-label>
              <q-item-label lines=15 caption class="patch" v-if="file.patch">{{ file.patch }}</q-item-label>
              <br>
          </div>
        </div>

        <q-item-section bottom>
          <q-item-label caption>5 min ago</q-item-label>
        </q-item-section>
      </q-expansion-item>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { Commit } from '../backend/integrations/github';
export default defineComponent({
  name: 'CommitListItem',
  props: {
    commit: {
      type: Object as () => Commit,
      required: true
    }
  },
  data() {
    return {
      selected: false,
    }
  },
  methods: {
    status_icon(status: string) {
      switch (status) {
        case 'added':
          return 'add'
        case 'modified':
          return 'edit'
        case 'removed':
          return 'delete'
        case 'renamed':
          return 'badge'
        default:
          return 'help'
      }
    }
  },
  watch: {
    selected() {
      this.$emit('selected', this.selected, this.commit)
    }
  }
})
</script>

<style>
.commit {
  max-height: 300px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  scroll-behavior: smooth;

  -ms-overflow-style: none;  /* Internet Explorer 10+ */
  scrollbar-width: none;  /* Firefox */
}
.commit::-webkit-scrollbar {
    display: none;  /* Safari and Chrome */
}

.patch {
  white-space: pre;
}
</style>
