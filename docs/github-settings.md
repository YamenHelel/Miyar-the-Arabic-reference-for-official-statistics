# GitHub repository settings for SEO/GEO (lead: copy-paste, about 2 minutes)

The agent cannot write repository settings (the sandbox proxy blocks it), so these are ready to paste.

## 1. About box (repo home page → ⚙️ next to "About")
**Description:**
```
مِعيار Miʿyar: the Arabic reference for official statistics. Labour-statistics definitions quoted verbatim from ILO/ICLS standards and 10 national statistical offices, verified and compared. المرجع العربي للإحصاء الرسمي
```
**Website:**
```
https://yamenhelel.github.io/Miyar-the-Arabic-reference-for-official-statistics/
```
**Topics** (type each, press Enter):
```
official-statistics labour-statistics labor-statistics arabic arab-region ilo icls sdg unemployment labour-force-survey statistics metadata knowledge-base open-data ai claude geo llms-txt
```
Tick "Releases" and untick "Packages" and "Deployments" if you want a cleaner sidebar.

## 2. Social preview (Settings → General → Social preview → Edit)
Upload `static/social/site.png` from a site build. It is 1200×630, in the Miʿyar gold sheet design. To get it, run the website workflow once and download the artifact, or ask Claude to send you the file.

## 3. Pages (Settings → Pages)
Build and deployment → Source: **GitHub Actions**. Then Actions → **website** → Run workflow.

## 4. After the site is live (PRD 16, lead actions)
- Google Search Console and Bing Webmaster Tools: add the site and submit `sitemap.xml`.
- Zenodo: log in with GitHub, switch the repository on, then create release `v0.1.0`. Send Claude the DOI so it goes into `CITATION.cff` and the README.
- Wikidata: create the Miʿyar item (instance of: online database; language: Arabic; licence CC BY 4.0; official website = the URL above).
