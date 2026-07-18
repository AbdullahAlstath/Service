/**
 * AFMS Chat Proxy — Cloudflare Worker
 * 
 * This tiny proxy sits between your GitHub Pages site and the Anthropic API.
 * It adds your API key server-side so it never appears in the browser.
 *
 * SETUP (takes ~5 minutes):
 *   1. Go to https://workers.cloudflare.com  →  sign up free
 *   2. Create a new Worker, paste this entire file
 *   3. Go to Worker Settings → Variables → add a Secret:
 *        Name:  ANTHROPIC_API_KEY
 *        Value: your key from https://console.anthropic.com
 *   4. Deploy the Worker — copy the *.workers.dev URL
 *   5. In index.html, set:
 *        const API_PROXY_URL = 'https://YOUR-WORKER.YOUR-NAME.workers.dev/chat';
 *   6. Push index.html to GitHub — done!
 */

// List of allowed origins (your GitHub Pages URL). Keep this tight.
const ALLOWED_ORIGINS = [
  // Add your GitHub Pages URL here, e.g.:
  // 'https://yourusername.github.io',
  // Also allow localhost for local testing:
  'http://localhost',
  'http://127.0.0.1',
  'null', // file:// opened locally
];

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';

    // Allow if origin matches list OR if list is empty (open — lock it down once working)
    const isAllowed = ALLOWED_ORIGINS.length === 0 ||
      ALLOWED_ORIGINS.some(o => origin === o || origin.startsWith(o));

    // CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': isAllowed ? origin : 'null',
          'Access-Control-Allow-Methods': 'POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
          'Access-Control-Max-Age': '86400',
        },
      });
    }

    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    if (!isAllowed) {
      return new Response('Forbidden', { status: 403 });
    }

    // Forward to Anthropic
    let body;
    try {
      body = await request.json();
    } catch {
      return new Response('Bad request', { status: 400 });
    }

    const anthropicResp = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
        'anthropic-beta': 'web-search-1', // enables web_search tool
      },
      body: JSON.stringify(body),
    });

    const data = await anthropicResp.json();

    return new Response(JSON.stringify(data), {
      status: anthropicResp.status,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': isAllowed ? origin : 'null',
      },
    });
  },
};
