import { client } from '../api';
import { Integration } from 'components/models';
import randomString from 'random-string';
import { ref } from 'vue';
import qs from 'qs';
import { userAuth } from 'boot/user-auth';
import { Report } from 'boot/reports';

export class CommitFile {
  public filename: string;
  public additions: number;
  public deletions: number;
  public changes: number;
  public status: string;
  public raw_url: string;
  public patch: string;

  constructor(apiCommitFileObject: any) {
    this.filename = apiCommitFileObject.filename;
    this.additions = apiCommitFileObject.additions;
    this.deletions = apiCommitFileObject.deletions;
    this.changes = apiCommitFileObject.changes;
    this.status = apiCommitFileObject.status;
    this.raw_url = apiCommitFileObject.raw_url;
    this.patch = apiCommitFileObject.patch;
  }
}

export class Commit {
  public additions: number;
  public changes: number;
  public deletions: number;
  public message: string;
  public filename: string;
  public patch: string;
  public raw_url: string;
  public sha: string;
  public status: string;
  public files: CommitFile[];

  constructor(apiCommitObject: any) {
    this.sha = apiCommitObject.sha;
    this.message = apiCommitObject.message;
    this.additions = apiCommitObject.additions;
    this.changes = apiCommitObject.changes;
    this.deletions = apiCommitObject.deletions;
    this.filename = apiCommitObject.filename;
    this.patch = apiCommitObject.patch;
    this.raw_url = apiCommitObject.raw_url;
    this.status = apiCommitObject.status;

    this.files = apiCommitObject.files.map((file: any) => {
      return new CommitFile(file);
    });
  }
}

export class Repo {
  public id: number;
  public name: string;
  public html_url: string;
  public commits: Commit[];

  constructor(apiRepoObject: any) {
    this.id = apiRepoObject.id;
    this.name = apiRepoObject.name;
    this.html_url = apiRepoObject.html_url;
    this.commits = [];
  }

  // TODO: Remove? Haven't been using ...
  //  Should I move commit requests to here?
  setCommits(commits: Commit[]) {
    this.commits = commits;
  }
}

export class Github implements Integration {
  public name = 'GitHub';
  public icon = 'fa-brands fa-github-alt';
  public listCaption = 'Summarize your commits.';
  public authorized = false;

  public stateKey = 'githubState';
  public codeKey = 'githubCode';
  public tokenKey = 'githubToken';

  public login = ref<string | null>(null);
  public avatar_url = ref<string | null>(null);

  public repos = ref<Repo[]>([]);

  constructor() {
    const state = localStorage.getItem(this.stateKey);
    if (!state) {
      this.setStateString();
    }

    const token = this.getToken();
    console.log('token:', token);
    // if (token) {
    if (token && this.validateToken(token)) {
      console.log('token is valid');
      this.authorized = true;
      this.updateBackendToken(token).then(() => {
        this.updateUserInfo();
      });
    } else if (token) {
      console.log('token is invalid');
      this.refreshToken(token);
    }
  }

  setStateString() {
    const state = randomString({ length: 20 });
    localStorage.setItem(this.stateKey, state);
  }

  setToken(token: object) {
    localStorage.setItem(this.tokenKey, JSON.stringify(token));
  }

  getToken() {
    const tokenString = localStorage.getItem(this.tokenKey);
    if (tokenString) {
      const token = JSON.parse(tokenString);
      return token;
    }
  }

  clearToken() {
    localStorage.removeItem(this.tokenKey);
  }

  validateToken(token: any) {
    return Date.now() < token.timestamp + token.expires_in * 1000
  }

  async refreshToken(token: any) {
    const new_token = await client
      .get('/integrations/github/refresh', {
        params: {
          refresh_token: token.refresh_token,
        },
      })
      .then((resp) => {
        const token = resp.data;
        token.timestamp = Date.now();
        this.setToken(token);
        this.authorized = true;
        return token;
      })
      .catch((error) => {
        this.clearToken()
        throw new Error(error);
      });
    console.log('token refreshed:', new_token);
  }

  async grabParams() {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    // TODO: figure out what to do with state
    const state = urlParams.get('state');

    if (code) {
      await this.processGithubCode(code);
      await this.getRepos();
    }

    localStorage.removeItem('awaitingAuth');
    this.authorized = true;
  }

