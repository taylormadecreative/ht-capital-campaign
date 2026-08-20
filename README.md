# For Such a Time as This

Landing page for the Huston-Tillotson University capital campaign. Built by
[Taylormade Creative](https://www.taylormadecreative.net) from HT's Case for Support
and Funding Priorities documents.

## Status: preview, not approved for release

The campaign is unannounced and the figures on this page are preliminary, so the
site carries `noindex` plus a blanket `robots.txt`. Remove both only after HT
signs off on a public launch.

Two things need HT's confirmation first:

1. **Rendering-to-project pairings.** The Master Plan slides are not captioned per
   building, so each rendering was matched to a funding priority by inference.
   Image alt text is written descriptively rather than naming a building, and it
   should stay that way until someone at HT confirms the mapping.
2. **The funding totals do not reconcile.** The source document states the campaign
   "could reasonably approach $600–750 million," but the four priority ranges sum
   to $650–875M. Priority I is stated at $300–400M while its own five sub-items sum
   to $335–480M. Every range on the page is quoted verbatim and no total is ever
   computed; the scale bar is labeled "Segment widths show relative scale, not a
   committed total." These are HT's figures to correct, not ours.

## Structure

```
index.html        the page, self-contained apart from assets/ and Google Fonts
assets/           Master Plan renderings (r-*.jpg), campus photography, HT marks
build/bundle.py   produces a single-file build with everything base64-inlined
```

`build/bundle.py` downscales and inlines every asset, inlines GSAP, and strips the
document wrapper. Run it after editing `index.html` if you need the portable
single-file version.

## Credits

Master Plan renderings by McElroy Architecture and Smallwood. Brand system per the
Huston-Tillotson Brand Identity System (June 2026).

Typography note: the brand book specifies Martina Plantijn and Cards, neither of
which is licensed here, so the page uses Source Serif 4 and Archivo as approved
stand-ins. Swap them in `:root` if HT provides the licensed families.
