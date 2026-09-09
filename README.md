# For Such a Time as This

Landing page and giving page for the Huston-Tillotson University capital campaign.
Built for the University by [Taylormade Creative](https://www.taylormadecreative.net)
from HT's Case for Support and Funding Priorities documents.

## Structure

```
index.html        the campaign page
give/index.html   the giving and contact page
assets/           Master Plan renderings, campus photography, HT marks
build/bundle.py   produces a single-file build with every asset inlined
```

`build/bundle.py` downscales and inlines every asset, inlines GSAP, and strips the
document wrapper. Run it after editing `index.html` if you need the portable
single-file version.

## Credits

Master Plan renderings by McElroy Architecture and Smallwood. Colors, marks, and
typography follow the Huston-Tillotson University Brand Identity System. Every
figure on the page is quoted from the University's own campaign documents and is
labeled preliminary.
