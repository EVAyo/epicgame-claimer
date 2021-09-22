/* eslint-disable no-await-in-loop */
import 'source-map-support/register';
import { config, Account } from './common/config';
import './common/config2';
import L from './common/logger';
import Login from './login';
import FreeGames from './free-games';
import Purchase from './purchase';
import { newCookieJar } from './common/request';
import PuppetPurchase from './puppet/purchase';

export async function redeemAccount(account: Account, index: number): Promise<void> {
  await new Promise((resolve) => setTimeout(resolve, index * (config.intervalTime || 60) * 1000));
  L.info(`Checking free games for ${account.email} `);
  try {
    const requestClient = newCookieJar(account.email);
    const login = new Login(requestClient, account.email);
    const freeGames = new FreeGames(requestClient, account.email);
    const purchase = new Purchase(requestClient, account.email);
    const purchasePuppeteer = new PuppetPurchase(account.email);
    await login.fullLogin(account.email, account.password, account.totp); // Login
    const offers = await freeGames.getAllFreeGames(); // Get purchasable offers
    for (let i = 0; i < offers.length; i += 1) {
      // Async for-loop as running purchases in parallel may break
      L.info(`Purchasing ${offers[i].productName}`);
      let { puppeteerPurchase } = config;
      try {
        if (!puppeteerPurchase) {
          await purchase.purchase(offers[i].offerNamespace, offers[i].offerId);
        }
      } catch (err) {
        L.warn(err);
        L.warn('API purchase experienced an error, trying puppeteer purchase');
        puppeteerPurchase = true;
      }
      if (puppeteerPurchase) {
        await purchasePuppeteer.purchaseShort(offers[i].offerNamespace, offers[i].offerId);
      }
      L.info(`Done purchasing ${offers[i].productName}`);
    }
  } catch (e) {
    if (e.response) {
      if (e.response.body) L.error(e.response.body);
      else L.error(e.response);
    }
    L.error(e);
  }
}

export async function main(): Promise<void> {
  if (process.env.NODE_ENV !== 'test') {
    const accountPromises = config.accounts.map(redeemAccount);
    await Promise.all(accountPromises);
  }
}

main().catch((err) => L.error(err));
