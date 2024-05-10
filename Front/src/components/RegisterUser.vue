<template>
  <div class="row justify-center">
    <div class="col">
      <q-form @submit="RegisterSubmit" @reset="onReset" class="col-md-auto">
        <q-input
          v-model="email"
          class="q-ma-sm"
          outlined
          label="Email"
          :rules="rules.email"
        />

        <q-input
          v-model="password"
          class="q-ma-sm"
          outlined
          label="P*ssw*rd"
          ref="password"
          :type="password_hidden ? 'password' : 'text'"
          :rules="rules.password"
        >
          <template v-slot:append>
            <q-icon
              :name="password_hidden ? 'visibility_off' : 'visibility'"
              class="cursor-pointer"
              @click="password_hidden = !password_hidden"
            />
          </template>
        </q-input>

        <q-input
          v-model="password_confirm"
          class="q-ma-sm"
          outlined
          label="Confirm P*ssw*rd"
          ref="password_confirm"
          :type="password_hidden ? 'password' : 'text'"
          :rules="rules.password"
        >
          <template v-slot:append>
            <q-icon
              :name="password_hidden ? 'visibility_off' : 'visibility'"
              class="cursor-pointer"
              @click="password_hidden = !password_hidden"
            />
          </template>
        </q-input>

        <q-btn label="Register" type="submit" color="primary" icon="login" />
        <q-btn label="Reset" type="reset" color="primary" flat />
      </q-form>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { userAuth } from 'boot/user-auth';
import { QInput } from 'quasar';
// import { runSequentialPromises } from 'quasar';

export default defineComponent({
  data() {
    return {
      email: '',
      password: '',
      password_confirm: '',
      password_hidden: true,
      rules: {
        email: [
          (v: string) => !!v || 'E-mail is required',
          (v: string) => /.+@.+\..+/.test(v) || 'E-mail must be valid'
        ],
        password: [
          (v: string) => !!v || 'Password is required',
          (v: string) => v.length >= 8 || 'Password must be at least 8 characters',
          () => this.password === this.password_confirm || 'Passwords must match',
        ],
      },
    };
  },
  watch: {
    password() {
      (this.$refs.password as typeof QInput).validate();
      (this.$refs.password_confirm as typeof QInput).validate();
    },
    password_confirm() {
      (this.$refs.password as typeof QInput).validate();
      (this.$refs.password_confirm as typeof QInput).validate();
    },
  },
  methods: {
    onReset() {
      this.email = '';
      this.password = '';
      this.password_confirm = '';
    },

    async RegisterSubmit() {
      await userAuth
        .RegisterUser(this.email, this.password)
        .then((response) => {
          console.log(response);
          this.$emit('userRegistered', this.email, this.password);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
});
</script>
