<template>
  <q-item clickable q-pa-md @click="initAuth" :disable="!integration.isLive">
    <!-- href="https://github.com/login/oauth/authorize?client_id=Iv1.c4bad3fa63a2e3a5&state=XuM7zEvakLsvH3zo4oCGshwchTtY7l" -->
    <!-- href="https://github.com/login/oauth/authorize?response_type=code&client_id=Iv1.c4bad3fa63a2e3a5&redirect_uri=https%3A%2F%2F127.0.0.1%3A9000&state=XuM7zEvakLsvH3zo4oCGshwchTtY7l" -->
    <q-item-section top avatar>
      <q-icon :name="integration.icon" color="white" class="q-pt-sm"/>
    </q-item-section>

    <q-item-section>
      <q-item-label>{{ integration.name }}</q-item-label>
      <q-item-label caption>{{ integration.listCaption }}</q-item-label>
    </q-item-section>

    <q-item-section side v-if="integration.isLive">
      <q-btn v-if="authorized" icon="logout" @click.stop="logout()" />
      <q-badge color="red" v-else>
        <q-icon name="warning" size="14px" />
      </q-badge>
    </q-item-section>
    <q-item-section side v-else>
      <q-chip color="accent" text-color="white" label="coming soon!" class="text-caption"/>
    </q-item-section>
  </q-item>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { Integration } from 'components/models';
// import { callbackify } from 'util';

export default defineComponent({
  props: {
    integration: {
      type: Object as () => Integration,
      required: true,
    },
  },
  data() {
    return {
      authorized: false,
    };
  },
  setup(props) {
    // console.log(props.integration)
    if (localStorage.getItem('awaitingAuth') == props.integration.name) {
      // props.integration.grabParams();
      props.integration.finalizeAuth();
    }

    return {
      // TODO: change this to pull from an injected integration model
      // icon: "fa-brands fa-github-alt",
      // name: "GitHub",
      // caption: "Summarize your commits."
    };
  },
  methods: {
    initAuth() {
      this.integration.initAuth();
    },
    logout() {
      console.log('logout');
      this.integration.logout();
    },
  },
  watch: {
    integration: {
      immediate: true,
      deep: true,
      handler() {
        this.authorized = this.integration.authorized;
      },
    },
  },
});
</script>
