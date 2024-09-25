<template>
  <q-page class="col-10 q-pa-md content-center">
    <div class="row justify-center no-wrap">
      <div class="col-6" v-if="!authenticated">
        <q-tabs v-model="tab" active-color="primary" indicator-color="primary">
          <q-tab name="login" label="Login" />
          <q-tab name="register" label="Register" />
        </q-tabs>

        <q-tab-panels v-model="tab">
          <!-- TODO: submit when pressing enter -->
          <q-tab-panel name="register">
            <RegisterUser @userRegistered="postRegisterLogin" />
          </q-tab-panel>

          <q-tab-panel name="login">
            <LoginUser ref="login" />
          </q-tab-panel>
        </q-tab-panels>
      </div>

      <div v-if="authenticated" class="col-7 q-pa-md">
        <div class="row no-wrap justify-center">
          <!-- Token bank and buy more tokens -->
          <div class="col-6 content-center">
            <TokenBankCard/>
            <div class="row justify-around no-wrap q-mt-sm">
              <div class="col-5">
                <q-slider
                  v-model="creditRechargeForm.amount"
                  :min="creditRechargeForm.min"
                  :max="creditRechargeForm.max"
                  switch-label-side
                  class="q-ma-sm"
                  :step="5"
                />
              </div>
              <div class="col-4">
                <q-chip icon="savings" class="q-ma-sm">
                  +
                  <q-input
                    type="number"
                    v-model="creditRechargeForm.amount"
                    borderless
                  ></q-input>
                </q-chip>
              </div>
            </div>
            <div class="row justify-around no-wrap">
              <div class="col-3 q-my-sm q-ml-xl">
                <p class="text-h4 q-ma-sm q-pt-sm">{{ rechargeCost }}</p>
              </div>
              <div class="col-6 q-my-sm q-mr-md">
                <q-btn
                  @click="openStripeCheckout"
                  color="primary"
                  label="Recharge Tokens"
                  icon="payment"
                  type="submit"
                  class="q-ma-md"
                />
              </div>
            </div>
          </div>
          <!-- User name and logout -->
          <div class="col-6 content-center">
            <div class="row justify-center">
              <q-avatar
                size="100px"
                font-size="40px"
                color="primary"
                text-color="white"
                icon="person"
              />
            </div>
            <div class="row justify-center q-my-md">
              <div class="text-h5">{{ userAuth.userEmail.value }}</div>
            </div>
            <div class="row justify-center">
              <q-btn
                color="primary"
                icon="logout"
                label="Log Out"
                @click="Logout"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
import { userAuth } from 'boot/user-auth';
import { tokens_api } from 'boot/tokens';
import { ref } from 'vue';
import RegisterUser from 'components/RegisterUser.vue';
import LoginUser from 'components/LoginUser.vue';
import TokenBankCard from 'components/TokenBankCard.vue';

export default {
  name: 'UserPage',
  components: {
    RegisterUser,
    LoginUser,
    TokenBankCard
  },
  async mounted() {
    // TODO: dead code - remove? might re-implement subscriptions eventually...
    let script = document.createElement('script');
    script.src = 'https://js.stripe.com/v3/buy-button.js';
    script.async = true;
    document.body.appendChild(script);
  },
  beforeUnmount() {
    return;
  },
  setup() {
    return {
      userAuth,
      isPwd: ref(true),
    };
  },
  data() {
    return {
      publishableKey: process.env.STRIPE_PUBLISHABLE_KEY,
      tab: 'login',
      email: '',
      password: '',
      creditRechargeForm: {
        min: 25,
        max: 500,
        amount: 100,
        costPerToken: 0.1,
      },
      // tokenQuantity: 0
    };
  },
  async created() {
    const urlParams = new URLSearchParams(window.location.search);

    const checkoutSessionId = urlParams.get('checkout-session-id');
    if (checkoutSessionId) {
      console.log('checkoutSessionId: ', checkoutSessionId);
      const response = this.processStripeCheckout(checkoutSessionId);
      console.log(
        'checkoutSessionId: ',
        checkoutSessionId,
        'response: ',
        response
      );
      urlParams.delete('checkout-session-id');
      window.history.replaceState({}, '', '?' + urlParams.toString());
    }

    const verificationToken = urlParams.get('verification-token');
    if (verificationToken) {
      userAuth.verifyUser(verificationToken);
      urlParams.delete('verification-token');
      window.history.replaceState({}, '', '?' + urlParams.toString());
    }

    // console.log('UserPage created');
    // if (userAuth.authenticated.value) {
    //   tokens_api.getTokens().then((response) => {
    //     console.log('getTokens response', response);
    //     this.tokenQuantity = response.data.tokens;
    //   });
    // }
  },
  computed: {
    authenticated() {
      return userAuth.authenticated.value;
    },
    rechargeCost() {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
      }).format(
        parseFloat(
          (
            this.creditRechargeForm.costPerToken *
            this.creditRechargeForm.amount
          ).toFixed(2)
        )
      );
    },
  },
  watch: {
    'userAuth.authenticated': function (val) {
      console.log('User Authenticated: ', val);
    },
    'creditRechargeForm.amount': function (val) {
      if (val === '' || val < this.creditRechargeForm.min) {
        this.creditRechargeForm.amount = this.creditRechargeForm.min;
      } else if (val > this.creditRechargeForm.max) {
        this.creditRechargeForm.amount = this.creditRechargeForm.max;
      }
    },
  },
  methods: {
    async postRegisterLogin(email: string, password: string) {
      this.tab = 'login';
      this.$nextTick(async () => {
        const response = await (
          this.$refs.login as typeof LoginUser
        ).LoginSubmit(email, password);
        console.log('postRegisterLogin response', response);
      });
    },

    Logout() {
      userAuth
        .LogoutUser()
        .then((response) => {
          console.log(response);
          this.$router.go(0);
        })
        .catch((error) => {
          console.log(error);
          this.$router.go(0);
        });
    },

    openStripeCheckout() {
      tokens_api.beginCheckout(this.creditRechargeForm.amount).then((response) => {
        window.location.replace(response.data.stripe_url);
      });
    },

    async processStripeCheckout(checkoutSessionId: string) {
      return await tokens_api.processCheckout(checkoutSessionId).then((response) => {
        console.log(response);
        return response;
      });
    },
  },
};
</script>

<style>
.empty-bank {
  color: red;
  text-decoration: underline;
  /* font-weight: bold; */
}

input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
input[type='number'] {
  -moz-appearance: textfield;
}
</style>
