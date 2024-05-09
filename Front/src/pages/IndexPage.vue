<template>
  <q-page class="row justify-center q-pa-md">
    <div class="col-8">
      <div class="row q-my-xl">
        <div :class="$q.screen.gt.sm ? 'col-6' : 'col-12'">
          <h1 :class="$q.screen.gt.sm ? 'text-h1' : 'text-h3'">Welcome to<br/>MyDaily.Report</h1>
        </div>
        <div :class="$q.screen.gt.sm ? 'col-3 q-pr-sm q-pt-md' : 'col-6 q-pr-xl align-bottom'">
          <img src="/images/undraw_at_work_re_qotl.svg" :class="$q.screen.gt.sm ? 'header-art-desktop' : 'header-art-mobile'"/>
        </div>
        <div :class="$q.screen.gt.sm ? 'col-3 q-pl-xl q-pb-xl align-bottom' : 'col-6 q-pl-xl align-bottom'">
          <img src="/images/undraw_quitting_time_re_1whp.svg" :class="$q.screen.gt.sm ? 'header-art-desktop' : 'header-art-mobile'"/>
        </div>
      </div>
      <div class="column items-center">
        <p :class="$q.screen.gt.sm ? 'text-h3' : 'text-h5'">Summarize your day - Get on with your life!</p>
      </div>
      <q-separator class="q-mb-md"/>
      <div class="column items-center">
        <!-- <p>Unleash the Power of Your Productivity with Intelligent Summaries</p> -->
        <div class="row justify-center">
          <div class="col-6">
            <h3 class="row justify-center">Your Day, Distilled.</h3>
            <p>MyDaily.Report is not just another productivity tool; it's your personalized daily briefing, powered by cutting-edge language models. Transform your scattered workday data—from Git commits and emails to Slack messages—into insightful, actionable summaries.</p>
          </div>
          <div class="col-6">
            <div class="row justify-center">
              <img src="/images/undraw_software_engineer_re_tnjc.svg" class="header-art-desktop q-mt-xl"/>
            </div>
          </div>
        </div>
        <div class="row justify-center">
          <div class="col-6">
            <div class="row justify-center">
              <img src="/images/undraw_feeling_proud_qne1.svg" class="header-art-desktop q-mt-xl"/>
            </div>
          </div>
          <div class="col-6">
            <h3 class="row justify-center">How it Works</h3>
            <ol>
              <li>Connect seamlessly: Link your Git, email, and Slack accounts effortlessly. MyDaily.Report takes care of the rest.</li>
              <li>Intelligent Processing: Our advanced Language Model scans through your daily activities, identifying key patterns and significant events.</li>
              <li>Summaries that Matter: Receive concise, easy-to-digest summaries of your workday, highlighting accomplishments, potential roadblocks, and key interactions.</li>
            </ol>
          </div>
        </div>
        <h3>Why MyDaily.Report?</h3>
        <ul>
          <li>Effortless Insights: No more sifting through endless messages or commit logs. Get the highlights that matter, instantly.</li>
          <li>Data-Driven Productivity: Leverage AI to understand your work patterns, identify bottlenecks, and enhance your efficiency over time.</li>
          <li>Stay in the Loop: Be on top of your day without drowning in details. MyDaily.Report keeps you informed without overwhelming you.</li>
        </ul>
        <h4>Join Thousands Who've Elevated Their Workday</h4>
        <p>Ready to experience a smarter, more focused work life? Join the ranks of professionals who trust MyDaily.Report to streamline their daily workflow.</p>
        <q-btn
          label="Start Reporting"
          color="primary"
          size="lg"
          to="/reports"
          />
        <br/>
        <p class="small-print">MyDaily.Report respects your privacy. We prioritize security and data protection, ensuring your information remains confidential.</p>
      </div>
    </div>
</q-page>
</template>

<script lang="ts">

export default {
  name: 'IndexPage',
  components: {
  },
  setup() {
    return {
    };
  },
  data() {
    return {
    };
  },
  async mounted() {
    return
  },
  computed: {
  },
  watch: {
  },
  methods: {
  },
};
</script>

<style>
.small-print {
  font-size: 0.8em;
}

.align-bottom {
  display: flex;
  align-items: flex-end;
}

.header-art-desktop {
  max-width: 240px;
  max-height: 240px;
}

.header-art-mobile {
  max-width: 150px;
  max-height: 150px;
}
</style>
