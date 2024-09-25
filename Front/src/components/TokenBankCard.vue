<template>
  <div class="row justify-center no-wrap">
      <q-card class="col-12 q-ma-md">
        <q-item class="q-ma-sm">
          <q-item-section avatar>
            <q-avatar
              size="100px"
              font-size="70px"
              color="primary"
              text-color="white"
              icon="savings"
            />
          </q-item-section>

          <q-item-section>
            <q-item-label class="text-h4">Token Bank</q-item-label>
            <q-item-label caption>
              Tokens for generating reports, tokens consumed varies for size input data
            </q-item-label>
          </q-item-section>

        </q-item>
        <p :class="(tokenQuantity == 0 ? 'empty-bank' : '') + ' row justify-center'">You have {{ tokenQuantity }} tokens remaining!</p>
      </q-card>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { userAuth } from 'boot/user-auth';
import { tokens_api } from 'boot/tokens';

export default defineComponent({
  // name: 'ComponentName'
  data() {
    return {
      tokenQuantity: 0
    }
  },
  async created() {
    console.log('UserPage created');
    if (userAuth.authenticated.value) {
      tokens_api.getTokens().then((response) => {
        console.log('getTokens response', response);
        this.tokenQuantity = response.data.tokens;
      });
    }
  }
})
</script>
