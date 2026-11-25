# NextByt social media playbook

Claude makes and publishes every NextByt post. Rishitha does not make posts.

## Accounts (Buffer org "My organization", id 6b0719186a77081e39833051, free plan: 10 queued posts per channel)
- Facebook page "NextByt Digital Studio": 6b071a7b8541f09ecba05605 (metadata.facebook.type post / reel)
- Instagram @nextbyt_web: 6b071add8541f09ecba05a2c (metadata.instagram.type post / reel, shouldShareToFeed true)
- TikTok @nextbyt: 6b071ba68541f09ecba062a8 (metadata.tiktok.title; image or video asset)

## Cadence
5 posts a week, Monday to Friday, 12:00 Europe/London, same post on all three channels with captions adapted:
- Mon: website or branding tip
- Tue: what we do / service spotlight / client showcase
- Wed: short video reel (10 to 15 s, 1080x1920)
- Thu: small business advice (branding, Shopify, getting found on Google)
- Fri: offer or behind the scenes
English only. British spelling, £, no em dashes, no emoji, no hype words. One call to action pointing to nextbyt.uk (Instagram: "link in bio").

## Rules
- Never name a client or show client work without Rishitha's yes. Never quote prices other than Starter £399 and Growth £899 (Enterprise custom). Never invent offers, discounts or free services.
- Follow the brand guide (Projects doc claude/nextbyt-brand-guide.md): black #0d0a09 ground, one DM Sans headline with one gold Cormorant italic accent word, copper pill CTA, NEXTBYT wordmark top left.
- Do not repeat a topic listed in POSTED.md.

## How to build
- Images: write a week JSON like toolkit/week1.json, then in toolkit/ replace TOOLKIT_DIR with the real path and run `python3 build.py weekN.json` (1080x1350 PNG, Chrome at /usr/bin/google-chrome). Check a contact sheet before uploading.
- Reel: edit the scene text in toolkit/reel.html and run `python3 render_reel.py` (writes reel.mp4). Check frames before uploading.
- Upload to this repo under YYYY/MM/YYYY-MM-DD-slug.ext, push to main, then use https://raw.githubusercontent.com/rishluck/nextbyt-media/main/<path> as the Buffer asset URL. Confirm HTTP 200 first.
- Schedule with Buffer create_post, mode customScheduled, dueAt YYYY-MM-DDT12:00:00 with the London offset (+00:00 in winter, +01:00 in summer).
- Add each post to POSTED.md.
