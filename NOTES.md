# Profile notes

Working notes for the profile redesign. This file is not shown on the profile page.

## 1. GitHub bio (≤ 160 chars)

Pick one and paste it at **Settings → Public profile → Bio**:

| Option | Text | Chars |
| :-- | :-- | --: |
| **A (recommended)** | `ABAP Cloud & RAP Developer · SAP S/4HANA Public Cloud · BTP side-by-side apps (Kotlin, Python, Java) · AI for ERP with MCP` | 122 |
| B | `SAP Developer: ABAP Cloud, RAP & CDS on S/4HANA Public Cloud. Clean Core inside, side-by-side apps outside. AI for ERP (MCP).` | 125 |
| C | `Systems Analyst @ J.Assy · ABAP Cloud, RAP, CDS · S/4HANA Public Cloud · SAP BTP · Kotlin apps on SAP EWM · AI for ERP (MCP)` | 124 |

Also worth setting: **Company** `J.Assy`, **Location** `Caldas Novas, Goiás, Brazil`,
**Website** `https://www.linkedin.com/in/joaovictor-rvg`.

## 2. Pinned repositories

Right now the pins are coursework (`IF-Goiano-ED1`, `IF-Goiano-ED2`, `IF-Goiano-POO`).
To a SAP recruiter that reads as "student", which undercuts the profile.

**Unpin** all three. Optionally rename them with a `coursework-` prefix, or archive
them (Settings → Danger Zone → Archive) so they're read-only and visibly old, but
still there as proof of CS fundamentals.

**Pin instead**, in this order, as soon as they exist (see section 3):

1. `rap-managed-bo-demo`: the strongest single signal for ABAP Cloud / RAP roles
2. `s4-cds-view-cookbook`
3. `ewm-odata-kotlin-client`
4. `sap-mcp-server-demo` (optional 4th demo, see below)
5. The thesis repo, **only if** IF Goiano and any data owners allow publishing it,
   with all S/4HANA tenant data, URLs and credentials removed
6. One older web/Java project that is clean and documented, to show range

Until the demos exist, pin fewer repos (even zero) rather than coursework.
Empty pins are better than pins that tell the wrong story.

**Archive or make private:** forks you never changed, tutorial clones,
`test`/`hello-world` style repos, and anything with secrets or company names in
the history. Check old commits for `.env` files and API keys before archiving.

## 3. Public demo repositories (zero company code)

All three use only SAP's public demo data (Flight / `/DMO/` reference scenario,
API Business Hub sandbox) or mock data. Nothing from J.Assy.

### a) `rap-managed-bo-demo`: RAP managed business object, end to end
- **What:** a managed RAP BO on the `/DMO/` flight model or a tiny "warehouse task"
  model: CDS root/child entities, behavior definition with validations,
  determinations and actions, draft handling, service definition and binding
  (OData V4), Fiori Elements preview via annotations.
- **Where to run:** SAP BTP ABAP Environment trial (free), pushed with abapGit.
- **README must show:** the data model diagram, the behavior definition, a GIF or
  screenshots of the Fiori Elements app, and *why* each Clean Core decision was made
  (released APIs only, no modifications).
- **Signals:** ABAP Cloud, RAP, CDS, OData V4, Fiori Elements, Clean Core.

### b) `s4-cds-view-cookbook`: CDS patterns for analytics and APIs
- **What:** 10–15 small, documented CDS views on `/DMO/` data: associations vs. joins,
  parameters, aggregations, analytical annotations (`@Analytics.dataCategory`),
  access control (DCL), virtual elements, plus a "performance notes" section
  (pushdown, avoiding runtime errors in large reports).
- **Format:** each view gets a short note "problem → pattern → when not to use it".
- **Signals:** deep CDS knowledge and the report-performance work you do daily,
  without exposing it.

### c) `ewm-odata-kotlin-client`: Kotlin Android app on a mocked EWM OData API
- **What:** a small Android app (Jetpack Compose) that lists warehouse tasks and
  confirms them, consuming an OData service. Back it with a mock server
  (e.g. a JSON/OData mock or the SAP API Business Hub sandbox for the public
  EWM APIs) so it runs for anyone.
- **README:** architecture diagram (app → OData → S/4HANA via Communication
  Arrangement), offline/retry strategy, barcode scanning flow.
- **Signals:** mirrors the RF Warehouse Collector story with fully public code.

### Bonus) `sap-mcp-server-demo`: MCP server for an SAP OData API
- An MCP server exposing a few read-only tools (e.g. "list sales orders",
  "get business partner") over the API Business Hub sandbox, with a demo of an
  LLM client answering natural-language questions. Directly backs the
  "AI for ERP (MCP)" line in your headline.

## 4. Maintenance

- **Edit visuals:** change `tools/build_assets.py`, run `python3 tools/build_assets.py`,
  commit the regenerated `assets/*.svg`.
- **Stats cards blank?** The public github-readme-stats instance is rate limited.
  Self-host instructions are in the HTML comment above the stats section in `README.md`.
- **Certifications:** when you earn a formal SAP certification exam (e.g. *SAP Certified
  Associate – Back-End Developer – ABAP Cloud*), add a Credly badge link. It carries
  more weight than learning journeys.
