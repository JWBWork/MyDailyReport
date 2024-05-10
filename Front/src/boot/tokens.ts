import { userAuth } from './user-auth';

class Tokens {
  async getTokens() {
    console.log('Getting tokens');
    return userAuth.get('/tokens');
  }

  async beginCheckout(quantity: number) {
    console.log('Requesting checkout session');
    return userAuth.post('/tokens/begin-checkout', {
      quantity: quantity,
    });
  }

  async processCheckout(session_id: string) {
    console.log('Processing checkout session');
    return userAuth.post('/tokens/process-checkout', {
      session_id: session_id,
    });
  }
}

const tokens_api = new Tokens();

export { tokens_api };
