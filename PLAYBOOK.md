# NextByt social media playbook

Claude makes and publishes every NextByt post. Rishitha does not make posts.

## Accounts (Buffer org "My organization", id 6b0719186a77081e39833051, free plan: 10 queued posts per channel)
- Facebook page "NextByt Digital Studio": 6b071a7b8541f09ecba05605 (metadata.facebook.type post / reel)
- Instagram @nextbyt_web: 6b071add8541f09ecba05a2c (metadata.instagram.type post / reel, shouldShareToFeed true)
- TikTok @nextbyt: 6b071ba68541f09ecba062a8. DO NOT POST OR CHANGE ANYTHING ON TIKTOK (Rishitha, 25 Nov 2026). Facebook and Instagram only.

## Cadence and variety (Rishitha wants it different every week, more professional, following current trends)
5 posts a week, Monday to Friday, 12:00 Europe/London, on Facebook and Instagram only with captions adapted per platform.
Every week MUST mix formats. Never use the same layout two days running. Each week include at least:
- 2 short videos (reels): kinetic type, "3 mistakes" countdowns, before/after website redesign reveals of invented demo sites, quick screen-style walkthroughs, Christmas or seasonal countdowns. Short-form video is the top format, so lean on it.
- 1 carousel (5 to 7 slides, toolkit/carousel.py): myth vs fact, step-by-step guides, checklists, "save this" reference posts. Carousels drive saves and shares.
- 1 or 2 single images, rotating layouts: big quote/stat card, checklist, price card, device mockup of an invented demo site, "this or that" comparison.
Rotate themes: website tips, branding, Shopify, getting found on Google and AI search, social media tips, small business advice, behind the scenes of the design process, seasonal and UK calendar moments (Christmas, New Year, Valentine's, Small Business Saturday, etc.).
Before planning each week: run a web search for current Instagram/TikTok trends, formats and UK small business news for that week, and use 1 or 2 that genuinely fit a premium design studio. Skip trends that are silly, off-brand or use copyrighted audio/characters.
Start a running series when it fits (for example a weekly "Website fix" tip) so followers come back.
End captions with a question or "save this" prompt to drive comments and saves. English only. British spelling, £, no em dashes, no emoji, no hype words. One call to action pointing to nextbyt.uk (Instagram: "link in bio").
Design: polished and editorial. Use the brand colours and fonts, but vary composition (centred, split, big number, full-bleed mockup). Always check a contact sheet; fix crowding, edge-touching text or weak hierarchy before posting.

## Rules
- Never name a client or show client work without Rishitha's yes. Never quote prices other than Starter £399 and Growth £899 (Enterprise custom). Never invent offers, discounts or free services.
- Follow the brand guide (Projects doc claude/nextbyt-brand-guide.md): black #0d0a09 ground, one DM Sans headline with one gold Cormorant italic accent word, copper pill CTA, NEXTBYT wordmark top left.
- Do not repeat a topic listed in POSTED.md.

## How to build
- Carousels: write a JSON like toolkit/myths.json and run `python3 carousel.py file.json` (slides 1080x1350; post all slides as multiple image assets in one Buffer post).
- Images: write a week JSON like toolkit/week1.json, then in toolkit/ replace TOOLKIT_DIR with the real path and run `python3 build.py weekN.json` (1080x1350 PNG, Chrome at /usr/bin/google-chrome). Check a contact sheet before uploading.
- Music: every reel gets music. If toolkit/music/ has licensed free tracks (Pixabay or YouTube Audio Library, sent by Rishitha), pick one that fits and trim it with a fade; otherwise generate an original track with `python3 music.py bed.wav <seconds> <bpm> <seed>` (vary bpm 85 to 120 and seed each time). Mux with ffmpeg: -c:v copy -c:a aac -b:a 160k -shortest. Never use copyrighted or trending commercial songs.
- Carousel slide kinds: cover, myth, check (big number + ticked label + headline, for checklists), end.
- Alternative single-image layouts: `python3 single.py weekN.json` with layout "date" (framed big date, for calendar moments) or "dm" (DM chat mockup, for the free website check). See toolkit/week2.json.
- Reel: edit the scene text in toolkit/reel.html (kinetic type), reel_beforeafter.html (browser wipe reveal of an invented demo site) or reel_countdown.html (3-2-1 countdown with progress bar), then run `python3 render_reel.py <file.html> <out.mp4> <seconds>`. Frames are saved every second to /tmp/fNNNN.jpg; check them before uploading.
- Upload to this repo under YYYY/MM/YYYY-MM-DD-slug.ext, push to main, then use https://raw.githubusercontent.com/rishluck/nextbyt-media/main/<path> as the Buffer asset URL. Confirm HTTP 200 first.
- Schedule with Buffer create_post, mode customScheduled, dueAt YYYY-MM-DDT12:00:00 with the London offset (+00:00 in winter, +01:00 in summer).
- Add each post to POSTED.md.

## Canva copies (Rishitha, 26 Nov 2026: keep building here, and also save editable copies in Canva each week)
- Canva folder "NextByt Social": FAHcBi__aLc.
- After building, convert each image or carousel's rendered HTML into one file under canva/ (one `<div data-document-role="page">` per slide, fonts as 'DM Sans', 'Cormorant Garamond', 'Josefin Sans'; scope only the bare `body{` rule, not `.body{`). Push, then import with Canva import-design-from-url using the commit-SHA raw URL (the main-branch raw URL is cached for minutes). Name it "YYYY-MM-DD Topic (NextByt)" and move it into the folder.
- Upload reels with upload-asset-from-url and move them into the folder too.
- Check the Canva thumbnails. Known importer limits: the gold Cormorant accent word comes in as DM Sans italic, and some text boxes need nudging. The Buffer posts always use the repo PNG/MP4, not the Canva copy.
