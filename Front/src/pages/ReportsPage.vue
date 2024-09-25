<template>
  <q-page class="col full-height row justify-center">
    <div class="col-3 q-py-sm">
      <div class="column justify-between full-height">
        <div class="col-auto">
          <TokenBankCard class="q-ma-sm" />
          <integration-list :integrations="integrations" class="q-mb-sm" />
          <!-- TODO: apply date range for query  -->
          <!-- <report-calendar /> -->
          <repo-list v-show="githubAuthorized" :github="github" :repos="repos" ref="repoSelect" />
        </div>
        <div
          class="col"
          style="overflow-y: scroll; max-width: 100%; max-height: 50vh"
        >
          <commit-list
            :github="github"
            :repo="selectedRepo"
            v-show="selectedRepo != null"
            @updatedCommitSelection="selectedCommits"
            ref="commitList"
          />
        </div>
        <div class="col-1 self-center full-width">
          <q-btn
            icon="history_edu"
            :loading="awaiting_summary"
            label="Summarize"
            class="full-width"
            @click="requestSummary()"
            :disabled="!commitsSelected || awaiting_summary"
          />
        </div>
      </div>
    </div>
    <div class="col-5 q-ma-sm full-height">
      <div class="col-1">
        <ReportList
          ref="reportList"
          @saveReport="saveReport"
          @selectReport="selectReport"
        />
      </div>
      <div class="col-8" style="overflow: scroll">
        <report-editor
          class="full-height"
          ref="reportEditor"
          :readonly="awaiting_summary"
          height="80vh"
        />
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
// import ReportCalendar from 'components/ReportCalendar.vue';
import IntegrationList from 'components/IntegrationList.vue';
import ReportEditor from 'components/ReportEditor.vue';
import RepoList from 'components/RepoList.vue';
import CommitList from 'components/CommitList.vue';
import ReportList from 'components/ReportList.vue';
// TODO: move to boot?
import { Github, Commit } from '../backend/integrations/github';
import { Slack } from '../backend/integrations/slack';
import { Teams } from '../backend/integrations/teams';
import { Gmail } from '../backend/integrations/gmail';
import { ref } from 'vue';
import { userAuth } from 'boot/user-auth';
import { Report, reports_api } from 'boot/reports';
import TokenBankCard from 'components/TokenBankCard.vue';

export default {
  name: 'IndexPage',
  components: {
    // ReportCalendar,
    IntegrationList,
    ReportEditor,
    RepoList,
    CommitList,
    ReportList,
    TokenBankCard,
  },
  setup() {
    // TODO: move to to IntegrationsList.vue
    const github = new Github();
    const repos = ref(github.repos);

    const slack = new Slack();
    const teams = new Teams();
    const gmail = new Gmail();

    var integrations = [github, slack, teams, gmail];
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
      awaiting_summary: false,
    };
  },
  async mounted() {
    this.mounted = true;
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
          await this.github
            .getReport(this.selectedRepo, commitList.selectedCommits)
            .then((report: Report) => {
              console.log('response', report);
              const report_list = this.$refs.reportList as any;
              report_list.setReport(report);
              this.updateEditorContent(report.content);
              this.awaiting_summary = false;
            })
            .catch((e) => {
              console.log(e);
              this.awaiting_summary = false;
              if (e.response.status == 401) {
                userAuth.LogoutUser();
                this.$q.notify({
                  type: 'negative',
                  message: 'Unauthorized - Please log in to generate reports!',
                });
                this.$router.push({ path: '/user' });
              } else {
                this.$q.notify({
                  type: 'negative',
                  message: 'Error',
                });
              }
            });
        }
      }
    },
    async saveReport(report_name: string) {
      const editor_element = this.$refs.reportEditor as any;
      const report_list = this.$refs.reportList as any;
      await reports_api.saveReport(report_name, editor_element.content);
      report_list.refreshReports();
    },
    async selectReport(report: Report) {
      this.updateEditorContent(report.content);
    },
    updateEditorContent(content: string) {
      const editor_element = this.$refs.reportEditor as any;
      editor_element.content = content.replace(/(?:\r\n|\r|\n)/g, '<br>');
      editor_element.$forceUpdate();
    },
  },
};
</script>
