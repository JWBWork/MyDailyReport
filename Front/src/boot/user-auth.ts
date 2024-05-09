// import { boot } from 'quasar/wrappers';
import { client } from 'src/backend/api';
import { LocalStoreAttribute } from 'src/backend/local-store-attr';


class UserAuth {
  // TODO: move key definitions to a separate file so they're all in one place
  public authenticated = new LocalStoreAttribute('authenticated', false);
  public accessToken = new LocalStoreAttribute('accessToken', '');
  public userEmail = new LocalStoreAttribute('userEmail', '');

  constructor() {
    if (this.accessToken.get()) {
      this.getUser().catch((error) => {
        console.log('UserAuth constructor error', error);
        if (error.response.status === 401) {
          this.browserLogout();
        }
      }).then((response) => {
        console.log('UserAuth constructor user', response);
        return
      });
    }
  }

  _set_headers(config = {}) {
    if (this.accessToken.get()) {
      console.log('setting headers');
      config = {
        ...config,
        headers: {
          Authorization: `Bearer ${this.accessToken.get()}`,
        },
      };
    }
    return config;
  }

  post(url: string, data = {}, config = {}) {
    config = this._set_headers(config);
    console.log(config);
    return client.post(url, data, config);
  }

  get(url: string, config = {}) {
    config = this._set_headers(config);
    return client.get(url, config);
  }

  public async getUser() {
    return await this.get('/user/me').then((resp) => {
      console.log('user response', resp);
      return resp;
    });
  }

  public async RegisterUser(email: string, password: string) {
    console.log('Registering ...');
    return await this.post('/auth/register', {
      email: email,
      password: password,
    }).then((resp) => {
      console.log('register response', resp);
      return resp;
    });
  }

  public async LoginUser(email: string, password: string) {
    console.log('Logging in ...');
    return await this.post(
        '/auth/jwt/login',
        {
          username: email,
          password: password,
        },
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      )
      .then((resp) => {
        console.log('login response', resp);
        this.authenticated.set(true);
        this.accessToken.set(resp.data.access_token);
        this.userEmail.set(email);
        return resp;
      });
  }

  public async LogoutUser() {
    return await this.post('/auth/jwt/logout').then((resp) => {
      console.log('logout response', resp);
      this.browserLogout();
      return resp;
    }).catch((error) => {
      console.log('logout error', error);
      this.browserLogout();
      return error;
    })
  }

  async browserLogout() {
    this.authenticated.set(false);
    this.accessToken.set('');
  }

  async verifyUser(token: string) {
    return await this.post(
      '/auth/verify',
      { token: token }
    ).then((resp) => {
      console.log('verification response', resp);
      return resp;
    }).catch((error) => {
      console.log('verification error', error);
      return error;
    });
  }
}

const userAuth = new UserAuth();

// TODO: is this not implemented in my version of quasar?
// export default boot(({ app }) => {
//   app.config.globalProperties.$userAuth = userAuth;
// });

export { userAuth };
export { UserAuth };