  async initAuth() {
    localStorage.setItem('awaitingAuth', this.name);
    window.location.href =
      'https://github.com/login/oauth/authorize' +
      '?client_id=Iv1.c4bad3fa63a2e3a5' +
      `&state=${localStorage.getItem(this.stateKey)}`;
  }

  async logout() {
    console.log(`logging ${this.login.value} out of github`);
    client.post(
      '/integrations/github/logout',
      {
        login: this.login.value
      }
    )
    this.clearToken();
    this.authorized = false;
    this.login.value = null;
    this.avatar_url.value = null;
  }

  async processGithubCode(code: string) {
    await client
      .get('/integrations/github', {
        params: {
          code: code,
        },
      })
      .then((resp) => {
        const token = resp.data;
        token.timestamp = Date.now();
        this.setToken(token);
        this.authorized = true;
        console.log(`authorized: ${this.authorized}`);
        this.updateUserInfo()
      })
      .catch((error) => {
        const statusCode = error.response ? error.response.status : null;
        console.error('auth error:', error);
        // We will handle locally
        // When it's a 404 error, else handle globally
        if (statusCode === 498) {
          this.authorized = false;
          // Do some specific error handling logic for this request
          // For example: show the user a paywall to upgrade
          //  their subscription in order to view achieves
        } else {
          this.authorized = false;
          error.handleGlobally && error.handleGlobally();
        }
        throw error;
      });
  }

  async updateBackendToken(token: any) {
    console.log('updating backend token', token);
    await client
      .post('/integrations/github/update', token)
      .then((resp) => {
        console.log('token updated successfully', resp);
      })
      .catch((error) => {
        throw new Error(error);
      });
  }

  async getUser() {
    const user = await client
      .get('/integrations/github/user')
      .then((resp) => {
        return resp.data;
      })
      .catch((error) => {
        throw new Error(error);
      });
    return user;
  }

  async updateUserInfo() {
    this.getUser()
      .then((resp) => {
        this.login.value = resp.login;
        this.avatar_url.value = resp.avatar_url;
        this.authorized = true;
        console.log('User info retrieved successfully');
      })
      .catch((error) => {
        this.authorized = false;
        throw error
      })
      .finally(() => {
        //  python's 'pass' kwyword equivalent for typescript
        void 0;
      });
  }

  async getRepos(): Promise<Repo[]> {
    // TODO: remove token? not used in backend, saved in backend after auth
    const token = this.getToken();
    if (!token) {
      throw new Error('No token found');
    }
    const repos = await client
      .get('/integrations/github/repos')
      .then((resp) => {
        return resp.data;
      })
      .catch((error) => {
        throw new Error(error);
      });
    return repos.map((repo: any) => {
      return new Repo(repo);
    });
  }

  async getCommits(repo: Repo): Promise<Commit[]>  {
    const token = this.getToken();
    if (!token) {
      throw new Error('No token found');
    }
    const _commits = await client
      .get(`/integrations/github/repos/${repo.name}/commits`, {
        params: {
          // access_token: token.access_token,
          owner: this.login.value,
        },
      })
      .then((resp) => {
        return resp.data;
      })
      .catch((error) => {
        throw new Error(error);
      });
    repo.commits = _commits.map((commit: any) => {
      return new Commit(commit);
    });
    console.log('repo.commits:', repo.commits);
    return repo.commits
  }

  async getReport(repo: Repo, commits: Commit[])  {
    const token = this.getToken();
    if (!token) {
      throw new Error('No token found');
    }
    const commit_shas = commits.map((commit) => {
      return commit.sha;
    });
    console.log('requesting summary for commits:', commit_shas);
    // TODO: remove client with the user auth class? or move this to reports_api?
    return await client
      .get(`/integrations/github/report/${this.login.value}/${repo.name}`, {
        params: {
          commit_shas: commit_shas,
        },
        headers: {
          Authorization: `Bearer ${userAuth.accessToken.get()}`,
        },
        paramsSerializer: params => {
          return qs.stringify(params, { arrayFormat: 'repeat'})
        }
      })
      .then((resp) => {
        console.log('summary response:', resp);
        return new Report(null, resp.data.report.name, resp.data.report.content);
      })
      .catch((error) => {
        // UI should respond to this error
        throw error;
      });
  }
}
