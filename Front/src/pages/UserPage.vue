<template>
  <q-page class="col-10 q-pa-md content-center">
    <div class="row justify-center">
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
        <div class="row">
          <!-- Token bank and buy more tokens -->
          <div class="col-6 content-center">
            <div class="row justify-center">
              <q-card class="col-12 q-ma-md">
                <q-item>
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
                <p class="row justify-center">You have X tokens remaining!</p>
              </q-card>
            </div>
            <div class="row justify-around">
              <div class="col-5">
                <q-slider
                  v-model="creditRechargeForm.amount"
                  :min="creditRechargeForm.min"
                  :max="creditRechargeForm.max"
                  switch-label-side
                  class="q-ma-sm"
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
            <div class="row justify-around">
              <div class="col-3 q-ma-md">
                <p class="text-h4 q-ma-sm q-pt-sm">{{ rechargeCost }}</p>
              </div>
              <div class="col-7 q-ma-md">
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
          <!-- <q-card
            class="q-ma-lg col justify-center"
            v-for="plan in Subscriptions"
            :key="plan.name"
          >
            <q-img :src="plan.image" :ratio="3 / 4">
              <div class="absolute-bottom">
                <div class="text-h6">{{ plan.name }}</div>
                <div
                  class="text-subtitle2"
                  v-for="feature in plan.features"
                  :key="feature"
                >
                  {{ feature }}
                </div>
              </div>
            </q-img>

            <q-card-actions class="col justify-center">
              <q-btn @click="openStripeCheckout(plan.buyUrl)">
                <stripe-buy-button
                  :buy-button-id="plan.buyButtonId"
                  :publishable-key="publishableKey"
                  :customer-email="userAuth.userEmail.value"
                  style="pointer-events: none"
                />
              </q-btn>
            </q-card-actions>
          </q-card>
         -->
        </div>
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
// import { client } from '../backend/api';
import { userAuth } from 'boot/user-auth';
import { ref } from 'vue';
import RegisterUser from 'components/RegisterUser.vue';
import LoginUser from 'components/LoginUser.vue';

export default {
  name: 'UserPage',
  components: {
    RegisterUser,
    LoginUser,
  },
  async mounted() {
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
    const urlParams = new URLSearchParams(window.location.search);

    const checkoutSessionId = urlParams.get('checkout-session-id');
    if (checkoutSessionId) {
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
      // urlParams.delete('verification-token');
      // window.history.replaceState({}, '', '?' + urlParams.toString());
    }

    return {
      publishableKey: process.env.STRIPE_PUBLISHABLE_KEY,
      checkoutSessionId: checkoutSessionId,
      tab: 'login',
      email: '',
      password: '',
      creditRechargeForm: {
        min: 25,
        max: 500,
        amount: 100,
        costPerToken: 0.1,
      },
      // credits: {
      //   buyUrl: 'https://buy.stripe.com/test_14kdSBdTk0IxdlSaEG',
      //   buyButtonId: 'buy_btn_1PEb5KA8jMGv8c7QjRnIJWLX',
      // },
      // Subscriptions: [
      //   {
      //     name: 'Standard',
      //     priceVal: 4.99,
      //     features: [
      //       'Generate up to 5 reports per day',
      //       'Save up to 10 reports',
      //     ],
      //     buyButtonId: 'buy_btn_1OzisbA8jMGv8c7QrDkQuYy8',
      //     buyUrl: 'https://buy.stripe.com/test_00gaGpeXocrf81y9AA',
      //     image: '/images/paper.jpg',
      //   },
      //   {
      //     name: 'Unlimited',
      //     priceVal: 9.99,
      //     features: ['Generate unlimited reports', 'Save unlimited reports'],
      //     buyButtonId: 'buy_btn_1OzjGbA8jMGv8c7QdsKmT1vD',
      //     buyUrl: 'https://buy.stripe.com/test_4gw29T5mObnbgy46op',
      //     image: '/images/papers.jpg',
      //   },
      // ],
    };
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

    // openStripeCheckout(url: string) {
    //   window.location.replace(
    //     `${url}?prefilled_email=${userAuth.userEmail.value}`
    //   );
    // },

    openStripeCheckout() {
      console.log('recharge token checkout ...');
    },

    processStripeCheckout(checkoutSessionId: string) {
      // Create class for subs? move into userAuth?
      return userAuth
        .post('/subscriptions/checkout-session', {
          session_id: checkoutSessionId,
        })
        .then((response) => {
          console.log(response);
          return response;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

<style>
.small-print {
  font-size: 0.8em;
  color: grey;
}

.sub-card {
  width: 100%;
  max-width: 250px;
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
