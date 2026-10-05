# Dr. Shanu Dengre — personal website

A static one-page site (`index.html` + `assets/`), hosted on GitHub Pages. There is no build step.

## Preview locally

Open `index.html` in a browser, or run a small local server so the PDF link behaves as it will on GitHub:

```bash
python -m http.server 8000
```

Then open http://localhost:8000.

## Deploy to GitHub Pages (first time)

1. On GitHub, create a **new public repository** named exactly `shanudengre82.github.io`. Leave it empty: no README, .gitignore or licence.
2. In a terminal, from this folder (`D:\Job_Applications\personal_website`), run:

   ```bash
   git init
   git add .
   git commit -m "Personal website"
   git branch -M main
   git remote add origin https://github.com/shanudengre82/shanudengre82.github.io.git
   git push -u origin main
   ```

3. In the repository, open **Settings → Pages**. Under **Build and deployment**, set:
   - Source: **Deploy from a branch**
   - Branch: **main** / **(root)**

   Then click **Save**.
4. After 1–2 minutes the site is live at **https://shanudengre82.github.io**. Progress shows under the repo's **Actions** tab.

## Updating the site

```bash
git add .
git commit -m "Update website"
git push
```

To refresh the downloadable CV, recompile `CV/Shanu_Dengre_CV.tex`, copy the new `Shanu_Dengre_CV.pdf` into `assets/`, and push.

## Optional

- **Custom domain:** in Settings → Pages → Custom domain, enter your domain. Then add the DNS records GitHub shows you at your domain registrar.
- **Show it on your profile:** add the URL to your LinkedIn "Website" field and to your GitHub profile bio.
