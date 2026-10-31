# APOE4.science

Source for [apoe4.science](https://apoe4.science), a community resource on APOE ε4 homozygosity: evidence, data resources, papers, trials and drugs.

Maintained by [Mahdi Moqri, PhD](https://moqri.bwh.harvard.edu/), in a personal capacity.

## Editing

The pages are generated. Edit the content in `tools/build.py` (and shared styles in `tools/base.css` or the `EXTRA_CSS` block), then rebuild from the repository root:

```
python3 tools/build.py
```

This rewrites the `.html` pages (including `404.html`) and `style.css`. To redraw the link-preview image `og.png`, run `python3 tools/make_og.py` (needs Pillow). Commit the regenerated files; GitHub Pages serves them from the `main` branch root.

To announce a change on the home page, add a line at the top of `UPDATES` in `tools/build.py`.
