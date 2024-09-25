<template>
  <div class="row items-top">
    <div class="col">
      <q-expansion-item
        expand-icon-toggle
        expand-separator
        group="commits"
        :label="commit.message"
      >
        <template v-slot:header>
          <q-item-section avatar class="col-2 q-mr-md">
            <div class="row no-wrap items-center">
              <q-checkbox
                size="xs"
                v-model="selected"
                @click="selectCommit"
                indeterminate-value="partial"
              />
              <q-avatar size="lg" icon="commit" text-color="white" />
              <q-badge color="yellow" floating class="q-ma-xs">
                {{ commit.token_cost }}
                <q-icon name="toll" color="white" class="q-ml-xs" />
              </q-badge>
            </div>
          </q-item-section>

          <q-item-section class="col">
            <span class="items-center text-caption">
              {{
                commit.message.length > 50
                  ? commit.message.substring(0, 50) + '...'
                  : commit.message
              }}
            </span>
          </q-item-section>
        </template>

        <q-item-section style="overflow-x: hidden">
          <br />
          <div class="row items-top" style="text-wrap: wrap; max-width: 100%">
            <div class="col-1 q-mr-md">
              <q-avatar size="lg" icon="chat_bubble" text-color="white" />
            </div>
            <div class="col-10">
              {{ commit.message }}
            </div>
          </div>
          <div class="row items-center q-mb-sm" style="max-width: 100%">
            <div class="col-1">
              <q-avatar size="md" icon="person" text-color="white" />
            </div>
            <div class="col-11 text-caption">
              {{ commit.author.name }}
            </div>
          </div>
          <div class="commit">
            <div v-for="file in commit.files" v-bind:key="file.raw_url">
              <q-separator />
              <q-item-label overline>
                <q-checkbox
                  size="xs"
                  v-model="file.selected"
                  @click="selectFile"
                />
                <q-icon :name="statusIcon(file.status)" />
                {{ file.filename }}
                <q-badge color="yellow" class="q-ma-xs">
                  {{ file.token_cost }}
                  <q-icon name="toll" color="white" class="q-ml-xs" />
                </q-badge>
              </q-item-label>
              <q-item-label caption class="patch" v-if="file.patch">
                {{ file.patch }}
              </q-item-label>
              <br />
            </div>
          </div>
        </q-item-section>

        <q-item-section bottom class="q-ma-sm">
          <div class="row justify-around">
            <div class="col-1 content-center">
              <q-icon name="today" />
            </div>
            <div class="col-11 content-center">
              <q-item-label caption>{{
                renderDate(commit.author.date)
              }}</q-item-label>
            </div>
          </div>
        </q-item-section>
      </q-expansion-item>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { Commit } from '../backend/integrations/github';
export default defineComponent({
  name: 'CommitListItem',
  props: {
    commit: {
      type: Object as () => Commit,
      required: true,
    },
  },
  data() {
    return {
      selected: false as string | boolean,
    };
  },
  methods: {
    statusIcon(status: string) {
      switch (status) {
        case 'added':
          return 'add';
        case 'modified':
          return 'edit';
        case 'removed':
          return 'delete';
        case 'renamed':
          return 'badge';
        default:
          return 'help';
      }
    },
    renderDate(date: string) {
      return new Date(date).toLocaleString();
    },
    selectCommit() {
      for (const file of this.commit.files) {
        file.selected = Boolean(this.selected);
      }
    },
    selectFile() {
      // check if all files are selected
      const allSelected = this.commit.files.every((file) => file.selected);
      const someSelected = this.commit.files.some((file) => file.selected);
      if (allSelected) {
        this.selected = true;
      } else if (someSelected) {
        this.selected = 'partial';
      } else {
        this.selected = false;
      }
    },
  },
  watch: {
    selected() {
      this.$emit('selected', this.selected, this.commit);
    },
  },
});
</script>

<style>
.commit {
  max-width: inherit;
  max-height: 300px;
  overflow-y: auto;
  scroll-behavior: smooth;
  flex-direction: column;
  -ms-overflow-style: none; /* Internet Explorer 10+ */
  scrollbar-width: none; /* Firefox */
}
.commit::-webkit-scrollbar {
  display: none; /* Safari and Chrome */
}

.patch {
  white-space: pre;
  max-width: 100%;
  overflow-x: auto;
}
</style>
