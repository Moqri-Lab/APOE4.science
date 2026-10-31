"""Build the apoe4.science site.

Usage, from the repository root:
    python3 tools/build.py

Writes the HTML pages and style.css into the repository root.
"""
import pathlib, urllib.parse

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent
BASE_CSS = (HERE / "base.css").read_text()

EXTRA_CSS = """
nav a[aria-current="page"]{color:var(--ink);font-weight:600;text-decoration:underline;text-decoration-color:var(--e4);text-decoration-thickness:2px;text-underline-offset:6px}
.page-head{padding-block:56px 8px;display:grid;gap:12px}
.page-head h1{font-size:clamp(34px,5vw,52px)}
.page-head .lede{font-size:18px;color:var(--muted);max-width:62ch}
.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0;border-top:1px solid var(--rule);border-left:1px solid var(--rule)}
.card{display:grid;gap:8px;align-content:start;padding:24px;border-right:1px solid var(--rule);border-bottom:1px solid var(--rule);text-decoration:none;color:var(--ink);background:var(--surface)}
.card:hover h3{color:var(--e4)}
.card h3{font-size:22px}
.card p{color:var(--muted);font-size:15.5px}
.group{display:grid;gap:14px;margin-bottom:40px}
.group h2{font-size:26px}
ul.refs li p.why{color:var(--muted);font-size:14.5px;margin-top:4px}
table.data{border-collapse:collapse;width:100%;min-width:760px}
table.data th,table.data td{padding:14px 16px;text-align:left;vertical-align:top;border-bottom:1px solid var(--rule);font-size:15px}
table.data th{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:400}
table.data td:first-child{font-weight:600;white-space:nowrap}
.pill{display:inline-block;font-family:var(--mono);font-size:11.5px;letter-spacing:.04em;padding:2px 8px;border:1px solid currentColor;white-space:nowrap}
.pill.ok{color:var(--e2)} .pill.stop{color:var(--e4)} .pill.run{color:var(--e3)}
.signup{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,480px);gap:40px;align-items:center}
.signup iframe{width:100%;max-width:480px;height:320px;border:1px solid var(--rule);background:#fff}
@media (max-width:820px){.signup{grid-template-columns:minmax(0,1fr)}}
td.asof{font-family:var(--mono);font-size:13px;color:var(--muted);white-space:nowrap}
.resources{display:grid;gap:0}
.resource{display:grid;grid-template-columns:minmax(0,240px) minmax(0,1fr);gap:32px;padding-block:32px;border-bottom:1px solid var(--rule);scroll-margin-top:24px}
.resource:first-child{padding-top:0}
.resource-head{display:grid;gap:8px;align-content:start}
.resource-head h2{font-size:28px}
.resource-head h2 a{color:var(--ink);text-decoration-color:var(--e4)}
.resource dl.facts div{grid-template-columns:110px minmax(0,1fr)}
@media (max-width:820px){.resource{grid-template-columns:minmax(0,1fr);gap:14px}.resource dl.facts div{grid-template-columns:minmax(0,1fr)}}
.skip{position:absolute;left:-9999px;top:0;background:var(--ink);color:var(--bg);padding:8px 14px;z-index:20}
.skip:focus{left:max(16px, env(safe-area-inset-left, 0px));top:8px}
dl.glossary div{grid-template-columns:260px minmax(0,1fr)}
dl.glossary dt{font-family:var(--body);text-transform:none;letter-spacing:0;font-size:14.5px;color:var(--ink);font-weight:600}
@media (max-width:820px){dl.glossary div{grid-template-columns:minmax(0,1fr)}}
@media (max-width:640px){
  header.top{flex-direction:column;align-items:flex-start;gap:12px;padding-block:16px}
  header.top nav{flex-wrap:nowrap;overflow-x:auto;max-width:100%;gap:18px;padding-bottom:6px;-webkit-overflow-scrolling:touch;scrollbar-width:thin}
  header.top nav a{white-space:nowrap}
}
@media (max-width:640px){
  table.data{min-width:0}
  table.data thead{position:absolute;left:-9999px}
  table.data tr{display:block;padding:14px 16px;border-bottom:1px solid var(--rule)}
  table.data td{display:grid;grid-template-columns:96px minmax(0,1fr);gap:10px;padding:5px 0;border:0;white-space:normal}
  table.data td::before{content:attr(data-label);font-family:var(--mono);font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);padding-top:3px}
}
.bar-row{display:flex;align-items:center;gap:10px;min-width:160px}
.bar{display:block;height:10px;background:var(--e4);min-width:4px}
.num{font-family:var(--mono);font-size:13px;font-variant-numeric:tabular-nums}
span.asof{font-family:var(--mono);font-size:13px;color:var(--muted)}
.updated{font-size:13.5px;color:var(--muted)}
@media (max-width:1000px){.cards{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:560px){.cards{grid-template-columns:minmax(0,1fr)}}
"""

PAGES = [  # (file, nav label, title)
    ("index.html", "Home", "APOE4 Science"),
    ("gene.html", "Gene and evidence", "The APOE gene and the evidence"),
    ("resources.html", "Resources", "Resources"),
    ("papers.html", "Papers", "Key papers"),
    ("trials.html", "Trials", "Clinical trials"),
    ("drugs.html", "Drugs", "Drugs"),
    ("glossary.html", "Glossary", "Glossary"),
    ("newsletter.html", "Newsletter", "Newsletter"),
]


def pm(q):
    return "https://pubmed.ncbi.nlm.nih.gov/?term=" + urllib.parse.quote_plus(q)


def ct(q):
    return "https://clinicaltrials.gov/search?term=" + urllib.parse.quote_plus(q)


SITE = "https://apoe4.science/"
DESC = "A community resource on APOE ε4 homozygosity: evidence, data, trials and drugs."


