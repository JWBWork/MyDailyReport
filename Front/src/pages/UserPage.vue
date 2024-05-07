<template>
  <q-page class="columns q-pa-md">
    <div class="row justify-center">
      <div class="col-6" v-if="!authenticated">
        <q-tabs v-model="tab" active-color="primary" indicator-color="primary">
          <q-tab name="login" label="Login" />
          <q-tab name="register" label="Register" />
        </q-tabs>

        <q-input v-model="email" class="q-ma-sm" outlined label="Email" />
        <q-input
          v-model="password"
          class="q-ma-sm"
          outlined
          label="P*ssw*rd"
          :type="isPwd ? 'password' : 'text'"
        >
          <template v-slot:append>
            <q-icon
              :name="isPwd ? 'visibility_off' : 'visibility'"
              class="cursor-pointer"
              @click="isPwd = !isPwd"
            />
          </template>
        </q-input>
        <q-tab-panels v-model="tab">
          <q-tab-panel name="register">
            <q-form
              @submit="RegisterSubmit"
              @reset="onReset"
              class="col-md-auto"
            >
              <div>
                <q-btn
                  label="Register"
                  type="submit"
                  color="primary"
                  icon="login"
                />
                <q-btn
                  label="Reset"
                  type="reset"
                  color="primary"
                  flat
                  class="q-ml-sm"
                />
              </div>
            </q-form>
          </q-tab-panel>

          <q-tab-panel name="login">
            <q-form @submit="LoginSubmit" @reset="onReset" class="col-md-auto">
              <div>
                <q-btn
                  label="Login"
                  type="submit"
                  color="primary"
                  icon="login"
                />
                <q-btn
                  label="Reset"
                  type="reset"
                  color="primary"
                  flat
                  class="q-ml-sm"
                />
              </div>
            </q-form>
          </q-tab-panel>
        </q-tab-panels>
      </div>
      <div v-if="authenticated" class="col-6 justify-center q-ma-sm">
        <div class="row">
          <q-card
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
  </q-page>
</template>

<script lang="ts">
import { client } from '../backend/api';
import { userAuth } from 'boot/user-auth';
import { ref } from 'vue';

export default {
  name: 'UserPage',
  components: {},
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
      console.log('checkoutSessionId: ', checkoutSessionId, 'response: ', response);
      urlParams.delete('checkout-session-id');
      window.history.replaceState({}, '', '?' + urlParams.toString());
    }

    return {
      publishableKey: process.env.STRIPE_PUBLISHABLE_KEY,
      checkoutSessionId: checkoutSessionId,
      tab: 'login',
      email: '',
      password: '',
      Subscriptions: [
        {
          name: 'Standard',
          priceVal: 4.99,
          features: [
            'Generate up to 5 reports per day',
            'Save up to 10 reports',
          ],
          buyButtonId: 'buy_btn_1OzisbA8jMGv8c7QrDkQuYy8',
          buyUrl: 'https://buy.stripe.com/test_00gaGpeXocrf81y9AA',
          image: '/images/paper.jpg',
        },
        {
          name: 'Unlimited',
          priceVal: 9.99,
          features: ['Generate unlimited reports', 'Save unlimited reports'],
          buyButtonId: 'buy_btn_1OzjGbA8jMGv8c7QdsKmT1vD',
          buyUrl: 'https://buy.stripe.com/test_4gw29T5mObnbgy46op',
          image: '/images/papers.jpg',
        },
      ],
    };
  },
  computed: {
    authenticated() {
      return userAuth.authenticated.value;
    },
  },
  watch: {
    'userAuth.authenticated': function (val) {
      console.log('User Authenticated: ', val);
    },
  },
  methods: {
    onReset() {
      this.email = '';
      this.password = '';

      console.log(userAuth.authenticated);
      console.log(userAuth.accessToken);
    },
    RegisterSubmit() {
      userAuth
        .RegisterUser(this.email, this.password)
        .then((response) => {
          console.log(response);
          this.LoginSubmit();
        })
        .catch((error) => {
          console.log(error);
        });
    },

    LoginSubmit() {
      console.log('!!!!', this.email, this.password);
      userAuth
        .LoginUser(this.email, this.password)
        .then((response) => {
          console.log('login complete. ', response, userAuth);
          this.$router.go(0);
        })
        .catch((error) => {
          console.log(error);
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

    openStripeCheckout(url: string) {
      window.location.replace(
        `${url}?prefilled_email=${userAuth.userEmail.value}`
      );
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
</style>
