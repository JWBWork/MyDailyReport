export interface Integration {
  name: string;
  authorized: boolean;
  icon: string;
  listCaption: string;

  // const checkAuth async;
  // auth(): any;
  initAuth(): any;
  grabParams(): any;
}