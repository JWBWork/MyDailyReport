<template>
  <q-input
    label="Report Name"
    v-model="selected_report.name"
    class="full-width"
    >
      <template v-slot:prepend>
        <q-icon name="place" />
      </template>
      <template v-slot:append v-if="authorized">
        <q-btn @click="saveReport" :disable="!Boolean(selected_report.name)">
          <q-icon name="save"/>
        </q-btn>
        <q-btn-dropdown
          :disable="!Boolean(reports.length)"
        >
          <q-list>
            <q-item clickable v-ripple v-for="report in reports" v-bind:key="report.id" @click="selectReport(report)">
              <q-item-section avatar>
                <q-avatar icon="description" text-color="white" />
              </q-item-section>
              <q-item-section>
                <q-item-label>{{report.name}}</q-item-label>
                <q-item-label caption>February 22, 2016</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
      </template>
      <template v-slot:append v-else>
        <q-btn @click="goToLogin()">
          <q-chip outline square color="red" text-color="white" icon="lock">
            login to save your reports!
          </q-chip>
        </q-btn>
      </template>
    </q-input>
</template>

<script lang="ts">
import { Report, reports_api } from 'boot/reports';
import { userAuth } from 'boot/user-auth';

export default {
  name: 'ReportList',
  // props: {
  //   reports: Array as PropType<Report[]>,
  // },
  data() {
    return {
      // report_name: '',
      selected_report: {} as Report,
      reports: [] as Report[],
      authorized: true,
    };
  },
  mounted() {
    this.refreshReports();
    console.log('ReportList mounted');
  },
  methods: {
    setReport(report: Report) {
      console.log('setReport', report);
      this.selected_report = report;
    },
    selectReport(report: Report) {
      if (report.id != this.selected_report.id) {
        this.setReport(report);
        this.$emit('selectReport', report);
      } else {
        console.log('report already selected');
      }
    },
    saveReport() {
      this.$emit('saveReport', this.selected_report.name)
    },
    async refreshReports() {
      if (userAuth.isLoggedIn()) {
        var reports: Report[] = await reports_api.getReports();
        this.reports = reports;
        this.authorized = true;
      } else {
        this.authorized = false;
        var reports: Report[] = [];
      }
      return reports;
    },
    async goToLogin() {
      this.$router.push({path: '/user'});
    },
  }
};
</script>

<style>
</style>
