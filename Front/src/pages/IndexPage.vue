<template>
  <q-page class="row justify-evenly q-pa-md">
    <div class="col-10">
      <div class="column items-center">
        <h1>Welcome to MyDaily.Report</h1>
        <p>Unleash the Power of Your Productivity with Intelligent Summaries</p>
        <h2>Your Day, Distilled.</h2>
        <p>MyDaily.Report is not just another productivity tool; it's your personalized daily briefing, powered by cutting-edge language models. Transform your scattered workday data—from Git commits and emails to Slack messages—into insightful, actionable summaries.</p>
        <h2>How it Works</h2>
        <ol>
          <li>Connect seamlessly: Link your Git, email, and Slack accounts effortlessly. MyDaily.Report takes care of the rest.</li>
          <li>Intelligent Processing: Our advanced Language Model scans through your daily activities, identifying key patterns and significant events.</li>
          <li>Summaries that Matter: Receive concise, easy-to-digest summaries of your workday, highlighting accomplishments, potential roadblocks, and key interactions.</li>
        </ol>
        <h2>Why MyDaily.Report?</h2>
        <ul>
          <li>Effortless Insights: No more sifting through endless messages or commit logs. Get the highlights that matter, instantly.</li>
          <li>Data-Driven Productivity: Leverage AI to understand your work patterns, identify bottlenecks, and enhance your efficiency over time.</li>
          <li>Stay in the Loop: Be on top of your day without drowning in details. MyDaily.Report keeps you informed without overwhelming you.</li>
        </ul>
        <h3>Join Thousands Who've Elevated Their Workday</h3>
        <p>Ready to experience a smarter, more focused work life? Join the ranks of professionals who trust MyDaily.Report to streamline their daily workflow.</p>
        <q-btn
          label="Start Reporting"
          color="primary"
          size="lg"
          to="/reports"
          />
        <br/>
        <p class="small-print">Note: MyDaily.Report respects your privacy. We prioritize security and data protection, ensuring your information remains confidential.</p>
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
  color: grey;
}
</style>
