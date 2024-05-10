<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          <a href="/" class="headerLink">MyDaily.Report</a>
        </q-toolbar-title>

        <div>Quasar v{{ $q.version }}</div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      overlay
    >
      <q-list>
        <q-item-label header>
          Essential Links
        </q-item-label>

        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
      </q-list>

      <div class="absolute" style="top: 8px; right: -17px">
        <q-btn
          dense
          round
          unelevated
          color="primary"
          icon="chevron_left"
          @click="leftDrawerOpen = false"
        />
      </div>
    </q-drawer>

    <q-page-container>
      <router-view/>
    </q-page-container>
  </q-layout>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import EssentialLink from 'components/EssentialLink.vue';

const linksList = [
  {
    title: 'Home',
    caption: '',
    icon: 'flight_land',
    link: '/home'
  },
  {
    title: 'Reports',
    caption: 'Generate reports',
    icon: 'history_edu',
    link: '/reports'
  },
  {
    title: 'Github',
    caption: 'github.com/quasarframework',
    icon: 'star',
    link: 'https://github.com/quasarframework'
  },
  {
    title: 'User',
    caption: 'user page',
    icon: 'face',
    link: '/user'
  },
  {
    title: '404',
    caption: 'test 404',
    icon: 'question_mark',
    link: '/asdfasdfasd'
  }
];

export default defineComponent({
  name: 'MainLayout',

  components: {
    EssentialLink
  },

  setup() {
    // const drawerState = window.localStorage.getItem('drawerState');
    // const parsedDrawerState = drawerState !== null ? JSON.parse(JSON.parse(drawerState)) : false;
    // let leftDrawerOpen = ref(parsedDrawerState);
    let leftDrawerOpen = ref(false);

    return {
      essentialLinks: linksList,
      leftDrawerOpen,
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value
        // localStorage.setItem('drawerState', String(leftDrawerOpen.value))
      }
    }
  },
});
</script>

<style>
.headerLink {
  color: white;
  text-decoration: none;
}
</style>
