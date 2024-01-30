<template>
  <div v-if="loading" class="q-pa-md">
    <div class="q-gutter-md row">
      <q-spinner class="q-ma-auto"
          size="2em"
          :thickness="5"/>
    </div>
  </div>
  <q-list padding dense v-else-if="commits.length != null">
    <commit-list-item
      v-for="commit in commits"
      v-bind:key="commit.sha"
      :commit="commit"
      @selected="commitSelected"
    >
      <!-- {{commit.message}} -->
    </commit-list-item>
  </q-list>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import CommitListItem from 'components/CommitListItem.vue';
import {Github, Repo, Commit} from '../backend/integrations/github';
import {ref} from 'vue'

export default defineComponent({
  name: 'CommitList',
  components: {
    CommitListItem
  },
  expose: ['selectedCommits'],
  props: {
    github: {
      type: Github,
      required: true
    },
    repo: {
      type: Object as () => Repo | null,
      required: false
    },
  },
  data () {
    return {
      commits: ref([] as Commit[]),
      selectedCommits: ref([] as Commit[]),
      loading: false,
    }
  },
  watch: {
    repo: {
      immediate: true,
      async handler() {
        this.selectedCommits = []
        if (this.repo != null) {
          this.loading = true
          this.commits = await this.github.getCommits(this.repo)
          this.loading = false
        } else {
          this.commits = []
        }
      }
    }
  },
  methods: {
    commitSelected(selected: boolean, commit: Commit) {
      if (selected) {
        if (
          this.selectedCommits.find((c) => {
            // checking if already in list
            return c.sha === commit.sha
          })
        ) {
          return
        } else {
          this.selectedCommits.push(commit)
        }
      } else {
        this.selectedCommits = this.selectedCommits.filter((c) => {
          return c.sha !== commit.sha
        })
      }
      this.$emit('updatedCommitSelection', this.selectedCommits)
    }
  }
})
</script>
