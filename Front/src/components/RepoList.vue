<template>

  <q-select padding
    filled
    v-model="repo"
    :options="repos"
    stack-label
    map-options
    label="Repo"
    option-label="name"
    :display-value="`Repo: ${repo ? repo.name : ' ... '}`"
  >

  <template v-slot:append>
      <q-icon
        v-if="repo !== null"
        class="cursor-pointer"
        name="clear"
        @click.stop.prevent="repo = null"
      />
    </template>
  </q-select>
  <!-- <q-list padding>
    <repo-list-item />
  </q-list> -->
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import RepoListItem from 'components/RepoListItem.vue';
import { Github, Repo } from '../backend/integrations/github';
import {ref} from 'vue'

export default defineComponent({
  name: 'RepoList',
  exposes: ['repo'],
  props: {
    github: {
      type: Github,
      required: true
    },
    // repos: {
    //   type: Array as () => Repo[],
    //   required: true
    // },
    loading: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  components: {
  },
  data () {
    return {
      // repo: null as Repo | null,
      repos: [] as Repo[],
    }
  },
  setup() {
    const repo = ref<Repo | null>(null);

    return {
      repo,
    };
  },
  watch: {
    github: {
      immediate: true,
      deep: true,
      async handler() {
        if (this.github.authorized && this.repos.length == 0) {
          this.repos = await this.github.getRepos();
        }
      },
    },
  },
})
</script>
