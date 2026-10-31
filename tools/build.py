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
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{doc_title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{DESC}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="APOE4 Science">
<meta property="og:title" content="{doc_title}">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{SITE}{'' if fname == 'index.html' else fname}">
<meta property="og:image" content="{SITE}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">{extra_head}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,400;0,600;1,400&family=Public+Sans:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap">
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="wrap">
  <header class="top">
    <a class="mark" href="index.html">apoe<span>4</span>.science</a>
    <nav aria-label="Pages">
{nav}
    </nav>
  </header>
  <main>
{body}
  </main>
  <footer>
    <span>apoe4.science · Maintained by Mahdi Moqri, PhD, in a personal capacity. An educational resource, not medical advice.</span>
    <span class="updated">Last reviewed October 2026</span>
  </footer>
</div>
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
        out.append(f'        <li>{cite} <a href="{link}">Find</a><p class="why">{why}</p></li>')
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
      <div class="geno" aria-label="Genotype epsilon 4 slash epsilon 4">ε4/ε4<small>About 2–3% of people of European ancestry</small></div>
    </div>
    <section>
      <div class="cards">
""" + "\n".join(
    f'        <a class="card" href="{f}"><h3>{t}</h3><p>{d}</p></a>' for f, t, d in cards
) + """
      </div>
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
      </div>
      <p class="note" style="margin-top:20px">Full references are on the <a href="papers.html">Papers</a> page.</p>
    </section>"""

# ---------- Evidence ----------
# ---------- Researchers ----------
pages["resources.html"] = head("Resources", "Where to find ε4/ε4 data",
    "Cohorts and repositories with APOE genotype linked to clinical, biomarker, omic or autopsy data.") + """
    <section>
      <div class="alleles" role="region" aria-label="Data resources" tabindex="0">
        <table class="data">
          <thead><tr><th>Resource</th><th>What it offers for APOE4 research</th><th>Access</th></tr></thead>
          <tbody>
            <tr><td><a href="https://naccdata.org/">NACC</a></td><td>Clinical follow-up and neuropathology from US Alzheimer’s Disease Research Centers, with APOE genotype for most participants. Basis of the Fortea 2024 analysis.</td><td>Online request form</td></tr>
            <tr><td><a href="https://www.niagads.org/">NIAGADS</a></td><td>NIA’s repository for Alzheimer’s genetics, including genome-wide data from the Alzheimer’s Disease Genetics Consortium. Records can be linked to NACC.</td><td>Formal data access request</td></tr>
            <tr><td><a href="https://adsp.niagads.org/">ADSP</a></td><td>Alzheimer’s Disease Sequencing Project: whole-genome sequencing in tens of thousands of people, including diverse ancestries, with harmonized phenotypes.</td><td>Through NIAGADS</td></tr>
            <tr><td><a href="https://ncrad.org/">NCRAD</a></td><td>Stored DNA, plasma, serum and spinal fluid from research-center participants with known outcomes.</td><td>Biosample request</td></tr>
            <tr><td><a href="https://adni.loni.usc.edu/">ADNI</a></td><td>Repeated amyloid and tau PET, MRI, fluid biomarkers and cognition, with APOE genotype.</td><td>Data use agreement</td></tr>
            <tr><td><a href="https://www.a4studydata.org/">A4 Study</a></td><td>Cognitively unimpaired older adults with amyloid PET, repeated MRI including microbleeds, and APOE genotype.</td><td>Data use agreement</td></tr>
            <tr><td><a href="https://adknowledgeportal.synapse.org/">AD Knowledge Portal</a></td><td>Brain multi-omics by genotype (ROSMAP, Mount Sinai, Mayo) and APOE4 knock-in mouse models (MODEL-AD).</td><td>Synapse account and data use certificate</td></tr>
            <tr><td><a href="https://www.ukbiobank.ac.uk/">UK Biobank</a></td><td>About half a million participants with genotypes, plasma proteomics and long-term health records, including a large ε4/ε4 group.</td><td>Approved project application</td></tr>
          </tbody>
        </table>
      </div>
      <p class="note">Each resource sets its own terms. NIH rules on controlled-access genomic data also limit the use of public generative AI tools with individual-level data.</p>
    </section>"""

# ---------- Papers ----------
groups = [
    ("Genetics and risk", [
        ("Corder EH, Saunders AM, Strittmatter WJ, et al. Gene dose of apolipoprotein E type 4 allele and the risk of Alzheimer’s disease in late onset families. <i>Science</i> 1993.",
         "First showed that risk rises and age at onset falls with each ε4 copy.", pm("Corder gene dose apolipoprotein E type 4 allele 1993")),
        ("Strittmatter WJ, Saunders AM, Schmechel D, et al. Apolipoprotein E: high-avidity binding to β-amyloid and increased frequency of type 4 allele in late-onset familial Alzheimer disease. <i>PNAS</i> 1993.",
         "Linked APOE to Alzheimer’s and to amyloid binding.", pm("Strittmatter apolipoprotein E high-avidity binding beta-amyloid 1993")),
        ("Farrer LA, Cupples LA, Haines JL, et al. Effects of age, sex, and ethnicity on the association between apolipoprotein E genotype and Alzheimer disease: a meta-analysis. <i>JAMA</i> 1997.",
         "Classic estimates of risk by genotype, age, sex and ancestry.", pm("Farrer effects of age sex ethnicity apolipoprotein E genotype meta-analysis 1997")),
        ("Genin E, Hannequin D, Wallon D, et al. APOE and Alzheimer disease: a major gene with semi-dominant inheritance. <i>Molecular Psychiatry</i> 2011.",
         "Lifetime risk estimates for ε4/ε4.", pm("Genin APOE Alzheimer disease major gene semi-dominant inheritance")),
        ("Belloy ME, Andrews SJ, Le Guen Y, et al. APOE genotype and Alzheimer disease risk across age, sex, and population ancestry. <i>JAMA Neurology</i> 2023.",
         "Large modern estimates across ancestries.", pm("Belloy APOE genotype Alzheimer disease risk across age sex population ancestry")),
        ("Fortea J, Pegueroles J, Alcolea D, et al. APOE4 homozygosity represents a distinct genetic form of Alzheimer’s disease. <i>Nature Medicine</i> 2024.",
         "Near-full penetrance of pathology and predictable onset in ε4/ε4.", "https://doi.org/10.1038/s41591-024-02931-w"),
    ]),
    ("Amyloid, blood vessels and bleeding", [
        ("Greenberg SM, Rebeck GW, Vonsattel JP, Gomez-Isla T, Hyman BT. Apolipoprotein E ε4 and cerebral hemorrhage associated with amyloid angiopathy. <i>Annals of Neurology</i> 1995.",
         "About 13-fold higher odds of moderate to severe amyloid angiopathy with two ε4 copies.", "https://doi.org/10.1002/ana.410380219"),
        ("Jansen WJ, Ossenkoppele R, Knol DL, et al. Prevalence of cerebral amyloid pathology in persons without dementia: a meta-analysis. <i>JAMA</i> 2015.",
         "Amyloid positivity by age and APOE genotype in people without dementia.", pm("Jansen prevalence cerebral amyloid pathology persons without dementia meta-analysis")),
        ("Montagne A, Nation DA, Sagare AP, et al. APOE4 leads to blood–brain barrier dysfunction predicting cognitive decline. <i>Nature</i> 2020.",
         "A vascular route for APOE4 effects, independent of amyloid and tau.", pm("Montagne APOE4 leads to blood-brain barrier dysfunction predicting cognitive decline")),
        ("Independent effects of white matter lesion volume and APOE ε4 on ARIA-H in the A4 Study. <i>Alzheimer’s &amp; Dementia</i> 2025.",
         "ε4/ε4 predicts accumulating small bleeds in people without symptoms.", "https://pubmed.ncbi.nlm.nih.gov/41085172/"),
    ]),
    ("Mechanisms", [
        ("Shi Y, Yamada K, Liddelow SA, et al. ApoE4 markedly exacerbates tau-mediated neurodegeneration in a mouse model of tauopathy. <i>Nature</i> 2017.",
         "APOE4 worsens tau damage, partly through microglia.", pm("Shi ApoE4 markedly exacerbates tau-mediated neurodegeneration")),
        ("Lin YT, Seo J, Gao F, et al. APOE4 causes widespread molecular and cellular alterations associated with Alzheimer’s disease phenotypes in human iPSC-derived brain cell types. <i>Neuron</i> 2018.",
         "Matched human cell models of APOE3 versus APOE4.", pm("Lin APOE4 causes widespread molecular cellular alterations iPSC-derived brain cell types")),
        ("Blanchard JW, Akay LA, Davila-Velderrain J, et al. APOE4 impairs myelination via cholesterol dysregulation in oligodendrocytes. <i>Nature</i> 2022.",
         "Cholesterol handling and myelin loss in human ε4 brains and cells.", pm("Blanchard APOE4 impairs myelination cholesterol dysregulation oligodendrocytes")),
        ("Haney MS, Pálovics R, Munson CN, et al. APOE4/4 is linked to damaging lipid droplets in Alzheimer’s disease microglia. <i>Nature</i> 2024.",
         "Lipid-laden microglia in ε4/ε4 brains.", pm("Haney APOE4/4 damaging lipid droplets Alzheimer's disease microglia")),
    ]),
    ("Protection and resilience", [
        ("Arboleda-Velasquez JF, Lopera F, O’Hare M, et al. Resistance to autosomal dominant Alzheimer’s disease in an APOE3 Christchurch homozygote: a case report. <i>Nature Medicine</i> 2019.",
         "A rare APOE variant that appears to protect against early-onset disease, pointing to APOE as a drug target.", pm("Arboleda-Velasquez resistance autosomal dominant Alzheimer APOE3 Christchurch homozygote")),
    ]),
    ("Reviews", [
        ("Belloy ME, Napolioni V, Greicius MD. A quarter century of APOE and Alzheimer’s disease: progress to date and the path forward. <i>Neuron</i> 2019.",
         "Broad review of APOE genetics and biology.", pm("Belloy Napolioni Greicius quarter century APOE Alzheimer's disease")),
        ("Yamazaki Y, Zhao N, Caulfield TR, Liu CC, Bu G. Apolipoprotein E and Alzheimer disease: pathobiology and targeting strategies. <i>Nature Reviews Neurology</i> 2019.",
         "Mechanisms and therapeutic approaches.", pm("Yamazaki apolipoprotein E Alzheimer disease pathobiology targeting strategies")),
    ]),
    ("Trial results by genotype", [
        ("van Dyck CH, Swanson CJ, Aisen P, et al. Lecanemab in early Alzheimer’s disease. <i>New England Journal of Medicine</i> 2023.",
         "Clarity AD; ARIA rates reported by APOE genotype.", pm("van Dyck lecanemab in early Alzheimer's disease")),
        ("Sims JR, Zimmer JA, Evans CD, et al. Donanemab in early symptomatic Alzheimer disease: the TRAILBLAZER-ALZ 2 randomized clinical trial. <i>JAMA</i> 2023.",
         "ARIA rates reported by APOE genotype.", pm("Sims donanemab early symptomatic Alzheimer disease TRAILBLAZER-ALZ 2")),
        ("Efficacy and safety of oral valiltramiprosate in APOE4/4 homozygotes with early AD: topline results from the APOLLOE4 Phase 3 trial. 2025.",
         "The first completed Phase 3 trial run only in ε4/ε4.", "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12726020/"),
    ]),
]
body = head("Key papers", "The studies that define what we know",
    "Grouped by topic. “Find” opens the paper or a PubMed search for it.") + "\n    <section>\n"
for g, items in groups:
    body += f'    <div class="group">\n      <h2>{g}</h2>\n{refs(items)}\n    </div>\n'
body += "    </section>"
pages["papers.html"] = body

# ---------- Trials ----------
def pill(kind, text):
    return f'<span class="pill {kind}">{text}</span>'

trials = [
    ("APOLLOE4", "Valiltramiprosate (ALZ-801), oral", "325 ε4/ε4 with early Alzheimer’s (Phase 3)",
     pill("stop", "Missed primary endpoint") + " Prespecified MCI subgroup favored drug (nominal p-values). ARIA-E about 3% in both arms.",
     "https://clinicaltrials.gov/study/NCT04770220"),
    ("Generation Study 1", "Umibecestat (BACE inhibitor) or CAD106 (amyloid vaccine)", "Cognitively unimpaired ε4/ε4, aged 60–75",
     pill("stop", "Stopped 2019") + " Umibecestat arms stopped for mild cognitive worsening; CAD106 arm also halted.",
     "https://clinicaltrials.gov/study/NCT02565511"),
    ("Generation Study 2", "Umibecestat", "Cognitively unimpaired ε4 carriers at high risk",
     pill("stop", "Stopped 2019") + " Ended with the rest of the Generation Program.",
     ct("Generation Study 2 umibecestat")),
    ("LX1001", "AAV gene therapy delivering APOE2", "ε4/ε4 with MCI or Alzheimer’s dementia (Phase 1/2)",
     pill("run", "Interim data 2024") + " Rising APOE2 in spinal fluid, tau PET reduction in 5 of 6, no ARIA. FDA Fast Track. Small, open-label.",
     ct("LX1001")),
    ("Clarity AD", "Lecanemab", "Early Alzheimer’s, all genotypes (Phase 3)",
     pill("ok", "Positive") + " Slowed decline; ARIA most frequent in ε4/ε4.", ct("Clarity AD lecanemab")),
    ("TRAILBLAZER-ALZ 2", "Donanemab", "Early Alzheimer’s, all genotypes (Phase 3)",
     pill("ok", "Positive") + " Slowed decline; ARIA most frequent in ε4/ε4.", ct("TRAILBLAZER-ALZ 2 donanemab")),
    ("TRAILBLAZER-ALZ 6", "Donanemab, modified dose titration", "Early Alzheimer’s (Phase 3b)",
     pill("ok", "Reported") + " ARIA-E 14% versus 24% with standard dosing; largest reduction in ε4/ε4.", ct("TRAILBLAZER-ALZ 6")),
    ("A4 Study", "Solanezumab", "Cognitively unimpaired with elevated amyloid",
     pill("stop", "No benefit") + " Rich natural-history data on ε4/ε4, including small bleeds over time.", ct("A4 solanezumab")),
    ("AHEAD 3-45", "Lecanemab", "Preclinical Alzheimer’s (amyloid without symptoms)",
     pill("run", "Ongoing") + " Prevention trial; check registry for genotype-specific dosing and monitoring.", ct("AHEAD 3-45 lecanemab")),
    ("HT-4253", "HT-4253 (Halia Therapeutics)", "ε4 carriers, prevention (Phase 2)",
     pill("run", "Planned 2026") + " Listed as not yet recruiting.", "https://clinicaltrials.gov/study/NCT07399171"),
]
TRIAL_ASOF = {'APOLLOE4': 'Apr 2025', 'Generation Study 1': 'Dec 2019', 'Generation Study 2': '2019', 'LX1001': 'Oct 2024', 'Clarity AD': '2023', 'TRAILBLAZER-ALZ 2': '2023', 'TRAILBLAZER-ALZ 6': '2025', 'A4 Study': '2023', 'AHEAD 3-45': 'Not verified', 'HT-4253': '2026 registry'}
rows = "\n".join(
    f'            <tr><td><a href="{link}">{name}</a></td><td>{drug}</td><td>{pop}</td><td>{res}</td><td class="asof">{TRIAL_ASOF[name]}</td></tr>'
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
        ("Lecanemab (Leqembi)", "Anti-amyloid antibody, IV or subcutaneous",
         "Higher risk of ARIA in ε4/ε4. In the US, a boxed warning applies and APOE testing is advised before treatment. In the EU, approved only for people who are not ε4 homozygotes."),
        ("Donanemab (Kisunla)", "Anti-amyloid antibody, IV",
         "Higher risk of ARIA in ε4/ε4. A slower dose titration lowered ARIA-E, most in ε4/ε4 (TRAILBLAZER-ALZ 6). In the EU, approved only for people who are not ε4 homozygotes."),
        ("Donepezil, rivastigmine, galantamine, memantine", "Symptomatic treatments",
         "Treat symptoms; do not slow the disease. Used regardless of APOE genotype."),
    ]),
    ("Investigational, aimed at ε4/ε4", [
        ("Valiltramiprosate (ALZ-801)", "Oral; blocks formation of toxic amyloid oligomers",
         "Phase 3 APOLLOE4 in ε4/ε4 missed its primary endpoint; a prespecified MCI subgroup favored drug. Low ARIA."),
        ("LX1001", "Gene therapy that adds the protective APOE2 form",
         "Phase 1/2 in ε4/ε4; early biomarker signals, no ARIA in interim data. FDA Fast Track."),
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
    rows = "\n".join(f"            <tr><td>{n}</td><td>{t}</td><td>{x}</td></tr>" for n, t, x in items)
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
OUT.joinpath("404.html").write_text(shell("404.html", "Page not found", NOT_FOUND, '\n<meta name="robots" content="noindex">'))
print("built", len(PAGES), "pages")
