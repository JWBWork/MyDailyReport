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
    repos: {
      type: Array as () => Repo[],
      required: true
    },
  },
  components: {
  },
  setup() {
    const repo = ref<Repo | null>(null);

    return {
      repo,
    };
  },
})
</script>
