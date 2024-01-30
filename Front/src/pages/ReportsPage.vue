<template>
  <q-page class="row justify-evenly q-pa-md">
    <div class="col-5 q-pa-sm">
      <integration-list :integrations="integrations" />

      <!-- TODO: apply date range for query  -->
      <!-- <report-calendar /> -->

      <!-- TODO: Some intermediate element to select integration specific elements -->
      <div v-show="githubAuthorized">
        <div class="col-10">
          <repo-list
            :github="github"
            :repos="repos"
            ref="repoSelect"
          />
          <commit-list
            :github="github"
            :repo="selectedRepo"
            v-show="selectedRepo != null"
            @updatedCommitSelection="selectedCommits"
            ref="commitList"
          />
        </div>
        <div class="col">
          <q-btn
            icon="history_edu"
            :loading="awaiting_summary"
            label="Summarize"
            class="full-width vertical-bottom	"
            @click="requestSummary()"
            :disabled="!commitsSelected || awaiting_summary"
          />
        </div>
      </div>
    </div>
    <div class="col q-pa-sm">
      <report-editor
        :new_summary="new_summary || ''"
        :readonly="awaiting_summary"
        />
    </div>
  </q-page>
</template>

<script lang="ts">
// import ReportCalendar from 'components/ReportCalendar.vue';
import IntegrationList from 'components/IntegrationList.vue';
import ReportEditor from 'components/ReportEditor.vue';
import RepoList from 'components/RepoList.vue';
import CommitList from 'components/CommitList.vue';
// import { Integration } from 'components/models';
// import { Github, Repo, Commit } from '../backend/integrations/github';
import { Github, Commit } from '../backend/integrations/github';
import { ref } from 'vue';

export default {
  name: 'IndexPage',
  components: {
    // ReportCalendar,
    IntegrationList,
    ReportEditor,
    RepoList,
    CommitList,
  },
  setup() {
    const github = new Github();
    const repos = ref(github.repos);

    var integrations = [github];
    return {
      github,
      integrations,
      repos,
    };
  },
  data() {
    return {
      mounted: false,
      githubAuthorized: false,
      commitsSelected: false,
      new_summary: null,
      awaiting_summary: false,
    };
  },
  async mounted() {
    this.mounted = true;
    // this.repos = await this.github.getRepos();
  },
  computed: {
    selectedRepo() {
      if (!this.mounted) {
        return null;
      } else {
        var repoList = this.$refs.repoSelect as typeof RepoList;
        if (repoList == null) {
          return null;
        } else {
          return repoList.repo;
        }
      }
    },
    noSelectedCommits() {
      const commitList = this.$refs.commitList as typeof CommitList;
      const result = !commitList || commitList.selectedCommits.length === 0;
      console.log('result', result);
      return result;
    },
  },
  watch: {
    github: {
      immediate: true,
      deep: true,
      async handler() {
        // if (this.github.authorized && this.repos.length == 0) {
        //   this.repos = await this.github.getRepos();
        // }
        this.githubAuthorized = this.github.authorized;
      },
    },
  },
  methods: {
    selectedCommits(selectedCommits: Commit[]) {
      if (selectedCommits) {
        this.commitsSelected = selectedCommits.length > 0;
      }
    },
    async requestSummary() {
      if (this.selectedRepo != null) {
        const commitList = this.$refs.commitList as typeof CommitList;
        if (commitList) {
          this.awaiting_summary = true;
          console.log('selectedCommits', commitList.selectedCommits);
          await this.github.getSummary(
            this.selectedRepo, commitList.selectedCommits
          )
          .then((response) => {
            console.log('response', response);
            this.new_summary = response.summary;
            this.awaiting_summary = false;
          })
          .catch((e) => {
            console.log('error', e);
            this.awaiting_summary = false;
          })
        }
      }
    },
  },
};
</script>
