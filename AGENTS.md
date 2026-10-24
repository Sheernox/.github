# AGENTS.md - sheernox_github

The public organization profile for **Sheernox Technology Group**: GitHub shows `profile/README.md` on [github.com/Sheernox](https://github.com/Sheernox). Global workstation rules apply; this file adds only what is specific to this repo.

## Guardrails
- **A push publishes.** The hub mirrors `main` to the public `Sheernox/.github` repo, and GitHub shows the new README on the org page at once. Push only when asked.
- **Facts come from sheernox.com.** Services, links, claims (since 2009, 99.9% uptime SLA, 24/7 support) and contact channels must match the live site and the corporate identity rules in the `sheernox.com` repo's `AGENTS.md`: publish the city only, `1-855-375-TECH` as the only phone number, and the sales, support and abuse addresses. Never add a street address, registration number or personal names.
- **GitHub-safe markup only.** GitHub strips CSS, scripts and `style` attributes. Use markdown, plain HTML (`table`, `img`, `a`, `sub`, `align`, `width`, `valign`) and images. `tel:` links are stripped, so the phone number stays plain text.

## Banner
- Edit `banner/banner.html` (Outfit fonts in `banner/fonts/`, SIL OFL 1.1), then run `python3 scripts/render-banner.py`. It writes `profile/assets/banner.png` at 2560x800 with transparent rounded corners. Commit the source and the PNG together.
- The look follows the sheernox.com brand: dark aurora background, gradient accent heading, diagonal brand stripes. No eyebrow pills, grid backgrounds, editorial or console themes.

## Commands
```bash
python3 scripts/check.py          # relative refs exist, banner is a 2560x800 PNG, no banned dashes
python3 scripts/render-banner.py  # needs the Python playwright package and its Chromium
```
