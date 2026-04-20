# Renewed Paper Source

## Files
- `main.tex`: renewed public paper source (11pt, single-column, double-spaced).
- `MAAT_renewed_paper.pdf`: shareable public PDF generated from the manuscript content.
- `build_public_pdf.py`: lightweight fallback PDF generator for environments without LaTeX.
- `refs.bib`: bibliography entries.
- `assets/`: supplementary GIF and PNG media referenced alongside the paper.

## Build
From this folder:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Output:
- `main.pdf`

## Notes
- The source here is intended for the public repo, not only the class submission bundle.
- The local machine used for this repo snapshot may not have a TeX toolchain installed, so rebuilding `main.pdf` can require `pdflatex` and `bibtex` or an equivalent engine such as `tectonic`.
- `MAAT_renewed_paper.pdf` is the current repo-friendly export for sharing when a full TeX build is unavailable.

## Supplementary Media
- `assets/vae_latent_compare_ep0_13s.gif`
- `assets/latest_resume555m_clip_002.gif`

These are small visuals for the repo, slides, and paper-adjacent project page.
