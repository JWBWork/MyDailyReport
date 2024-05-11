import { Integration } from 'components/models';

export class Teams implements Integration {
  public name = 'Teams';
  public icon = 'fa-solid fa-user-group';
  public listCaption= 'Summarize your teams.';
  public authorized = false;
  public isLive = false;

  public initAuth() {
    console.log('Teams.initAuth()');
  }

  public logout() {
    console.log('Teams.logout()');
  }
}
