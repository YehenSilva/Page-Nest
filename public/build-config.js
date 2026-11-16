// Runs on Vercel at build time: writes public/firebase-config.js from environment variables.
const fs = require('fs');
const e = process.env;
if (!e.FIREBASE_API_KEY) { console.error('Missing FIREBASE_API_KEY (set it in Vercel > Settings > Environment Variables)'); process.exit(1); }
const cfg = {
  apiKey: e.FIREBASE_API_KEY, authDomain: e.FIREBASE_AUTH_DOMAIN, projectId: e.FIREBASE_PROJECT_ID,
  storageBucket: e.FIREBASE_STORAGE_BUCKET, messagingSenderId: e.FIREBASE_SENDER_ID, appId: e.FIREBASE_APP_ID,
  appCheckKey: e.APP_CHECK_SITE_KEY || ''
};
fs.mkdirSync('public', { recursive: true });
fs.writeFileSync('public/firebase-config.js', 'window.FIREBASE_CONFIG = ' + JSON.stringify(cfg, null, 2) + ';\n');
console.log('firebase-config.js written');
