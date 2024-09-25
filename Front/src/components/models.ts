// TODO: rename this file to integrations.ts?

export interface Integration {
  name: string;
  authorized: boolean;
  icon: string;
  listCaption: string;
  isLive: boolean;

  // const checkAuth async;
  // auth(): any;
  initAuth(): any;
  // grabParams(): any;
  finalizeAuth(): any;
  logout(): any;
}
