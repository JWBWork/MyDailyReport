export class LocalStoreAttribute {
  public key: string;
  public value: string;
  public type: string;

  constructor(key: string, value: any) {
    this.key = key;
    this.type = typeof value;
    this.value = JSON.parse(localStorage.getItem(this.key) || 'null') || value;
  }

  public get() {
    // return JSON.parse(localStorage.getItem(this.key) || this.value)
    return JSON.parse(localStorage.getItem(this.key) || 'null');
  }

  public set(value: any) {
    localStorage.setItem(this.key, JSON.stringify(value));
    this.value = value;
    this.type = typeof value;
  }
}
