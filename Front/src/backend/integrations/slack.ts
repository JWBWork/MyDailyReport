import { Integration } from 'components/models';

export class Slack implements Integration {
  public name = 'Slack';
  public icon = 'fa-brands fa-slack';
  public listCaption= 'Summarize your threads.';
  public authorized = false;
  public isLive = false;

  public initAuth() {
    console.log('Slack.initAuth()');
  }

  public finalizeAuth() {
    console.log('Slack.finalizeAuth()');
  }

  public logout() {
    console.log('Slack.logout()');
  }
}
