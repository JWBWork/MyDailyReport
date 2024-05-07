import { boot } from 'quasar/wrappers'
import vue3GoogleLogin from 'vue3-google-login'

// TODO: implement eventually for future google auth
// "async" is optional;
// more info on params: https://v2.quasar.dev/quasar-cli/boot-files
export default boot(async ({ app }) => {
  console.log('google-auth boot file')
  app.use(vue3GoogleLogin, {
    clientId: process.env.GOOGLE_CLIENT_ID,
  })
  // something to do
})
