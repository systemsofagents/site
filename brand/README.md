# Systems of Agents · brand kit v0.1

## The Handoff

Two paths cross inside brackets. The brackets are the environment; the paths
are the participants; the amber square is the handoff. The mark belongs to the
system, not to a single agent. It should feel like a small notation from a
technical manual, not a chatbot mascot.

**Positioning:** An exploration of the patterns we can use to organize agents to do useful work and make steady progress toward long-term objectives.

**Voice:** Short and specific. Say what the system did, what the environment
allowed, and what the experiment actually established. Keep public pages simple. Avoid shell chrome, fake logs, CRT effects, and AI imagery that competes with the work.

## Identity

- **Primary:** `logos/wordmark-dark.svg` on Terminal or Panel. For constrained
  spaces, use `logos/mark-dark.svg`; the favicon and avatar are already framed.
- **Light:** `logos/*-light.svg` on near-white paper. Use `*-mono.svg` for
  one-color documents or printing. SVG wordmarks use vector outlines.
- **Clear space:** Keep at least one quarter of the mark height around the lockup.
  Minimum icon size is 16 px with the supplied favicon. Use the wordmark at
  200 px wide or larger. Never distort or add a glow.
- **Type:** DejaVu Sans Mono for terminal commands, controls, labels and
  identifiers. Open Sans for editorial reading and social headlines. Suggested
  web scale: 13–14 px label, 16 px terminal body, 17–18 px prose body at 1.6
  line-height. `web/tokens.css` includes platform fallbacks.
- **Color:** Terminal is the surface; Panel groups content. Text and Muted are
  the reading colors. Phosphor means actionable or active. Cursor is a sparse
  accent, never the only cue for status. Rule is decorative, not for text or for
  the only boundary of an interactive control. Underline links in prose and
  provide a visible keyboard focus ring.

| Role | Hex |
|---|---|
| Terminal | `#101613` |
| Panel | `#18211C` |
| Text | `#E8F0E9` |
| Muted | `#A2B2A7` |
| Phosphor | `#C9F879` |
| Cursor | `#F7C982` |
| Rule | `#2C3B32` |

Dark foreground samples meet WCAG AA against both dark surfaces. See
`contrast.txt` for ratios. Font binaries are not bundled; platform font
fallbacks preserve the terminal layout. The SVG exports carry their outlined
text. See the accompanying notices for typefaces used in exports.

## Share assets

- `social/og-home.png`: homepage share card.
- `social/og-track-01.png`: Track 01, “Uncapped session.”
- Both are 1200 × 630 PNG for Open Graph and X large cards, with editable SVG
  source. Host the PNGs publicly and use absolute HTTPS URLs in server-rendered
  page metadata; social crawlers may not execute browser-side JavaScript.
- `icons/avatar.png`: 512 × 512 profile image with a centered, circle-crop-safe mark.
- `icons/favicon.svg`, `favicon.ico`, and PNG sizes 16, 32, 180, 192 and 512.
- `web/share-metadata.html`: copy-ready head example. Change the URLs to the
  deployed file locations; use a versioned image URL after artwork changes to
  encourage preview refreshes.
