import { Integration } from 'components/models';

export class Gmail implements Integration {
  public name = 'Gmail';
  public icon = 'fa-regular fa-envelope';
  public listCaption= 'Summarize your teams.';
  public authorized = false;
  public isLive = false;

  public initAuth() {
    console.log('Gmail.initAuth()');
  }

  public logout() {
    console.log('Gmail.logout()');
  }
}
