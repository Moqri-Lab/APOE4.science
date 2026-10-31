# APOE4.science

Source for [apoe4.science](https://apoe4.science), a community resource on APOE ε4 homozygosity: evidence, data resources, papers, trials and drugs.

Maintained by Mahdi Moqri, PhD, in a personal capacity.

## Editing

The pages are generated. Edit the content in `tools/build.py` (and shared styles in `tools/base.css` or the `EXTRA_CSS` block), then rebuild from the repository root:

```
python3 tools/build.py
```

This rewrites the `.html` pages and `style.css`. Commit the regenerated files; GitHub Pages serves them from the `main` branch root.
