# AI Agent Guide: Malaysia Inflation Calculator (`malaysia-inflation-calc`)
<!-- Antigravity -->
> **Last Updated:** November 2026  
> **Status:** Active Project  
> **Primary Ground Truth Archive:** [`src/raw_data/`](file:///src/raw_data) 

---

## 1. Project Overview & Architecture

### 1.1 Purpose & Scope
`malaysia-inflation-calc` is a consumer-oriented web application and Progressive Web App (PWA) hosted at [inflation-calc.xkre.me](https://inflation-calc.xkre.me). It calculates the equivalent purchasing power of the Malaysian Ringgit (MYR / RM) between two time periods from 1960 through to the latest available data release.

The application is organized into three sections via [`SectionTabs.vue`](file:///src/components/SectionTabs.vue):
1. **Simple (`/`):** The core year-to-year calculator supporting:
   - **General Headline Inflation (1960 – 2025):** Long-term historical annual inflation rates derived from the World Bank and official DOSM reports.
   - **Consumer Price Index (CPI / IHP) by Division & Region (1960 / 1980 / 2003 / 2010 – 2026):** 13 COICOP 2018 divisions plus Overall CPI published by the Department of Statistics Malaysia (DOSM / *Jabatan Perangkaan Malaysia*), across National (*Malaysia*), 3 macro regions (*Semenanjung*, *Sabah & W.P. Labuan*, *Sarawak* — 2000–2025), and all 16 Malaysian states & federal territories (2010–2026).
   - **Big Mac Index (2000 – 2026):** Unofficial purchasing power indicator based on The Economist Big Mac Index (July / mid-year Malaysia RM releases).
2. **Detailed (`/detailed`, lazy-loaded):** Granular national CPI calculator covering all **329 MCOICOP categories** across three hierarchy tiers (**47 Groups · 3-Digit**, **101 Classes · 4-Digit**, **181 Subclasses · 5-Digit**) from `2010` to `Oct 2026`, with a **Yearly (Avg) / Monthly** granularity toggle, bilingual EN/BM search with match highlighting, cascading dropdowns, interactive progression line chart, and parent/headline benchmark comparison.
3. **Advanced (`Soon`):** Disabled placeholder tab reserved for future multi-basket and advanced analysis features.

### 1.2 Technology Stack
- **Framework:** Vue 3 (Composition API with `<script setup lang="ts">`)
- **Language:** TypeScript 4.9+ (`vue-tsc` for strict typechecking)
- **Build Tool:** Vite 3 (code-split lazy route + dynamic monthly chunk)
- **Styling:** Tailwind CSS 3.4 (`@tailwindcss/forms`), SCSS
- **PWA Support:** `vite-plugin-pwa` (Workbox offline service worker precaching split chunks)
- **Analytics:** `vue-matomo`
- **Python Processing Engine:** Python 3.15+ (`openpyxl`, `msoffcrypto-tool`, `pypdf`, `pandas`, `numpy`) for raw DOSM extraction, [`scripts/generate_detailed_cpi.py`](file:///scripts/generate_detailed_cpi.py) (stdlib-only) for Detailed JSON generation, and [`scripts/generate_cpi_workbook.py`](file:///scripts/generate_cpi_workbook.py) (`openpyxl`) for building the downloadable master `CpiDataset.xlsx` workbook.

### 1.3 Repository Directory Layout
```text
malaysia-inflation-calc/
├── AGENTS.md                   # Master instructions for AI agents (this file)
├── package.json                # Project dependencies and npm scripts
├── vite.config.ts              # Vite configuration (PWA, Vue plugin, path aliases @/*)
├── tsconfig.json               # TypeScript path alias (@/* -> src/*)
├── tailwind.config.js          # Tailwind CSS design system configuration
├── index.html                  # HTML entry point with meta tags
│
├── scripts/
│   ├── generate_detailed_cpi.py # Reproducible generator for Detailed 3D/4D/5D JSON datasets
│   └── generate_cpi_workbook.py # Builds 11-sheet CpiDataset.xlsx from frontend data & syncs public/
│
├── public/                     # Static assets served as-is
│   ├── favicon.ico
│   ├── Web.config              # IIS history-mode rewrite rules for /, /detailed, etc.
│   └── data/
│       └── CpiDataset.xlsx     # Downloadable 11-sheet Excel workbook synced from src/raw_data/CpiDataset.xlsx
│
├── src/
│   ├── main.ts                 # Vue app mount, Vue Router registration & Matomo setup
│   ├── App.vue                 # App shell layout (MainHeader, SectionTabs, RouterView, DataSource)
│   ├── router.ts               # Vue Router configuration (/, /detailed lazy route, fallback)
│   │
│   ├── views/                  # Route-level page views
│   │   ├── SimpleCalculatorView.vue   # Simple section wrapper (Calculator + DetailedInfo)
│   │   └── DetailedCalculatorView.vue # Lazy-loaded Detailed section + URL state syncing
│   │
│   ├── assets/                 # Styles, brand logos & bundled datasets
│   │   ├── style.scss
│   │   └── data/               # Bundled TypeScript & generated JSON datasets
│   │       ├── cpiMalaysia.ts      # National CPI by division (1960-2026)
│   │       ├── cpiSemenanjung.ts   # Peninsular Malaysia CPI by division (2000-2025)
│   │       ├── cpiSabahLabuan.ts   # Sabah & Labuan CPI by division (2000-2025)
│   │       ├── cpiSarawak.ts       # Sarawak CPI by division (2000-2025)
│   │       ├── cpiStates.ts        # 16 Malaysian states & FTs CPI by division (2010-2026)
│   │       ├── inflation.ts        # General annual inflation rates (1960-2025)
│   │       ├── index.ts            # Barrel exports for Simple datasets
│   │       ├── misc/
│   │       │   └── bigMacIndex.ts  # Big Mac price index in RM (2000-2026)
│   │       └── detailed/           # Generated by scripts/generate_detailed_cpi.py
│   │           ├── mcoicopTree.json        # 13 Divisions + 329 3D/4D/5D nodes (EN/BM, year/month bounds)
│   │           ├── cpiDetailedAnnual.json  # Annual average CPI (2010-2026) + YTD metadata
│   │           └── cpiDetailedMonthly.json # Lazy-loaded monthly CPI (2010-01 to 2026-10)
│   │
│   ├── components/             # UI Components
│   │   ├── SectionTabs.vue         # 3-section switcher (Simple / Detailed / disabled Advanced)
│   │   ├── Calculator.vue          # Simple calculator form, inputs, and result card
│   │   ├── DataSource.vue          # Route-aware citations and links to official data portals
│   │   ├── MainHeader.vue          # Navigation bar and header banner
│   │   ├── DetailedInfo.vue        # Shared collapsible "More Info" panel wrapper
│   │   ├── ReloadPrompt.vue        # PWA update prompt
│   │   ├── Detailed/               # Detailed section UI
│   │   │   ├── DetailedCalculator.vue # Yearly/Monthly toggle, inputs & out-of-range recovery
│   │   │   └── McoicopPicker.vue      # Highlighted EN/BM/code search + cascading 3D/4D/5D selects
│   │   └── Info/                   # Expanded breakdown cards & progression charts
│   │       ├── CpiInfo.vue            # Simple CPI/Big Mac KPI summary + line chart
│   │       ├── InflationInfo.vue      # General inflation KPI summary, chart & yearly table
│   │       ├── DetailedCpiInfo.vue    # Detailed KPI summary, chart & parent/overall benchmark
│   │       └── InflationLineChart.vue # Reusable interactive SVG line chart (yearly & monthly)
│   │
│   ├── services/               # Core business logic & computations
│   │   ├── inflationService.ts         # Simple purchasing power math & progression series
│   │   ├── detailedInflationService.ts # Detailed 3D/4D/5D lookups, async monthly load, EN/BM search, CAGR
│   │   └── routeService.ts             # Dynamic URL query parameter reader
│   │
│   ├── state/                  # Reactive application state
│   │   ├── calculatorState.ts         # Simple calculator state (isolated from /detailed URL params)
│   │   ├── detailedCalculatorState.ts # Detailed state (granularity, code, year/month) + /detailed URL sync
│   │   ├── routeState.ts              # Simple route query param watcher
│   │   └── infoState.ts               # Shared "More Info" panel visibility
│   │
│   ├── types/                  # TypeScript interfaces and Enums
│   │   ├── InflatitonTypeEnum.ts # Enum for Simple inflation types (General, TotalCPI, Food...)
│   │   ├── malaysiaPartEnum.ts   # Enum for regions & 16 states
│   │   ├── detailedCpi.ts        # Types for MCOICOP tree, 3D/4D/5D datasets, Yearly/Monthly modes
│   │   ├── chart.ts              # Shared ChartPoint interface for InflationLineChart
│   │   ├── data.d.ts             # Type definitions for CPIData, CPIDataset, InflationDataset
│   │   ├── route.d.ts            # Simple RouteState query contract
│   │   └── inflation.d.ts
│   │
│   └── raw_data/               # Official DOSM primary publications & master generated datasets
│       ├── cpi_2d_annual.csv   # Official DOSM Open Data annual series (1960-2025)
│       ├── cpi_2d_state.csv    # Official DOSM Open Data 16-state monthly series (2010-2026)
│       ├── cpi_2d.csv          # Official DOSM Open Data national 2-digit monthly series (1980-2026)
│       ├── cpi_3d.csv          # Official DOSM Open Data 3-digit group series (47 groups, 2010-2026)
│       ├── cpi_4d.csv          # Official DOSM Open Data 4-digit class series (101 classes, 2010-2026)
│       ├── cpi_5d.csv          # Official DOSM Open Data 5-digit subclass series (181 subclasses, 2010-2026)
│       ├── mcoicop.csv         # Official DOSM MCOICOP 2018 classification dictionary (343 entries)
│       ├── big-mac-full-index.csv # The Economist official Big Mac Index global CSV (Malaysia 2000–Jul 2026)
│       ├── AGENTS.md           # Raw data extraction guide (from conversation 2bb718e8-7de5-478b-9afa-613bf83d3fe7)
│       ├── 2010/ to 2026/      # Raw monthly Excel/PDF releases & annual summaries from DOSM
│       ├── CPI_Dataset_Complete.xlsx  # Master verified 6-tab multi-series workbook (2010–Oct 2026)
│       ├── cpi_dataset_monthly.csv    # Long/tidy format (2,660 records, 202 consecutive months)
│       ├── cpi_dataset_monthly_wide.csv# Wide format (202 monthly rows x 14 COICOP groups)
│       ├── cpi_dataset_annual.csv     # Annual indices & YoY rates (1,105 records, 2000–2025)
│       ├── cpi_dataset.json           # Structured JSON dataset for programmatic access
│       ├── CPI Raw.xlsx               # Populated working workbook (Detailed 2016–2026 + MCOICOP Dictionary + 3D/4D/5D sheets)
│       ├── CpiDataset.xlsx            # Master 11-sheet downloadable workbook mirroring all frontend data (synced to public/data/)
│       └── CpiDataset_legacy_backup.xlsx # Archived pre-v2 CpiDataset.xlsx backup
```

---

## 2. Core Inflation Calculation Mathematics

Simple calculation logic resides in [`src/services/inflationService.ts`](file:///src/services/inflationService.ts), and Detailed 3D/4D/5D calculation logic resides in [`src/services/detailedInflationService.ts`](file:///src/services/detailedInflationService.ts).

### 2.1 Basket / Category CPI & Big Mac (Relative Price Formula)
For any category where index numbers are provided (Simple divisions, Detailed 3D/4D/5D Yearly averages or exact Monthly indices, or Big Mac Index):

$$\text{Equivalent Value in } \text{Period}_2 = \text{Value}_1 \times \left( \frac{\text{CPI}_{\text{Period}_2}}{\text{CPI}_{\text{Period}_1}} \right)$$

*Note:* If index data is missing for either year, `inflationService.getCPIRate()` throws `'No Data'`. In Detailed mode (`getAnnualCPI` / `getMonthlyCPI`), missing periods return `{ cpi1, cpi2 }` without `rate` so the UI can display a one-click date-range recovery action.

### 2.2 General Historical Inflation (Compounding Formula)
For general inflation (1960 – 2025), where annual percentage rates $\pi_y$ are recorded:

- **Forward Calculation ($\text{Year}_2 > \text{Year}_1$):**
  $$C = \prod_{y = \text{Year}_1 + 1}^{\text{Year}_2} \left(1 + \frac{\pi_y}{100}\right)$$
  $$\text{Value}_2 = \text{Value}_1 \times C$$

- **Backward Calculation ($\text{Year}_2 < \text{Year}_1$):**
  $$C = \prod_{y = \text{Year}_1}^{\text{Year}_2 + 1} \left(1 - \frac{\pi_y}{100}\right)$$
  $$\text{Value}_2 = \text{Value}_1 \times C$$

### 2.3 Annualised Rate (CAGR) & `More Info` Progression
In `More Info` ([`CpiInfo.vue`](file:///src/components/Info/CpiInfo.vue), [`InflationInfo.vue`](file:///src/components/Info/InflationInfo.vue), [`DetailedCpiInfo.vue`](file:///src/components/Info/DetailedCpiInfo.vue)), when the absolute span between $\text{Period}_1$ and $\text{Period}_2$ is at least 1 year (12 months in Monthly mode), the Compound Annual Growth Rate is displayed:

$$\text{CAGR} = \left( \left(\frac{\text{Index}_2}{\text{Index}_1}\right)^{\frac{1}{|\Delta t_{\text{years}}|}} - 1 \right) \times 100$$

### 2.4 Month-on-Month (MoM) and Year-on-Year (YoY) Formulations
When extracting or verifying new monthly data points from DOSM releases:

$$MoM_t = \left(\frac{I_t - I_{t-1}}{I_{t-1}}\right) \times 100$$

$$YoY_t = \left(\frac{I_t - I_{t-12}}{I_{t-12}}\right) \times 100$$

$$\text{Annual Average Index } I_{annual} = \frac{1}{12} \sum_{m=1}^{12} I_m$$

---

## 3. Ground Truth Data Architecture & Official Data Sources (`src/raw_data/`)

In addition to the historical repository compiled from DOSM monthly Excel and PDF releases, the authoritative machine-readable Open Data feeds are obtained directly from OpenDOSM:

### 3.1 Direct OpenDOSM Storage Feeds & Portals
- **National Annual CPI (2D):** [`https://storage.dosm.gov.my/cpi/cpi_2d_annual.csv`](https://storage.dosm.gov.my/cpi/cpi_2d_annual.csv) (Format: `YYYY-01-01`, 1960–2025)
  - Data Catalogue Portal: [Annual CPI by Division (2-digit) | OpenDOSM](https://open.dosm.gov.my/data-catalogue/cpi_annual)
- **Monthly State CPI (2D):** [`https://storage.dosm.gov.my/cpi/cpi_2d_state.csv`](https://storage.dosm.gov.my/cpi/cpi_2d_state.csv) (Format: `YYYY-MM-01`, 2010–present across 16 states)
  - Data Catalogue Portal: [Monthly CPI by State & Division (2-digit) | OpenDOSM](https://open.dosm.gov.my/data-catalogue/cpi_state)
- **National Monthly CPI (2D):** [`https://storage.dosm.gov.my/cpi/cpi_2d.csv`](https://storage.dosm.gov.my/cpi/cpi_2d.csv) (Format: `YYYY-MM-01`, 1980–present across 14 divisions)
- **CPI by 3-Digit Group (3D):** [`https://storage.dosm.gov.my/cpi/cpi_3d.csv`](https://storage.dosm.gov.my/cpi/cpi_3d.csv) (Format: `YYYY-MM-01`, 47 groups, 2010–present)
  - Data Catalogue Portal: [`https://data.gov.my/data-catalogue/cpi_3d`](https://data.gov.my/data-catalogue/cpi_3d)
- **CPI by 4-Digit Class (4D):** [`https://storage.dosm.gov.my/cpi/cpi_4d.csv`](https://storage.dosm.gov.my/cpi/cpi_4d.csv) (Format: `YYYY-MM-01`, 101 classes, 2010–present)
  - Data Catalogue Portal: [`https://data.gov.my/data-catalogue/cpi_4d`](https://data.gov.my/data-catalogue/cpi_4d)
- **CPI by 5-Digit Subclass (5D):** [`https://storage.dosm.gov.my/cpi/cpi_5d.csv`](https://storage.dosm.gov.my/cpi/cpi_5d.csv) (Format: `YYYY-MM-01`, 181 subclasses, 2010–present)
  - Data Catalogue Portal: [`https://data.gov.my/data-catalogue/cpi_5d`](https://data.gov.my/data-catalogue/cpi_5d)
- **MCOICOP Dictionary:** [`https://storage.dosm.gov.my/dictionaries/mcoicop.csv`](https://storage.dosm.gov.my/dictionaries/mcoicop.csv) (343 classification entries with EN/BM descriptions)

### 3.2 Official Publication Endpoints & Formats
- **Monthly Publications:**
  - PDF: `https://storage.dosm.gov.my/cpi/cpi_YYYY-MM.pdf` (e.g. `cpi_2026-10.pdf`)
  - Headline Main: `https://storage.dosm.gov.my/cpi/cpi_YYYY-MM_main.xlsx` (e.g. `cpi_2026-10_main.xlsx`)
  - State: `https://storage.dosm.gov.my/cpi/cpi_YYYY-MM_state.xlsx` (e.g. `cpi_2026-10_state.xlsx`)
  - Core: `https://storage.dosm.gov.my/cpi/cpi_YYYY-MM_core.xlsx` (e.g. `cpi_2026-10_core.xlsx`)
  - Portal: `https://open.dosm.gov.my/publications/cpi_YYYY-MM` (e.g. [[Oct 2026] Consumer Price Index | OpenDOSM](https://open.dosm.gov.my/publications/cpi_2026-10))
- **Annual Publications:**
  - Annual Excel: `https://storage.dosm.gov.my/cpi/cpi_annual_YYYY.xlsx` (e.g. `cpi_annual_2025.xlsx`)
  - Annual PDF: `https://storage.dosm.gov.my/cpi/cpi_annual_YYYY.pdf` (e.g. `cpi_annual_2025.pdf`)
  - Portal: `https://open.dosm.gov.my/publications/cpi_annual_YYYY` (e.g. [[2025] Consumer Price Index | OpenDOSM](https://open.dosm.gov.my/publications/cpi_annual_2025))

### 3.3 Historical Compilation & Directory Architecture

In conversation `2bb718e8-7de5-478b-9afa-613bf83d3fe7`, the raw DOSM repository was audited, corrected, standardized, and compiled into the authoritative datasets now housed in [`src/raw_data/`](file:///src/raw_data).

### 3.4 Standardized File Naming Scheme (2017 – 2026)
Every folder from `2017/` to `2026/` follows a unified naming convention:

| File Pattern | Content & Type | Usage |
| :--- | :--- | :--- |
| `cpi_YYYY-MM_main.xlsx` | **Headline CPI** by main COICOP groups | Authoritative source for Headline National CPI |
| `cpi_YYYY-MM_core.xlsx` | **Core CPI** (*Indeks Teras*) | Excludes fresh food & administered items |
| `cpi_YYYY-MM_state.xlsx` | **State/Regional CPI** | Source for Semenanjung, Sabah, Sarawak |
| `cpi_YYYY-MM.pdf` | Monthly press release / bulletin | Official published text & tables |
| `cpi_annual_YYYY.{pdf,xlsx}` | Annual summary report & tables | Official yearly averages (available 2020–2025) |

### 3.5 Key DOSM Tables & Extraction Coordinates

| Period | Primary File | Table / Sheet | Notes |
| :--- | :--- | :--- | :--- |
| **2010** | `2011/02Malaysia.pdf` | Jadual 5 (p. 14 / index 13) | Text parsing ($2010=100$) |
| **2011 – 2012** | `2012/02Malaysia.pdf` | Jadual 5 (p. 14) | Text parsing |
| **2013 – 2014** | `2014/02Malaysia.pdf` | Jadual 5 (p. 14) | Text parsing |
| **2015 – 2016** | `2016/CPI December 2016.pdf` | Jadual 5 (p. 36 / index 35) | Text parsing |
| **2017 – 2018** | `2018/cpi_2018-12_main.xlsx` | `J5` | **Encrypted** with default password `VelvetSweatshop` |
| **2019 – 2020** | `2020/cpi_2020-12_main.xlsx` | `J5` | 13 columns (12 COICOP 1999 groups) |
| **2021 – 2022** | `2022/cpi_2022-12_main.xlsx` | `J5A` | Sheet name is `J5A` (not `J5`) |
| **2023** | `2024/cpi_2024-05_main.xlsx` | `J5` | 14 columns (COICOP 2018 shift) |
| **2024 – 2025** | `2025/cpi_2025-12_main.xlsx` | `J5` | 14 columns (13 COICOP 2018 groups) |
| **2026 (Jan–Oct)** | `2026/cpi_2026-10_main.xlsx` | `J5` | Latest published release (through October 2026) |

### 3.6 Regional Data Row Offsets (`*_state.xlsx` -> Sheet `IN_J3`)
When reading state and regional indices from sheet `IN_J3`:
- **Semenanjung (Peninsular Malaysia):** Row 11 across all years.
- **Sabah & W.P. Labuan:** Row 407 (up to 2025) $\rightarrow$ **shifted to Row 389 in 2026**.
- **Sarawak:** Row 437 (up to 2025) $\rightarrow$ **shifted to Row 417 in 2026**.

> [!WARNING]
> Row offsets for Sabah and Sarawak shifted upward in 2026 files. Always inspect or search the region name column before hardcoding row indices.

### 3.7 Decrypting Protected 2017–2018 Excel Spreadsheets
The official `.xlsx` files distributed by DOSM for 2017 and 2018 were protected with Excel's default read-only package password (`VelvetSweatshop`). Use Python's `msoffcrypto` library to open them:
```python
import io, msoffcrypto, openpyxl

with open(file_path, "rb") as f:
    office_file = msoffcrypto.OfficeFile(f)
    office_file.load_key(password="VelvetSweatshop")
    decrypted = io.BytesIO()
    office_file.decrypt(decrypted)
    wb = openpyxl.load_workbook(decrypted, data_only=True)
```

---

## 4. Critical Domain Gotchas & Auditing Discoveries

Agents must adhere strictly to these rules discovered during project audits:

### 1. Headline CPI vs. Core CPI (Critical Bug Prevention)
- **Headline CPI (*IHP Keseluruhan*):** Stored in `cpi_YYYY-MM_main.xlsx`. Encompasses all items in the consumer basket.
- **Core CPI (*Indeks Teras*):** Stored in `cpi_YYYY-MM_core.xlsx`. Excludes volatile fresh food and administered prices. In Core CPI sheets, *Alcoholic Beverages & Tobacco* is omitted and appears as `'-'`.
- **Historical Gotcha:** In commit `0c32d6d`, numbers for 2024 and 2025 were mistakenly copied from `cpi_2025-12_core.xlsx` into `src/assets/data/cpiMalaysia.ts`. This caused:
  - 2024 Headline Average to be recorded as **131.2** instead of the official **132.8**.
  - 2025 Headline Average to be recorded as **133.8** instead of the official **134.6**.
  - `alcoholTobacco` to be omitted.
- **Rule:** Never use `core.xlsx` for headline or category CPI datasets.

### 2. The 2024 UN COICOP 2018 Reclassification
Starting in January 2024, DOSM migrated from COICOP 1999 (12 main groups) to COICOP 2018 (13 main groups):
- **2000 – 2023:** Group 12 was *Miscellaneous Goods & Services* (*Pelbagai Barangan & Perkhidmatan*), including personal care, social care, and financial services.
- **2024 – Present:**
  - **Group 12:** *Insurance & Financial Services* (*Insurans & Perkhidmatan Kewangan*).
  - **Group 13:** *Personal Care, Social Protection & Miscellaneous Goods & Services* (*Penjagaan Diri, Perlindungan Sosial & Pelbagai Barangan & Perkhidmatan*).

### 3. Detailed Expenditure Classes (`Detailed`, `Detailed (COICOP 2018)`, `Detailed 3D/4D/5D`)
In [`src/raw_data/CPI Raw.xlsx`](file:///src/raw_data/CPI%20Raw.xlsx), the `Detailed` sheet (COICOP 2018 block backfilled 2016–Oct 2026), `Detailed (COICOP 2018)` (Jan 2024–Oct 2026), `MCOICOP Dictionary`, `Detailed 3D (Groups)` (47 groups, 2010–Oct 2026), `Detailed 4D (Classes)` (101 classes, 2010–Oct 2026), and `Detailed 5D (Subclasses)` (181 subclasses, 2010–Oct 2026) capture full granular indices with active `=AVERAGE(...)` yearly formulas matching published annual totals:
- 2024 Annual Average: **132.8**
- 2025 Annual Average: **134.6**
- 2026 YTD (Jan–Oct): **136.9** (latest single month Oct 2026: **137.7**)

### 4. Detailed 3D/4D/5D MCOICOP & Frontend Architecture Gotchas
- **Code Prefix Anomaly (`001` under Division `01`):** Group `001` (*Food away from home*) belongs to Division `01` (*Food & Beverages*), even though its code begins with `00`. Always derive parent-child links from [`mcoicop.csv`](file:///src/raw_data/mcoicop.csv) columns (`division`, `group`, `class`, `subclass`), never string slicing.
- **Single-Child Passthrough Exception (`0444` vs `04441`):** Most 1-child Groups/Classes with identical names have identical CPI series, **except** Class `0444` (*Other services relating to the dwelling n.e.c.*) vs Subclass `04441` (*Maintenance charges in multi-occupied buildings*), which diverge by up to `19.90` index points. [`scripts/generate_detailed_cpi.py`](file:///scripts/generate_detailed_cpi.py) only sets `hasDistinctChildren: false` when a single child matches both name **and** all monthly values (`<= 0.01`), so `0444 → 04441` and `0230 → 02301 Cigarettes` remain selectable.
- **Newer Series Start Dates (2016 / 2018 / 2024):** While 309/329 Detailed series begin in `2010-01`, 20 newer series start later (3 in `2016-01`, 1 in `2018-01`, 16 in `2024-01`, with zero internal gaps). [`DetailedCalculator.vue`](file:///src/components/Detailed/DetailedCalculator.vue) shows an inline availability notice with a one-click recovery button whenever the selected period precedes a series start date.
- **National-Only Scope & Partial-Year YTD Cap:** OpenDOSM 3D/4D/5D feeds are published at the National Malaysia level only (no state breakdown). In Monthly mode, [`DetailedCalculator.vue`](file:///src/components/Detailed/DetailedCalculator.vue) reads `meta.ytdYear` and `meta.ytdMonths` from [`cpiDetailedAnnual.json`](file:///src/assets/data/detailed/cpiDetailedAnnual.json) to disable unavailable future months (e.g., `Nov`–`Dec` in `2026`) and annotate YTD averages.
- **Bundle Splitting & CSS Pitfalls:** Keep [`detailedCalculatorState.ts`](file:///src/state/detailedCalculatorState.ts) and [`detailedInflationService.ts`](file:///src/services/detailedInflationService.ts) imported only inside the lazy `/detailed` route tree (and load [`DetailedCpiInfo.vue`](file:///src/components/Info/DetailedCpiInfo.vue) via `defineAsyncComponent`, and [`cpiDetailedMonthly.json`](file:///src/assets/data/detailed/cpiDetailedMonthly.json) via dynamic `import()`) so Simple (`/`) loads zero Detailed CPI data. Also note global `a:hover { @apply underline; }` in [`src/assets/style.scss`](file:///src/assets/style.scss) affects `<router-link>`; [`SectionTabs.vue`](file:///src/components/SectionTabs.vue) overrides this explicitly with `!no-underline hover:!no-underline`.

---

## 5. State of Frontend Data vs. Raw Data Ground Truth

All primary national, state, and detailed 3D/4D/5D frontend datasets are synced with OpenDOSM ground truth:

| Dimension | `src/raw_data/` (Ground Truth) | `src/assets/data/` (Frontend) | Status |
| :--- | :--- | :--- | :--- |
| **National Annual & 13 Divisions** | `cpi_2d_annual.csv` + `cpi_2d.csv` (1960–Oct 2026) | [`cpiMalaysia.ts`](file:///src/assets/data/cpiMalaysia.ts) (1960–2026, incl. `alcoholTobacco` & `insurance`) | **Synced** |
| **General Headline Inflation** | World Bank + DOSM (1960–2025) | [`inflation.ts`](file:///src/assets/data/inflation.ts) (1960–2025) | **Synced** |
| **16 States & Federal Territories** | `cpi_2d_state.csv` (2010–Oct 2026) | [`cpiStates.ts`](file:///src/assets/data/cpiStates.ts) (2010–2026) | **Synced** |
| **Macro Regions (Semenanjung, Sabah & Labuan, Sarawak)** | `cpi_YYYY-MM_state.xlsx` (through Oct 2026) | [`cpiSemenanjung.ts`](file:///src/assets/data/cpiSemenanjung.ts), [`cpiSabahLabuan.ts`](file:///src/assets/data/cpiSabahLabuan.ts), [`cpiSarawak.ts`](file:///src/assets/data/cpiSarawak.ts) (2000–2025) | **Synced through 2025** (2026 YTD pending if macro regions are extended) |
| **Detailed 3D / 4D / 5D (329 series)** | `mcoicop.csv` + `cpi_3d.csv`, `cpi_4d.csv`, `cpi_5d.csv` (2010-01–2026-10) | [`src/assets/data/detailed/`](file:///src/assets/data/detailed) (`mcoicopTree.json`, `cpiDetailedAnnual.json`, `cpiDetailedMonthly.json`) | **Synced** (generated via [`scripts/generate_detailed_cpi.py`](file:///scripts/generate_detailed_cpi.py)) |
| **Big Mac Index** | `big-mac-full-index.csv` (The Economist, 2000–2026) | [`bigMacIndex.ts`](file:///src/assets/data/misc/bigMacIndex.ts) (2000–2026) | **Synced** |

### 5.1 Detailed JSON Artifacts (`src/assets/data/detailed/`)
Generated deterministically from [`src/raw_data/`](file:///src/raw_data) by [`scripts/generate_detailed_cpi.py`](file:///scripts/generate_detailed_cpi.py):
- [`mcoicopTree.json`](file:///src/assets/data/detailed/mcoicopTree.json): `13` 2D Divisions + `329` 3D/4D/5D nodes (`code`, `digits`, `division`, `group`, `classCode`, `descEn`, `descBm`, `minYear`, `maxYear`, `minMonth`, `maxMonth`, `hasDistinctChildren`).
- [`cpiDetailedAnnual.json`](file:///src/assets/data/detailed/cpiDetailedAnnual.json): `meta` (`minYear`, `maxYear`, `latestMonth`, `ytdYear`, `ytdMonths`), `overall` benchmark annual means, and `series` annual means (`round(mean(...), 2)`).
- [`cpiDetailedMonthly.json`](file:///src/assets/data/detailed/cpiDetailedMonthly.json): Compact `[startIdx, values]` tuple per code indexed against `meta.dates` (`["2010-01", ..., "2026-10"]`), plus `overall` benchmark monthly tuple.

### 5.2 Downloadable Master Workbook (`CpiDataset.xlsx`)
Generated directly from [`src/assets/data/`](file:///src/assets/data) by [`scripts/generate_cpi_workbook.py`](file:///scripts/generate_cpi_workbook.py) so end-user exports match the web calculator 100%, written to [`src/raw_data/CpiDataset.xlsx`](file:///src/raw_data/CpiDataset.xlsx) and synced byte-for-byte to [`public/data/CpiDataset.xlsx`](file:///public/data/CpiDataset.xlsx) (which is linked by [`DataSource.vue`](file:///src/components/DataSource.vue) via Office Web Viewer):
- **11 User-Facing Worksheets** (color-coded tabs, frozen panes, AutoFilters, explicit column widths, text-formatted `@` MCOICOP codes to preserve leading zeros):
  1. `Overview` — metadata summary, clickable internal TOC links, methodology notes, and official source URLs.
  2. `General Inflation` — `1960–2025` annual `%` rates and live `1960 = 100` compounded price index formulas.
  3. `National CPI (2D)` — `1960–2026` Overall CPI + 13 Divisions (`2026` flagged `Jan–Oct YTD`).
  4. `Regional CPI (2D)` — *Semenanjung Malaysia*, *Sabah & W.P. Labuan*, and *Sarawak* (`2000–2025`).
  5. `State CPI (2D)` — all 16 Malaysian States & Federal Territories (`2010–2026`).
  6. `Big Mac Index` — `2000–2026` menu prices (RM) with live YoY `%` formulas.
  7. `MCOICOP Dictionary` — `342` categories (`13` Divisions + `47` Groups + `101` Classes + `181` Subclasses) sorted hierarchically with EN/BM names and month bounds.
  8. `Detailed Annual (3D-5D)` — `Overall` benchmark + all `329` 3D/4D/5D annual averages (`2010–2026`).
  9. `Detailed Monthly 3D` — `Overall` + `47` 3-Digit Groups across `202` months (`Jan 2010 – Oct 2026`).
  10. `Detailed Monthly 4D` — `Overall` + `101` 4-Digit Classes across `202` months (`Jan 2010 – Oct 2026`).
  11. `Detailed Monthly 5D` — `Overall` + `181` 5-Digit Subclasses across `202` months (`Jan 2010 – Oct 2026`).
- **Legacy Archive:** The original pre-enhancement workbook is preserved at [`src/raw_data/CpiDataset_legacy_backup.xlsx`](file:///src/raw_data/CpiDataset_legacy_backup.xlsx) alongside `CpiDataset_backup.xlsx`.

### 5.3 Route-Scoped URL Query Parameters
- **Simple (`/`):** `?y1=<year1>&y2=<year2>&v1=<value1>&i=<InflationType>&p=<MalaysiaPart>&s=<0|1>`
- **Detailed (`/detailed`, Yearly):** `?g=y&y1=<year1>&y2=<year2>&v1=<value1>&c=<mcoicopCode>&s=<0|1>`
- **Detailed (`/detailed`, Monthly):** `?g=m&y1=<year1>&m1=<1..12>&y2=<year2>&m2=<1..12>&v1=<value1>&c=<mcoicopCode>&s=<0|1>`

### 5.4 Simple Field Mapping Reference (`cpi_dataset_monthly_wide.csv` $\rightarrow$ `CPIData` Interface)
```typescript
interface CPIData {
  total: number;            // cpi_total
  food: number;             // cpi_01_food
  alcoholTobacco?: number;  // cpi_02_alcohol_tobacco
  clothing: number;         // cpi_03_clothing
  housing: number;          // cpi_04_housing
  furnishing: number;       // cpi_05_furnishings
  health: number;           // cpi_06_health
  transport: number;        // cpi_07_transport
  communication: number;    // cpi_08_communication
  recreative: number;       // cpi_09_recreation
  education: number;        // cpi_10_education
  restaurantHotels?: number;// cpi_11_restaurants_hotels
  misc: number;             // cpi_12_misc (2010-2023) or cpi_13_personal_care_misc (2024+)
  insurance?: number;       // cpi_12_insurance_financial (2024+)
}
```

---

## 6. Developer & AI Agent Workflows

### 6.1 Running the Frontend Application
On Windows, PowerShell execution policy may restrict direct `npm` script invocation. Always invoke through `cmd /c` if necessary:
```powershell
# Install dependencies
cmd /c "npm install"

# Start Vite dev server (runs on http://localhost:5173)
cmd /c "npm run dev"

# Run type check and production build
cmd /c "npm run build"

# Preview production build locally
cmd /c "npm run serve"
```

### 6.2 Python Extraction & Dataset Generation
Python 3.15 is installed in the local environment. Required packages for raw Excel/PDF extraction:
```powershell
pip install openpyxl msoffcrypto-tool pypdf pandas numpy
```

To regenerate the Detailed 3D/4D/5D frontend JSON files from [`src/raw_data/`](file:///src/raw_data) (`mcoicop.csv`, `cpi_2d.csv`, `cpi_3d.csv`, `cpi_4d.csv`, `cpi_5d.csv`), run the stdlib-only generator from the project root:
```powershell
python scripts/generate_detailed_cpi.py
```

To rebuild [`src/raw_data/CpiDataset.xlsx`](file:///src/raw_data/CpiDataset.xlsx) from all frontend datasets (`src/assets/data/`) and sync it to [`public/data/CpiDataset.xlsx`](file:///public/data/CpiDataset.xlsx), run:
```powershell
python scripts/generate_cpi_workbook.py
```

To run data processing tasks against `src/raw_data/`:
- Always use relative paths from project root or `os.path.join(os.path.dirname(__file__), 'raw_data')`.
- Maintain UTF-8 encoding across all CSV and JSON read/write operations.
- Back up any modified master workbook before executing destructive scripts.

### 6.3 Ingesting Future DOSM Releases (e.g., November 2026 onwards)
When DOSM publishes a new CPI release:
1. Save `cpi_YYYY-MM_main.xlsx`, `cpi_YYYY-MM_state.xlsx`, `cpi_YYYY-MM_core.xlsx`, and `cpi_YYYY-MM.pdf` under `src/raw_data/YYYY/`.
2. Refresh OpenDOSM CSVs in `src/raw_data/` (`cpi_2d.csv`, `cpi_2d_state.csv`, `cpi_2d_annual.csv`, `cpi_3d.csv`, `cpi_4d.csv`, `cpi_5d.csv`, `mcoicop.csv`).
3. Extract national headline index and 13 COICOP categories from sheet `J5` and regional indices from sheet `IN_J3` (check row offsets for Sabah/Sarawak).
4. Append the new monthly row to `src/raw_data/cpi_dataset_monthly.csv` and `cpi_dataset_monthly_wide.csv`, and update `CPI_Dataset_Complete.xlsx` and `CPI Raw.xlsx`.
5. Compute $MoM\%$ ($t$ vs $t-1$) and $YoY\%$ ($t$ vs $t-12$).
6. Run `python scripts/generate_detailed_cpi.py` to regenerate [`src/assets/data/detailed/`](file:///src/assets/data/detailed) (`mcoicopTree.json`, `cpiDetailedAnnual.json`, `cpiDetailedMonthly.json`); YTD metadata (`ytdYear`, `ytdMonths`, `latestMonth`) updates automatically in the Detailed UI.
7. Update Simple datasets (`src/assets/data/cpiMalaysia.ts`, `cpiStates.ts`, `cpi*.ts`, and `inflation.ts` when annual figures are finalized).
8. Run `python scripts/generate_cpi_workbook.py` to rebuild [`src/raw_data/CpiDataset.xlsx`](file:///src/raw_data/CpiDataset.xlsx) and sync [`public/data/CpiDataset.xlsx`](file:///public/data/CpiDataset.xlsx).
9. Run `cmd /c "npm run build"` to verify TypeScript types, Vite code-splitting, PWA precache generation, and build integrity.

---

## 7. AI Agent Guidelines & Rules of Engagement

- **Preserve Documentation Integrity:** Do not delete or overwrite historical data files without making explicit backups.
- **Precision First:** When working with CPI data, preserve the exact decimal points published by DOSM (typically 1 to 4 decimal places). Do not prematurely round values.
- **Link Files Correctly:** Always reference local workspace files using standard `file:///` markdown syntax.
- **Test Before Completing:** Before declaring tasks done, verify that the frontend builds without TypeScript errors (`vue-tsc --noEmit`).
