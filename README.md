# BNET.cc Docs

The source for [docs.bnet.cc](https://docs.bnet.cc), the documentation for
[Command Center](https://github.com/tagban/bnet_command_center), the software behind
[bnet.cc](https://bnet.cc).

Every page is a Markdown file in `content/`. When a change lands on `main`, GitHub
builds the site with [Hugo](https://gohugo.io) and publishes it with GitHub Pages.

## Editing a page

Click **Edit on GitHub** at the bottom of any page. GitHub opens the file and offers
to create a pull request. When it's merged, the site updates within a couple of minutes.

```markdown
---
title: "Tracker"
categories: ["Operations"]
---

Normal **Markdown** here. Link to other pages like [Architecture](/architecture/).
```

The sidebar is `content/sidebar/index.md`; edit it like any other page.

## Previewing on your computer

```bash
brew install hugo
hugo server
```

Then open http://localhost:1313.

## Theme

`themes/flatwiki/` is shared with [hlwiki.com](https://github.com/tagban/hlwiki).
This site's colors are in `static/css/site.css`.
