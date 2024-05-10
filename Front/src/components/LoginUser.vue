<template>
   <div class="row justify-center">
    <div class="col">
      <q-form @submit="LoginSubmit(email, password)" @reset="onReset" class="col-md-auto">
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
          :type="password_hidden ? 'password' : 'text'"
          :rules="rules.password"
          lazy-rules
        >
          <template v-slot:append>
            <q-icon
              :name="password_hidden ? 'visibility_off' : 'visibility'"
              class="cursor-pointer"
              @click="password_hidden = !password_hidden"
            />
          </template>
        </q-input>

        <q-btn label="Login" type="submit" color="primary" icon="login" />
        <q-btn label="Reset" type="reset" color="primary" flat />
      </q-form>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { userAuth } from 'boot/user-auth';

export default defineComponent({
  data() {
    return {
      email: '',
      password: '',
      password_hidden: true,
      rules: {
        email: [
          (v: string) => !!v || 'E-mail is required',
          (v: string) => /.+@.+\..+/.test(v) || 'E-mail must be valid'
        ],
        password: [
          (v: string) => !!v || 'Password is required',
          (v: string) => v.length >= 8 || 'Password must be at least 8 characters'
        ],
      },
    };
  },
  methods: {
    onReset() {
      this.email = '';
      this.password = '';
    },

    async LoginSubmit(email?: string, password?: string) {
      const _email: string = email || this.email;
      const _password: string = password || this.password;
      await userAuth
        .LoginUser(_email, _password)
        .then((response) => {
          console.log('login complete. ', response, userAuth);
          this.$router.go(0);
        })
        .catch((error) => {
          console.log(error);
        });
    },

  }
})
</script>