def shell(fname, title, body, extra_head=""):
    nav = "\n".join(
        f'      <a href="{f}"{" aria-current=\"page\"" if f == fname else ""}>{label}</a>'
        for f, label, _ in PAGES
    )
    doc_title = "APOE4 Science" if fname == "index.html" else f"{title} · APOE4 Science"
    jsonld = ""
    if fname == "index.html":
        jsonld = ('\n<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite",'
                  '"name":"APOE4 Science","url":"' + SITE + '","description":"' + DESC + '",'
                  '"maintainer":{"@type":"Person","name":"Mahdi Moqri"}}</script>')
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{doc_title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{DESC}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#b0234f">
<meta property="og:type" content="website">
<meta property="og:site_name" content="APOE4 Science">
<meta property="og:title" content="{doc_title}">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{SITE}{'' if fname == 'index.html' else fname}">
<meta property="og:image" content="{SITE}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{SITE}{'' if fname == 'index.html' else fname}">{jsonld}{extra_head}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,400;0,600;1,400&family=Public+Sans:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap">
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="wrap">
  <header class="top">
    <a class="mark" href="index.html">apoe<span>4</span>.science</a>
    <nav aria-label="Pages">
{nav}
    </nav>
  </header>
  <main id="main">
{body}
  </main>
  <footer>
    <span>apoe4.science · Maintained by Mahdi Moqri, PhD, in a personal capacity. An educational resource, not medical advice.</span>
    <span class="updated">Last reviewed October 2026 · <a href="https://github.com/Moqri-Lab/APOE4.science/issues">Suggest a correction</a></span>
  </footer>
</div>
<script>var c=document.querySelector('nav a[aria-current]');if(c&&c.scrollIntoView&&window.innerWidth<640)c.scrollIntoView({{inline:"center",block:"nearest"}});</script>
</body>
</html>
"""


def head(label, h1, lede):
    return f"""    <div class="page-head">
      <p class="label">{label}</p>
      <h1>{h1}</h1>
      <p class="lede">{lede}</p>
    </div>"""


def refs(items):
    out = []
    for cite, why, link in items:
        out.append(f'        <li>{cite} <a href="{link}">Read</a><p class="why">{why}</p></li>')
    return '      <ul class="refs">\n' + "\n".join(out) + "\n      </ul>"


DISCLAIMER = '      <p class="disclaimer">This site is for education and is not medical advice. Talk with your doctor or a genetic counselor about your own situation.</p>'


NEWSLETTER = """    <section id="newsletter">
      <div class="signup">
        <div class="prose">
          <p class="label">Newsletter</p>
          <h2>Get updates on APOE4 research</h2>
          <p>New findings, trials and data resources on APOE ε4 homozygosity, in your inbox. Enter your email to subscribe; no account or password is needed.</p>
          <p class="note">The newsletter is hosted on Substack, which stores your email. If you later create a Substack profile, you can hide your subscriptions in its settings. Unsubscribe from any email.</p>
          <p class="note">Prefer Substack directly? <a href="https://apoe4science.substack.com">apoe4science.substack.com</a></p>
        </div>
        <iframe src="https://apoe4science.substack.com/embed" title="Subscribe to the APOE4 Science newsletter" loading="lazy" scrolling="no"></iframe>
      </div>
    </section>"""

pages = {}

# ---------- Home ----------
UPDATES = [  # newest first; keep to about five
    ("Oct 2026", 'Trial statuses checked against registries; donanemab ARIA rates by genotype added to <a href="trials.html">Trials</a>.'),
    ("Oct 2026", 'New chart of APOE ε4 risk by ancestry on <a href="gene.html">Gene and evidence</a>.'),
    ("Oct 2026", 'AD Workbench, All of Us and SEA-AD added to <a href="resources.html">Resources</a>.'),
    ("Oct 2026", '<a href="glossary.html">Glossary</a> of genetics, biomarker and trial terms.'),
    ("Oct 2026", 'Site launched.'),
]
cards = [
    ("gene.html", "Gene and evidence", "Three forms of APOE, one amino acid apart, and what two copies of ε4 do to timing, amyloid and blood vessels."),
    ("resources.html", "Resources", "Cohorts and repositories with ε4/ε4 data, and how to access them."),
    ("papers.html", "Key papers", "The studies that define what we know, grouped by topic."),
    ("trials.html", "Clinical trials", "Trials in ε4/ε4 carriers and trials that report results by genotype."),
    ("drugs.html", "Drugs", "Approved and investigational treatments, and what they mean for ε4/ε4."),
    ("newsletter.html", "Newsletter", "Research updates on APOE4 in your inbox."),
]
pages["index.html"] = f"""    <div class="hero">
      <div>
        <p class="label">A community resource</p>
        <h1 style="margin-top:14px">Two copies of APOE4 may be a <em>genetic form</em> of Alzheimer’s disease.</h1>
        <p class="lede">Evidence, data resources, papers, trials and drugs on APOE ε4 homozygosity, gathered in one place for the community.</p>
      </div>
      <div class="geno" aria-label="Genotype epsilon 4 slash epsilon 4">ε4/ε4<small>About 2–3% of people</small></div>
    </div>
    <section>
      <div class="cards">
""" + "\n".join(
    f'        <a class="card" href="{f}"><h3>{t}</h3><p>{d}</p></a>' for f, t, d in cards
) + """
      </div>
    </section>
    <section>
      <div class="sec-head">
        <p class="label">Recently updated</p>
        <h2>What’s new</h2>
      </div>
      <ul class="refs">
""" + "\n".join(f'        <li><span class="asof">{d}</span> · {t}</li>' for d, t in UPDATES) + """
      </ul>
    </section>
""" + NEWSLETTER

# ---------- Gene ----------
pages["gene.html"] = head("The gene", "One letter apart",
    "Apolipoprotein E carries cholesterol and other lipids in the brain and blood. Everyone inherits two copies, one from each parent.") + """
    <section>
      <div class="alleles" role="region" aria-label="APOE alleles" tabindex="0">
        <table class="allele">
          <thead><tr><th>Allele</th><th>Residue 112</th><th>Residue 158</th><th>Alzheimer’s risk</th></tr></thead>
          <tbody>
            <tr><td class="al c-e2">ε2</td><td><span class="res c-e2"><b>C</b>Cys</span></td><td><span class="res c-e2"><b>C</b>Cys</span></td><td>Lower than ε3</td></tr>
            <tr><td class="al c-e3">ε3</td><td><span class="res c-e3"><b>C</b>Cys</span></td><td><span class="res c-e3"><b>R</b>Arg</span></td><td>Reference (most common)</td></tr>
            <tr class="is-e4"><td class="al c-e4">ε4</td><td><span class="res c-e4"><b>R</b>Arg</span></td><td><span class="res c-e4"><b>R</b>Arg</span></td><td><strong>Highest; strongest with two copies</strong></td></tr>
          </tbody>
        </table>
      </div>
      <p class="note">A single amino-acid change at residue 112 separates ε4 from ε3. Carrying one ε4 copy raises risk; carrying two (ε4/ε4, homozygous) raises it much further and shifts symptoms to an earlier, more predictable age. Risk by genotype also differs by age, sex and ancestry.</p>
    </section>
    <section id="evidence">
      <div class="sec-head">
        <p class="label">What we know</p>
        <h2>Evidence so far</h2>
      </div>
      <div class="findings">
        <article class="finding">
          <div class="fig">~65</div>
          <p>Typical age at symptom onset in ε4/ε4 carriers, with a narrower range than in ε3/ε3. Almost all show Alzheimer’s pathology at autopsy.</p>
          <p class="src">Fortea et al., <i>Nature Medicine</i> 2024 (NACC brain donors and five biomarker cohorts)</p>
        </article>
        <article class="finding">
          <div class="fig">55</div>
          <p>Age from which Alzheimer’s biomarkers are already higher than in ε3/ε3. By 65, nearly all have abnormal spinal-fluid amyloid and about 75% have a positive amyloid scan.</p>
          <p class="src">Fortea et al., <i>Nature Medicine</i> 2024</p>
        </article>
        <article class="finding">
          <div class="fig">~13×</div>
          <p>Higher odds of moderate to severe amyloid in brain blood vessel walls (cerebral amyloid angiopathy) at autopsy with two ε4 copies.</p>
          <p class="src">Greenberg et al., <i>Annals of Neurology</i> 1995</p>
        </article>
        <article class="finding">
          <div class="fig">4.8×</div>
          <p>Higher odds of accumulating two or more small brain bleeds over follow-up in ε4/ε4 adults without symptoms. This matters for the safety of anti-amyloid drugs.</p>
          <p class="src">A4 Study, <i>Alzheimer’s &amp; Dementia</i> 2025</p>
        </article>
        <article class="finding">
          <div class="fig">84 → 68</div>
          <p>Mean age at onset fell from 84 to 68 as the number of ε4 copies rose, in 42 families with late-onset Alzheimer’s. Two copies were nearly sufficient to cause disease by age 80 in these families.</p>
          <p class="src">Corder et al., <i>Science</i> 1993</p>
        </article>
        <article class="finding">
          <div class="fig">51–60%</div>
          <p>Estimated lifetime risk of Alzheimer’s by age 85 for ε4/ε4 (about 51% in men and 60% in women), versus about 11–14% for the general population. Family studies give higher estimates.</p>
          <p class="src">Genin et al., <i>Molecular Psychiatry</i> 2011</p>
        </article>
      </div>
      <div class="group" style="margin-top:40px">
        <h2>Risk differs by ancestry</h2>
        <p class="note" style="margin-top:0">Odds of Alzheimer’s with one ε4 copy (ε3/ε4) compared with ε3/ε3, by population ancestry. The study reported a similar stepwise pattern across ancestries for ε4/ε4.</p>
        <div class="alleles" role="region" aria-label="APOE ε3/ε4 odds ratios by ancestry" tabindex="0">
          <table class="data">
            <thead><tr><th>Ancestry</th><th>Odds ratio</th><th>95% CI</th></tr></thead>
            <tbody>
            <tr><td data-label="Ancestry">East Asian</td><td data-label="Odds ratio"><span class="bar-row"><span class="bar" style="width:91%"></span><span class="num">4.54</span></span></td><td data-label="95% CI" class="asof">3.99–5.17</td></tr>
            <tr><td data-label="Ancestry">White</td><td data-label="Odds ratio"><span class="bar-row"><span class="bar" style="width:69%"></span><span class="num">3.46</span></span></td><td data-label="95% CI" class="asof">3.27–3.65</td></tr>
            <tr><td data-label="Ancestry">Black</td><td data-label="Odds ratio"><span class="bar-row"><span class="bar" style="width:44%"></span><span class="num">2.18</span></span></td><td data-label="95% CI" class="asof">1.90–2.49</td></tr>
            <tr><td data-label="Ancestry">Hispanic</td><td data-label="Odds ratio"><span class="bar-row"><span class="bar" style="width:38%"></span><span class="num">1.90</span></span></td><td data-label="95% CI" class="asof">1.65–2.18</td></tr>
            </tbody>
          </table>
        </div>
        <p class="src note">Belloy et al., <i>JAMA Neurology</i> 2023</p>
      </div>
      <p class="note" style="margin-top:20px">Full references are on the <a href="papers.html">Papers</a> page.</p>
    </section>"""

# ---------- Resources ----------
RESOURCES = [
    dict(id="nacc", name="NACC", url="https://naccdata.org/",
         full="National Alzheimer’s Coordinating Center",
         host="University of Washington; funded by NIA",
         size="More than 54,000 participants followed since 2005 across Alzheimer’s Disease Research Centers",
         data="Yearly clinical and cognitive assessments, diagnoses, medications, neuropathology for brain donors, and linked imaging and biomarker data",
         apoe="APOE genotype for most participants. The Fortea 2024 study used 3,297 genotyped NACC brain donors to show near-full penetrance of pathology in ε4/ε4.",
         access="Online data request form; free; usually days to a few weeks. Also analysable in the AD Workbench",
         best="Clinical trajectories, age at onset and pathology"),
    dict(id="niagads", name="NIAGADS", url="https://www.niagads.org/",
         full="NIA Genetics of Alzheimer’s Disease Data Storage Site",
         host="University of Pennsylvania; NIA’s designated repository for Alzheimer’s genetic data",
         size="Dozens of genetic datasets, including the Alzheimer’s Disease Genetics Consortium (ADGC) genome-wide studies",
         data="Genotype arrays, sequencing, summary statistics and associated phenotypes",
         apoe="Genetic records of NACC participants can be linked to their NACC clinical data on request, enabling genotype-stratified trajectories.",
         access="Formal data access request with a research use statement, institutional signing official and data use agreement; renewed yearly. NIH security standards apply.",
         best="Genetic modifiers, ancestry effects"),
    dict(id="adsp", name="ADSP", url="https://adsp.niagads.org/",
         full="Alzheimer’s Disease Sequencing Project",
         host="NIA and NHGRI; data distributed through NIAGADS",
         size="Whole-genome sequencing in tens of thousands of people, with growing African American, Hispanic and Asian representation",
         data="Whole genomes and exomes, plus harmonized cognition, diagnosis and biomarker data from the ADSP Phenotype Harmonization Consortium",
         apoe="Enough ε4/ε4 carriers across ancestries to look for variants that delay or hasten onset in homozygotes.",
         access="Through NIAGADS, with the same request process. ADSP also asks for a plan to return derived data.",
         best="Protective and risk variants within ε4/ε4"),
    dict(id="ncrad", name="NCRAD", url="https://ncrad.org/",
         full="National Centralized Repository for Alzheimer’s Disease and Related Dementias",
         host="Indiana University; funded by NIA",
         size="Biosamples from Alzheimer’s Disease Research Centers and many NIA-funded cohorts",
         data="DNA, plasma, serum, spinal fluid and cell lines, linked to clinical data",
         apoe="Stored samples from people with known genotype and outcomes, for measuring new biomarkers such as proteomic or epigenetic aging clocks.",
         access="Biosample request reviewed by NCRAD and the contributing studies",
         best="New biomarker measurements on existing cohorts"),
    dict(id="adni", name="ADNI", url="https://adni.loni.usc.edu/",
         full="Alzheimer’s Disease Neuroimaging Initiative",
         host="Multi-site North American study; data shared through LONI at the University of Southern California",
         size="Several thousand participants across study phases since 2004",
         data="Repeated MRI, amyloid and tau PET, spinal fluid and plasma biomarkers, cognition and genetics",
         apoe="Repeated imaging lets you compare when amyloid, tau and small bleeds appear in ε4/ε4 versus other genotypes.",
         access="Online application and data use agreement through LONI’s Image and Data Archive",
         best="Biomarker and imaging timelines"),
    dict(id="a4", name="A4 Study", url="https://www.a4studydata.org/",
         full="Anti-Amyloid Treatment in Asymptomatic Alzheimer’s study, with the companion LEARN study",
         host="Alzheimer’s Therapeutic Research Institute (USC)",
         size="More than 1,100 randomized amyloid-positive adults aged 65–85 without symptoms, plus amyloid-negative LEARN participants",
         data="Amyloid PET at screening, tau PET in a subset, repeated MRI including microbleeds, cognition, plasma biomarkers and APOE genotype",
         apoe="Shows how small brain bleeds accumulate in ε4/ε4 adults without symptoms (odds ratio 4.8 in a 2025 analysis).",
         access="Data use agreement through the A4 data portal",
         best="Preclinical ε4/ε4 biology and ARIA risk"),
    dict(id="adkp", name="AD Knowledge Portal", url="https://adknowledgeportal.synapse.org/",
         full="AMP-AD and MODEL-AD data portal",
         host="Sage Bionetworks (Synapse); funded by NIA",
         size="Brain tissue from thousands of donors across ROSMAP, Mount Sinai Brain Bank, Mayo and diverse-cohort studies, plus mouse models",
         data="Brain genomics, transcriptomics, single-cell, proteomics, metabolomics and epigenomics; humanized APOE4 knock-in mice from MODEL-AD",
         apoe="Compare brain molecular changes by genotype in humans, and test APOE4 effects with age in mice.",
         access="Synapse account and certification, plus a data use certificate signed by your institution for controlled data",
         best="Brain molecular mechanisms"),
    dict(id="ukb", name="UK Biobank", url="https://www.ukbiobank.ac.uk/",
         full="UK Biobank",
         host="UK charity; data analysed on its cloud Research Analysis Platform",
         size="About 500,000 adults recruited 2006–2010; roughly 2% are ε4/ε4",
         data="Genotypes and whole genomes, plasma proteomics in about 53,000 people, brain MRI in a subset, and linked hospital, death and primary-care records",
         apoe="About 9,700 ε4/ε4 participants followed for over 15 years, many with proteomics, for prediction and risk-factor studies.",
         access="Project application with a fee; analysis on the cloud platform",
         best="Large-scale prediction and outcomes"),
    dict(id="aou", name="All of Us", url="https://www.researchallofus.org/",
         full="NIH All of Us Research Program",
         host="NIH; analysis in the Researcher Workbench",
         size="Hundreds of thousands of participants with whole-genome sequencing, with strong representation of groups underrepresented in research",
         data="Whole genomes, electronic health records, surveys and wearable data",
         apoe="APOE genotype can be derived from the genomes and studied across diverse ancestries alongside health records.",
         access="Institutional data use agreement, then individual registration and training; genomic data is in the controlled tier",
         best="Diverse ancestries and health records"),
    dict(id="addi", name="AD Workbench", url="https://www.alzheimersdata.org/ad-workbench",
         full="Alzheimer’s Disease Data Initiative (ADDI) AD Workbench",
         host="Alzheimer’s Disease Data Initiative, a nonprofit",
         size="Hundreds of datasets, browsable without login in the public AD Discovery Portal",
         data="Cohort, clinical trial and biomarker datasets from many contributors, including NACC and the ALFA study",
         apoe="One place to find and analyse several APOE-genotyped cohorts side by side in a secure cloud workspace.",
         access="Free workspace with R and Python; each dataset keeps its own access rules",
         best="Finding and combining datasets"),
    dict(id="seaad", name="SEA-AD", url="https://portal.brain-map.org/explore/seattle-alzheimers-disease",
         full="Seattle Alzheimer’s Disease Brain Cell Atlas",
         host="Allen Institute, University of Washington and Kaiser Permanente Washington",
         size="Middle temporal gyrus from 84 donors spanning the Alzheimer’s spectrum, plus neurotypical reference brains",
         data="Single-nucleus RNA and chromatin data, spatial transcriptomics and quantitative neuropathology",
         apoe="Cell-type-resolved brain changes across disease stages; check donor metadata for APOE genotype.",
         access="Open access; also distributed through the AD Knowledge Portal and a public AWS bucket",
         best="Cell-type brain atlas"),
]

summary_rows = "\n".join(
    f'            <tr><td data-label="Resource"><a href="#{r["id"]}">{r["name"]}</a></td><td data-label="Best for">{r["best"]}</td><td data-label="Access">{r["access"].split(";")[0].split(",")[0]}</td></tr>'
    for r in RESOURCES)
detail = "\n".join(f"""      <article class="resource" id="{r['id']}">
        <div class="resource-head">
          <h2><a href="{r['url']}">{r['name']}</a></h2>
          <p class="label">{r['full']}</p>
        </div>
        <dl class="facts">
          <div><dt>Run by</dt><dd>{r['host']}</dd></div>
          <div><dt>Size</dt><dd>{r['size']}</dd></div>
          <div><dt>Data</dt><dd>{r['data']}</dd></div>
          <div><dt>For ε4/ε4</dt><dd>{r['apoe']}</dd></div>
          <div><dt>Access</dt><dd>{r['access']}</dd></div>
        </dl>
      </article>""" for r in RESOURCES)

pages["resources.html"] = head("Resources", "Where to find ε4/ε4 data",
    "Cohorts, repositories and biobanks with APOE genotype linked to clinical, imaging, omic or autopsy data. Sizes are approximate; check each resource for current numbers and terms.") + f"""
    <section>
      <div class="alleles" role="region" aria-label="Resources at a glance" tabindex="0">
        <table class="data">
          <thead><tr><th>Resource</th><th>Best for</th><th>Access</th></tr></thead>
          <tbody>
{summary_rows}
          </tbody>
        </table>
      </div>
    </section>
    <section class="resources">
{detail}
    </section>
    <section>
      <div class="sec-head">
        <p class="label">Combining resources</p>
        <h2>Common pairings</h2>
      </div>
      <ul class="measures prose">
        <li><b>NACC + NIAGADS/ADSP:</b> clinical trajectories with whole-genome data, linked through NACC participant IDs.</li>
        <li><b>NACC + NCRAD:</b> outcomes plus stored blood or spinal fluid from the same people, for new biomarker assays.</li>
        <li><b>ADNI or A4 + UK Biobank:</b> deep imaging timelines alongside large-scale prediction and outcomes.</li>
      </ul>
      <p class="note">Each resource sets its own terms. NIH rules on controlled-access genomic data also limit the use of public generative AI tools with individual-level data, and require data to be held in approved secure environments.</p>
    </section>"""

# ---------- Papers ----------
groups = [
    ("Genetics and risk", [
        ("Corder EH, Saunders AM, Strittmatter WJ, et al. Gene dose of apolipoprotein E type 4 allele and the risk of Alzheimer’s disease in late onset families. <i>Science</i> 1993.",
         "First showed that risk rises and age at onset falls with each ε4 copy.", "https://doi.org/10.1126/science.8346443"),
        ("Strittmatter WJ, Saunders AM, Schmechel D, et al. Apolipoprotein E: high-avidity binding to β-amyloid and increased frequency of type 4 allele in late-onset familial Alzheimer disease. <i>PNAS</i> 1993.",
         "Linked APOE to Alzheimer’s and to amyloid binding.", "https://doi.org/10.1073/pnas.90.5.1977"),
        ("Farrer LA, Cupples LA, Haines JL, et al. Effects of age, sex, and ethnicity on the association between apolipoprotein E genotype and Alzheimer disease: a meta-analysis. <i>JAMA</i> 1997.",
         "Classic estimates of risk by genotype, age, sex and ancestry.", "https://doi.org/10.1001/jama.1997.03550160069041"),
        ("Genin E, Hannequin D, Wallon D, et al. APOE and Alzheimer disease: a major gene with semi-dominant inheritance. <i>Molecular Psychiatry</i> 2011.",
         "Lifetime risk estimates for ε4/ε4.", "https://doi.org/10.1038/mp.2011.52"),
        ("Belloy ME, Andrews SJ, Le Guen Y, et al. APOE genotype and Alzheimer disease risk across age, sex, and population ancestry. <i>JAMA Neurology</i> 2023.",
         "Large modern estimates across ancestries.", "https://doi.org/10.1001/jamaneurol.2023.3599"),
        ("Fortea J, Pegueroles J, Alcolea D, et al. APOE4 homozygosity represents a distinct genetic form of Alzheimer’s disease. <i>Nature Medicine</i> 2024.",
         "Near-full penetrance of pathology and predictable onset in ε4/ε4.", "https://doi.org/10.1038/s41591-024-02931-w"),
    ]),
    ("Amyloid, blood vessels and bleeding", [
        ("Greenberg SM, Rebeck GW, Vonsattel JP, Gomez-Isla T, Hyman BT. Apolipoprotein E ε4 and cerebral hemorrhage associated with amyloid angiopathy. <i>Annals of Neurology</i> 1995.",
         "About 13-fold higher odds of moderate to severe amyloid angiopathy with two ε4 copies.", "https://doi.org/10.1002/ana.410380219"),
        ("Jansen WJ, Ossenkoppele R, Knol DL, et al. Prevalence of cerebral amyloid pathology in persons without dementia: a meta-analysis. <i>JAMA</i> 2015.",
         "Amyloid positivity by age and APOE genotype in people without dementia.", "https://doi.org/10.1001/jama.2015.4668"),
        ("Montagne A, Nation DA, Sagare AP, et al. APOE4 leads to blood–brain barrier dysfunction predicting cognitive decline. <i>Nature</i> 2020.",
         "A vascular route for APOE4 effects, independent of amyloid and tau.", "https://doi.org/10.1038/s41586-020-2247-3"),
        ("Independent effects of white matter lesion volume and APOE ε4 on ARIA-H in the A4 Study. <i>Alzheimer’s &amp; Dementia</i> 2025.",
         "ε4/ε4 predicts accumulating small bleeds in people without symptoms.", "https://pubmed.ncbi.nlm.nih.gov/41085172/"),
    ]),
    ("Blood biomarkers", [
        ("APOE ε4 carriership determines a faster plasma p-tau217 progression in Aβ-positive individuals. <i>Alzheimer’s &amp; Dementia</i> 2025.",
         "In amyloid-positive people, p-tau217 rises faster in ε4 carriers (TRIAD and ADNI).", "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12741900/"),
        ("APOE4 impact on soluble and insoluble tau pathology is mostly influenced by amyloid-β. 2025.",
         "A contrasting view: in BioFINDER and WRAP, APOE4 effects on p-tau217 largely run through amyloid.", "https://pubmed.ncbi.nlm.nih.gov/39817469/"),
    ]),
    ("Mechanisms", [
        ("Shi Y, Yamada K, Liddelow SA, et al. ApoE4 markedly exacerbates tau-mediated neurodegeneration in a mouse model of tauopathy. <i>Nature</i> 2017.",
         "APOE4 worsens tau damage, partly through microglia.", "https://doi.org/10.1038/nature24016"),
        ("Lin YT, Seo J, Gao F, et al. APOE4 causes widespread molecular and cellular alterations associated with Alzheimer’s disease phenotypes in human iPSC-derived brain cell types. <i>Neuron</i> 2018.",
         "Matched human cell models of APOE3 versus APOE4.", "https://doi.org/10.1016/j.neuron.2018.05.008"),
        ("Blanchard JW, Akay LA, Davila-Velderrain J, et al. APOE4 impairs myelination via cholesterol dysregulation in oligodendrocytes. <i>Nature</i> 2022.",
         "Cholesterol handling and myelin loss in human ε4 brains and cells.", "https://doi.org/10.1038/s41586-022-05439-w"),
        ("Haney MS, Pálovics R, Munson CN, et al. APOE4/4 is linked to damaging lipid droplets in Alzheimer’s disease microglia. <i>Nature</i> 2024.",
         "Lipid-laden microglia in ε4/ε4 brains.", "https://doi.org/10.1038/s41586-024-07185-7"),
    ]),
    ("Protection and resilience", [
        ("Arboleda-Velasquez JF, Lopera F, O’Hare M, et al. Resistance to autosomal dominant Alzheimer’s disease in an APOE3 Christchurch homozygote: a case report. <i>Nature Medicine</i> 2019.",
         "A rare APOE variant that appears to protect against early-onset disease, pointing to APOE as a drug target.", "https://doi.org/10.1038/s41591-019-0611-3"),
        ("Le Guen Y, et al. Association of rare APOE missense variants V236E and R251G with risk of Alzheimer disease. <i>JAMA Neurology</i> 2022.",
         "R251G, inherited together with ε4, roughly halves its risk effect, showing that ε4 risk can be offset.", "https://doi.org/10.1001/jamaneurol.2022.1166"),
        ("Nelson MR, et al. The APOE-R136S mutation protects against APOE4-driven Tau pathology, neurodegeneration and neuroinflammation. <i>Nature Neuroscience</i> 2023.",
         "The Christchurch change blocks APOE4-driven tau damage in mice, supporting APOE-directed therapies.", "https://doi.org/10.1038/s41593-023-01480-8"),
    ]),
    ("Targeting APOE", [
        ("Huynh TV, et al. Age-dependent effects of apoE reduction using antisense oligonucleotides in a model of β-amyloidosis. <i>Neuron</i> 2017.",
         "Lowering APOE before plaques form strongly reduces amyloid pathology in mice; later lowering changes plaque size and toxicity.", "https://doi.org/10.1016/j.neuron.2017.11.014"),
        ("Liao F, et al. Targeting of nonlipidated, aggregated apoE with antibodies inhibits amyloid accumulation. <i>Journal of Clinical Investigation</i> 2018.",
         "The HAE-4 antibody, which binds aggregated apoE, lowers plaque burden in APOE4 mice.", "https://doi.org/10.1172/JCI96429"),
    ]),
    ("Reviews", [
        ("Belloy ME, Napolioni V, Greicius MD. A quarter century of APOE and Alzheimer’s disease: progress to date and the path forward. <i>Neuron</i> 2019.",
         "Broad review of APOE genetics and biology.", "https://doi.org/10.1016/j.neuron.2019.01.056"),
        ("Yamazaki Y, Zhao N, Caulfield TR, Liu CC, Bu G. Apolipoprotein E and Alzheimer disease: pathobiology and targeting strategies. <i>Nature Reviews Neurology</i> 2019.",
         "Mechanisms and therapeutic approaches.", "https://doi.org/10.1038/s41582-019-0228-7"),
        ("Hampel H, Elhage A, Cho M, Apostolova LG, Nicoll JAR, Atri A. Amyloid-related imaging abnormalities (ARIA): radiological, biological and clinical characteristics. <i>Brain</i> 2023.",
         "What ARIA is, how it is detected, and why ε4/ε4 raises risk.", "https://doi.org/10.1093/brain/awad188"),
    ]),
    ("Community and policy", [
        ("UsAgainstAlzheimer’s. FDA Patient Listening Session: Alzheimer’s disease and APOE ε4 homozygotes. Summary, July 2025.",
         "APOE ε4 homozygotes describe their needs and the lack of treatment options to FDA staff.", "https://www.usagainstalzheimers.org/sites/default/files/2025-11/07222025-FDA_Patient_Listening_Session-APOE4_Homozygosity_Summary_Final.pdf"),
    ]),
    ("Trial results by genotype", [
        ("van Dyck CH, Swanson CJ, Aisen P, et al. Lecanemab in early Alzheimer’s disease. <i>New England Journal of Medicine</i> 2023.",
         "Clarity AD; ARIA rates reported by APOE genotype.", "https://doi.org/10.1056/NEJMoa2212948"),
        ("Sims JR, Zimmer JA, Evans CD, et al. Donanemab in early symptomatic Alzheimer disease: the TRAILBLAZER-ALZ 2 randomized clinical trial. <i>JAMA</i> 2023.",
         "ARIA rates reported by APOE genotype.", "https://doi.org/10.1001/jama.2023.13239"),
        ("Efficacy and safety of oral valiltramiprosate in APOE4/4 homozygotes with early AD: topline results from the APOLLOE4 Phase 3 trial. 2025.",
         "The first completed Phase 3 trial run only in ε4/ε4.", "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12726020/"),
    ]),
]
body = head("Key papers", "The studies that define what we know",
    "Grouped by topic. Each link opens the paper.") + "\n    <section>\n"
for g, items in groups:
    body += f'    <div class="group">\n      <h2>{g}</h2>\n{refs(items)}\n    </div>\n'
body += "    </section>"
pages["papers.html"] = body

# ---------- Glossary ----------
GLOSSARY = [('Allele', 'One version of a gene. APOE has three common alleles: ε2, ε3 and ε4.'), ('Homozygote / heterozygote', 'A homozygote carries two copies of the same allele (ε4/ε4). A heterozygote carries two different alleles (for example ε3/ε4).'), ('Penetrance', 'The share of people with a genotype who develop the disease. ε4/ε4 shows high but incomplete penetrance.'), ('Amyloid-β (Aβ)', 'A protein fragment that clumps into plaques between brain cells; the earliest known change in Alzheimer’s.'), ('Tau', 'A protein that forms tangles inside neurons. Tau spread tracks closely with symptoms.'), ('Cerebral amyloid angiopathy (CAA)', 'Amyloid deposited in the walls of brain blood vessels, which weakens them and raises the risk of bleeds. More common with ε4.'), ('Microbleed', 'A tiny, usually silent bleed in the brain, seen on certain MRI scans.'), ('ARIA', 'Amyloid-related imaging abnormalities: brain swelling (ARIA-E) or small bleeds and iron deposits (ARIA-H) seen on MRI, mainly with anti-amyloid antibodies. Risk is highest in ε4/ε4.'), ('Amyloid PET / tau PET', 'Brain scans that measure amyloid plaques or tau tangles in living people.'), ('Plasma biomarkers', 'Blood tests for Alzheimer’s-related proteins, such as p-tau217, Aβ42/40, NfL and GFAP.'), ('MCI', 'Mild cognitive impairment: measurable decline in memory or thinking that does not yet disrupt daily life.'), ('CDR-SB, ADAS-Cog, iADRS', 'Rating scales used as outcomes in Alzheimer’s trials to measure cognition and daily function.'), ('Preclinical Alzheimer’s', 'Alzheimer’s brain changes, such as amyloid, without symptoms. Prevention trials enroll at this stage.'), ('Natural history study', 'An observational study that follows people over time without an experimental treatment, to learn how a disease unfolds.'), ('Gene therapy', 'Delivering genetic material, often with a harmless virus (AAV), to change what cells produce, for example adding APOE2.'), ('APOE3 Christchurch', 'A rare APOE variant that appeared to protect a carrier of an early-onset Alzheimer’s mutation, pointing to APOE as a drug target.'), ('BACE inhibitor', 'A drug that blocks the enzyme BACE1, which cuts the amyloid precursor protein to make amyloid-β.'), ('Antisense oligonucleotide (ASO)', 'A short strand of synthetic genetic material that lowers production of a specific protein, such as APOE.'), ('LRRK2', 'A kinase enzyme involved in inflammation and cell trafficking; the target of the investigational drug HT-4253.'), ('Odds ratio', 'How much more likely an outcome is in one group than another; 1 means no difference.'), ('FDA Fast Track', 'A US designation that speeds review of drugs for serious conditions with unmet need. It is not an approval.')]
pages["glossary.html"] = head("Glossary", "Terms used on this site",
    "Short definitions of the genetics, biomarker and trial terms that come up in APOE4 research.") + """
    <section>
      <dl class="facts glossary">
""" + "\n".join(f'        <div><dt>{t}</dt><dd>{d}</dd></div>' for t, d in GLOSSARY) + """
      </dl>
    </section>"""

# ---------- Trials ----------
def pill(kind, text):
    return f'<span class="pill {kind}">{text}</span>'

trials = [
    ("APOLLOE4", "Valiltramiprosate (ALZ-801), oral", "325 ε4/ε4 with early Alzheimer’s (Phase 3)",
     pill("stop", "Missed primary endpoint") + " Prespecified MCI subgroup favored drug (nominal p-values). ARIA-E about 3% in both arms. In July 2026 the company reported a 53% net reduction in plasma p-tau217 versus placebo in the MCI subgroup.",
     "https://clinicaltrials.gov/study/NCT04770220"),
    ("Generation Study 1", "Umibecestat (BACE inhibitor) or CAD106 (amyloid vaccine)", "Cognitively unimpaired ε4/ε4, aged 60–75",
     pill("stop", "Stopped 2019") + " Umibecestat arms stopped for mild cognitive worsening, brain volume loss and weight loss; CAD106 arm also halted. In a later analysis, CAD106 produced antibodies in 41 of 42 participants and slowed amyloid build-up versus placebo, with three ARIA cases.",
     "https://clinicaltrials.gov/study/NCT02565511"),
    ("Generation Study 2", "Umibecestat", "Cognitively unimpaired ε4 carriers at high risk",
     pill("stop", "Stopped 2019") + " Ended with the rest of the Generation Program.",
     ct("Generation Study 2 umibecestat")),
    ("LX1001", "AAV gene therapy delivering APOE2", "ε4/ε4 with MCI or Alzheimer’s dementia (Phase 1/2)",
     pill("run", "Interim data") + " 15 ε4/ε4 participants across four dose cohorts. Rising APOE2 in spinal fluid, tau PET reduction in 5 of 6 evaluated, no ARIA. FDA Fast Track. Small, open-label.",
     ct("LX1001")),
    ("Clarity AD", "Lecanemab", "Early Alzheimer’s, all genotypes (Phase 3)",
     pill("ok", "Positive") + " Slowed decline. Symptomatic ARIA-E in 9% of ε4/ε4 versus 2% of heterozygotes and 1% of non-carriers; severe ARIA-E in 5% of ε4/ε4.", "https://clinicaltrials.gov/study/NCT03887455"),
    ("TRAILBLAZER-ALZ 2", "Donanemab", "Early Alzheimer’s, all genotypes (Phase 3)",
     pill("ok", "Positive") + " Slowed decline. ARIA-E in 40.6% of ε4/ε4, 22.8% of heterozygotes and 15.7% of non-carriers on donanemab.", "https://clinicaltrials.gov/study/NCT04437511"),
    ("TRAILBLAZER-ALZ 6", "Donanemab, modified dose titration", "Early Alzheimer’s (Phase 3b)",
     pill("ok", "Reported") + " ARIA-E 14% versus 24% with standard dosing; largest reduction in ε4/ε4.", "https://clinicaltrials.gov/study/NCT05738486"),
    ("A4 Study", "Solanezumab", "Cognitively unimpaired with elevated amyloid",
     pill("stop", "No benefit") + " Rich natural-history data on ε4/ε4, including small bleeds over time.", "https://clinicaltrials.gov/study/NCT02008357"),
    ("AHEAD 3-45", "Lecanemab", "Preclinical Alzheimer’s (amyloid without symptoms)",
     pill("run", "Fully enrolled") + " About 1,400 participants; primary completion expected December 2028.", "https://clinicaltrials.gov/study/NCT04468659"),
    ("HT-4253", "HT-4253, oral LRRK2 inhibitor (Halia Therapeutics)", "Biomarker-positive ε4 carriers, prevention (Phase 2a)",
     pill("run", "Not yet recruiting") + " 112 planned. Aims to lower an amyloid risk score in blood.", "https://clinicaltrials.gov/study/NCT07399171"),
]
TRIAL_ASOF = {'APOLLOE4': 'Jul 2026', 'Generation Study 1': 'Dec 2019', 'Generation Study 2': '2019', 'LX1001': 'Jan 2026', 'Clarity AD': '2023', 'TRAILBLAZER-ALZ 2': '2023', 'TRAILBLAZER-ALZ 6': '2025', 'A4 Study': '2023', 'AHEAD 3-45': 'Jun 2026', 'HT-4253': '2026 registry'}
rows = "\n".join(
    f'            <tr><td data-label="Trial"><a href="{link}">{name}</a></td><td data-label="Intervention">{drug}</td><td data-label="Who">{pop}</td><td data-label="Status"><span>{res}</span></td><td class="asof" data-label="As of">{TRIAL_ASOF[name]}</td></tr>'
    for name, drug, pop, res, link in trials)
pages["trials.html"] = head("Clinical trials", "Trials in ε4/ε4 carriers",
    "Trials run only in ε4 homozygotes or carriers, and major trials that report safety and results by genotype.") + f"""
    <section>
      <div class="alleles" role="region" aria-label="Trials" tabindex="0">
        <table class="data">
          <thead><tr><th>Trial</th><th>Intervention</th><th>Who</th><th>Status and result</th><th>As of</th></tr></thead>
          <tbody>
{rows}
          </tbody>
        </table>
      </div>
      <p class="note">Trial status changes often. “As of” is the date of the result or status shown; check each registry entry for the latest. To find trials enrolling now, search <a href="{ct('APOE4')}">ClinicalTrials.gov for APOE4</a>.</p>
    </section>"""

# ---------- Drugs ----------
drugs = [
    ("Approved for early Alzheimer’s", [
        ("Lecanemab (Leqembi)", "Anti-amyloid antibody; IV, with a weekly under-the-skin autoinjector (Leqembi Iqlik) approved in the US in 2025 for maintenance after 18 months",
         "Higher risk of ARIA, including symptomatic and serious ARIA, in ε4/ε4. In the US, a boxed warning applies and APOE testing is advised before treatment; patients who decline testing can still be treated. In the EU (April 2025), approved only for people who are not ε4 homozygotes."),
        ("Donanemab (Kisunla)", "Anti-amyloid antibody, IV",
         "Higher risk of ARIA in ε4/ε4. In the US, a boxed warning applies, APOE testing is advised before treatment, and extra vigilance for ARIA is advised in the first 24 weeks. The FDA approved a slower dose titration that lowered ARIA-E, most in ε4/ε4 (TRAILBLAZER-ALZ 6). In the EU (September 2025), approved only for people who are not ε4 homozygotes."),
        ("Donepezil, rivastigmine, galantamine, memantine", "Symptomatic treatments",
         "Treat symptoms; do not slow the disease. Used regardless of APOE genotype."),
    ]),
    ("Investigational, aimed at ε4/ε4", [
        ("Valiltramiprosate (ALZ-801)", "Oral; blocks formation of toxic amyloid oligomers",
         "Phase 3 APOLLOE4 in ε4/ε4 missed its primary endpoint; a prespecified MCI subgroup favored drug. Low ARIA."),
        ("LX1001", "Gene therapy that adds the protective APOE2 form",
         "Phase 1/2 in ε4/ε4; early biomarker signals, no ARIA in interim data. FDA Fast Track."),
        ("HT-4253", "Oral LRRK2 inhibitor acting on the RAB10 pathway",
         "Phase 2a prevention trial in biomarker-positive ε4 carriers planned; not yet recruiting."),
    ]),
    ("Earlier-stage approaches", [
        ("Anti-APOE antibodies", "Antibodies against aggregated apoE, such as HAE-4",
         "Lower amyloid plaques in APOE4 mice; not yet in clinical trials as far as published reports show."),
        ("APOE4 lowering", "Antisense oligonucleotides and gene silencing",
         "Aim to reduce APOE production; lowering APOE before plaques form reduced amyloid in mice. Preclinical or early development."),
        ("APOE2 plus APOE4 silencing", "Gene therapy (for example Lexeo’s LX1020)",
         "Adds protective APOE2 while suppressing APOE4; preclinical."),
        ("Gene editing", "CRISPR-based conversion of APOE4",
         "Proof-of-concept studies only; efficiency must improve before clinical use."),
    ]),
    ("Stopped or withdrawn", [
        ("Aducanumab (Aduhelm)", "Anti-amyloid antibody", "Discontinued by the manufacturer in 2024."),
        ("Umibecestat (CNP520)", "BACE inhibitor", "Stopped in 2019 in Generation Studies after mild cognitive worsening."),
        ("CAD106", "Active amyloid vaccine", "Generation Study 1 arm halted in 2019 with the rest of the program."),
    ]),
]
body = head("Drugs", "Treatments and what they mean for ε4/ε4",
    "APOE genotype matters most for the safety of anti-amyloid antibodies. Several newer approaches target APOE4 biology directly.")
body += "\n    <section>\n"
for g, items in drugs:
    rows = "\n".join(f'            <tr><td data-label="Drug">{n}</td><td data-label="Type">{t}</td><td data-label="For ε4/ε4">{x}</td></tr>' for n, t, x in items)
    body += f"""    <div class="group">
      <h2>{g}</h2>
      <div class="alleles" role="region" aria-label="{g}" tabindex="0">
        <table class="data">
          <thead><tr><th>Drug</th><th>Type</th><th>For ε4/ε4</th></tr></thead>
          <tbody>
{rows}
          </tbody>
        </table>
      </div>
    </div>
"""
body += DISCLAIMER + "\n    </section>"
pages["drugs.html"] = body

pages["newsletter.html"] = head("Newsletter", "Stay up to date", "Research news on APOE ε4 homozygosity.") + "\n" + NEWSLETTER

OUT.joinpath("style.css").write_text(BASE_CSS.strip() + "\n" + EXTRA_CSS)
for fname, label, title in PAGES:
    OUT.joinpath(fname).write_text(shell(fname, title, pages[fname]))

NOT_FOUND = head("Page not found", "This page doesn’t exist",
    "It may have moved when the site was reorganized.") + """
    <section>
      <div class="prose">
        <p>Try the <a href="index.html">home page</a>, or go straight to <a href="gene.html">Gene and evidence</a>, <a href="resources.html">Resources</a>, <a href="papers.html">Papers</a>, <a href="trials.html">Trials</a> or <a href="drugs.html">Drugs</a>.</p>
      </div>
    </section>"""
OUT.joinpath("robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")
OUT.joinpath("sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{SITE}{'' if f == 'index.html' else f}</loc></url>\n" for f, _, _ in PAGES) + "</urlset>\n")
OUT.joinpath("404.html").write_text(shell("404.html", "Page not found", NOT_FOUND, '\n<meta name="robots" content="noindex">'))
print("built", len(PAGES), "pages")
