# AI Agent Guide: Malaysian CPI Raw Data Repository (`src/raw_data`)
<!-- Antigravity -->
> **Last Updated:** November 2026  
> **Repository Scope:** Raw CPI data archive under `src/raw_data`.  
> **Primary Authority:** Department of Statistics Malaysia (DOSM / *Jabatan Perangkaan Malaysia*)

---

## 1. Overview & Official Data Sources

This repository houses the historical and present archive of the **Consumer Price Index (CPI / Indeks Harga Pengguna - IHP)** for **Malaysia**, published by DOSM.

### 1.1 Direct OpenDOSM Storage Feeds (Authoritative Machine-Readable Data)
The primary and most up-to-date machine-readable datasets are available directly from DOSM's cloud storage:

| Dataset | URL | Description & Granularity | Date Format |
| :--- | :--- | :--- | :--- |
| **National Annual CPI (2D)** | [`https://storage.dosm.gov.my/cpi/cpi_2d_annual.csv`](https://storage.dosm.gov.my/cpi/cpi_2d_annual.csv) | National headline & 13 COICOP categories (1960–2025) | `YYYY-01-01` |
| **State Monthly CPI (2D)** | [`https://storage.dosm.gov.my/cpi/cpi_2d_state.csv`](https://storage.dosm.gov.my/cpi/cpi_2d_state.csv) | 16 Malaysian States & Federal Territories by division (2010–present) | `YYYY-MM-01` |
| **National Monthly CPI (2D)** | [`https://storage.dosm.gov.my/cpi/cpi_2d.csv`](https://storage.dosm.gov.my/cpi/cpi_2d.csv) | National headline & 13 COICOP divisions (1980–present) | `YYYY-MM-01` |
| **CPI by 3-Digit Group (3D)** | [`https://storage.dosm.gov.my/cpi/cpi_3d.csv`](https://storage.dosm.gov.my/cpi/cpi_3d.csv) | 47 COICOP 2018 3-digit groups (2010–present) | `YYYY-MM-01` |
| **CPI by 4-Digit Class (4D)** | [`https://storage.dosm.gov.my/cpi/cpi_4d.csv`](https://storage.dosm.gov.my/cpi/cpi_4d.csv) | 101 COICOP 2018 4-digit classes (2010–present) | `YYYY-MM-01` |
| **CPI by 5-Digit Subclass (5D)** | [`https://storage.dosm.gov.my/cpi/cpi_5d.csv`](https://storage.dosm.gov.my/cpi/cpi_5d.csv) | 181 COICOP 2018 5-digit subclasses (2010–present) | `YYYY-MM-01` |
| **MCOICOP Dictionary** | [`https://storage.dosm.gov.my/dictionaries/mcoicop.csv`](https://storage.dosm.gov.my/dictionaries/mcoicop.csv) | Official 343-row classification hierarchy & EN/BM descriptions | N/A (Lookup) |

### 1.2 OpenDOSM & `data.gov.my` Data Catalogue Portals
Interactive catalogues with data dictionaries, visual charts, and metadata:
- **Annual National Series (2-digit):** [Annual CPI by Division (2-digit) | OpenDOSM](https://open.dosm.gov.my/data-catalogue/cpi_annual)
- **Monthly State Series (2-digit):** [Monthly CPI by State & Division (2-digit) | OpenDOSM](https://open.dosm.gov.my/data-catalogue/cpi_state)
- **Monthly 3-Digit Group Series:** [CPI by Group (3-digit) | data.gov.my](https://data.gov.my/data-catalogue/cpi_3d) — CSV: [`cpi_3d.csv`](https://storage.dosm.gov.my/cpi/cpi_3d.csv)
- **Monthly 4-Digit Class Series:** [CPI by Class (4-digit) | data.gov.my](https://data.gov.my/data-catalogue/cpi_4d) — CSV: [`cpi_4d.csv`](https://storage.dosm.gov.my/cpi/cpi_4d.csv)
- **Monthly 5-Digit Subclass Series:** [CPI by Subclass (5-digit) | data.gov.my](https://data.gov.my/data-catalogue/cpi_5d) — CSV: [`cpi_5d.csv`](https://storage.dosm.gov.my/cpi/cpi_5d.csv)

### 1.3 Official DOSM Publication URLs & Standard Naming Conventions

#### A. Monthly Publications (Press Releases & Detailed Spreadsheets)
For every release month `YYYY-MM` (e.g. `2026-10`), DOSM publishes four files in storage and an online release page:

- **PDF Bulletin:** `https://storage.dosm.gov.my/cpi/cpi_YYYY-MM.pdf`  
  *Example:* [`https://storage.dosm.gov.my/cpi/cpi_2026-10.pdf`](https://storage.dosm.gov.my/cpi/cpi_2026-10.pdf)
- **Headline Main CPI Excel:** `https://storage.dosm.gov.my/cpi/cpi_YYYY-MM_main.xlsx`  
  *Example:* [`https://storage.dosm.gov.my/cpi/cpi_2026-10_main.xlsx`](https://storage.dosm.gov.my/cpi/cpi_2026-10_main.xlsx)  
  *(Contains Table J1–J5 national totals, Table 25 detailed 5-digit expenditure classes)*
- **State & Regional CPI Excel:** `https://storage.dosm.gov.my/cpi/cpi_YYYY-MM_state.xlsx`  
  *Example:* [`https://storage.dosm.gov.my/cpi/cpi_2026-10_state.xlsx`](https://storage.dosm.gov.my/cpi/cpi_2026-10_state.xlsx)  
  *(Contains Table IN_J3 for Semenanjung, Sabah, Sarawak, and individual states)*
- **Core CPI (*Indeks Teras*) Excel:** `https://storage.dosm.gov.my/cpi/cpi_YYYY-MM_core.xlsx`  
  *Example:* [`https://storage.dosm.gov.my/cpi/cpi_2026-10_core.xlsx`](https://storage.dosm.gov.my/cpi/cpi_2026-10_core.xlsx)  
  *(Excludes volatile food & administered prices; do not use for Headline CPI)*
- **Web Portal Release Page:** `https://open.dosm.gov.my/publications/cpi_YYYY-MM`  
  *Example:* [[Oct 2026] Consumer Price Index | OpenDOSM](https://open.dosm.gov.my/publications/cpi_2026-10)

#### B. Yearly / Annual Summary Publications
For each completed calendar year `YYYY` (e.g. `2025`), DOSM compiles annual reports:

- **Annual Excel Workbook:** `https://storage.dosm.gov.my/cpi/cpi_annual_YYYY.xlsx`  
  *Example:* [`https://storage.dosm.gov.my/cpi/cpi_annual_2025.xlsx`](https://storage.dosm.gov.my/cpi/cpi_annual_2025.xlsx)
- **Annual PDF Analysis:** `https://storage.dosm.gov.my/cpi/cpi_annual_YYYY.pdf`  
  *Example:* [`https://storage.dosm.gov.my/cpi/cpi_annual_2025.pdf`](https://storage.dosm.gov.my/cpi/cpi_annual_2025.pdf)
- **Web Portal Annual Summary Page:** `https://open.dosm.gov.my/publications/cpi_annual_YYYY`  
  *Example:* [[2025] Consumer Price Index | OpenDOSM](https://open.dosm.gov.my/publications/cpi_annual_2025)

---

## 2. Date Formats & Data Schemas

### 2.1 `cpi_2d_annual.csv` (National Annual Time Series)
- **Date Format:** `YYYY-01-01` (ISO 8601 string, fixed to January 1st for annual aggregate, e.g. `1960-01-01`, `2025-01-01`).
- **Columns:**
  1. `date`: `YYYY-01-01`
  2. `division`: COICOP division code (`overall`, `01`, `02`, `03`, `04`, `05`, `06`, `07`, `08`, `09`, `10`, `11`, `12`, `13`)
  3. `index`: Numerical index level (base $2010 = 100$)
- **Division Horizons:**
  - `overall`: 1960 to 2025 (66 consecutive years)
  - `01` to `07`, `09`: 1980 to 2025 (46 consecutive years)
  - `08`, `10`, `11`, `13`: 2003 to 2025 (23 consecutive years)
  - `12` (*Insurance & Financial Services*): 2010 to 2025 (16 consecutive years)

### 2.2 `cpi_2d_state.csv` (State & Federal Territory Monthly Series)
- **Date Format:** `YYYY-MM-01` (ISO 8601 string representing the 1st of each month, e.g. `2010-01-01` to `2026-10-01`).
- **Columns:**
  1. `state`: State / Federal Territory name
  2. `date`: `YYYY-MM-01`
  3. `division`: COICOP division code (`overall`, `01`–`13`)
  4. `index`: Numerical index level (base $2010 = 100$)
- **Geographic Coverage (16 Entities):**
  - *Johor, Kedah, Kelantan, Melaka, Negeri Sembilan, Pahang, Perak, Perlis, Pulau Pinang, Sabah, Sarawak, Selangor, Terengganu, W.P. Kuala Lumpur, W.P. Labuan, W.P. Putrajaya*.

### 2.3 `cpi_2d.csv`, `cpi_3d.csv`, `cpi_4d.csv`, and `cpi_5d.csv` (Granular National Monthly Series)
- **Date Format:** `YYYY-MM-01` (read code columns as strings to preserve leading zeros such as `'001'`, `'0111'`, `'00111'`).
- **`cpi_2d.csv` (2-Digit Divisions):** `date`, `division` (14 codes: `overall`, `01`–`13`), `index` (`1980-01-01` to `2026-10-01`).
- **`cpi_3d.csv` (3-Digit Groups):** `date`, `group` (47 codes: `'001'`–`'139'`), `index` (`2010-01-01` to `2026-10-01`).
- **`cpi_4d.csv` (4-Digit Classes):** `date`, `class` (101 codes: `'0011'`–`'1390'`), `index` (`2010-01-01` to `2026-10-01`).
- **`cpi_5d.csv` (5-Digit Subclasses):** `date`, `subclass` (181 codes: `'00111'`–`'13909'`), `index` (`2010-01-01` to `2026-10-01`).

### 2.4 `mcoicop.csv` (Official MCOICOP 2018 Classification Dictionary)
- **Columns:** `digits` (`1`–`5`), `division`, `group`, `class`, `subclass`, `desc_en`, `desc_bm` (343 rows covering all `overall`, 2-digit, 3-digit, 4-digit, and 5-digit codes).

---

## 3. Master Generated Datasets (Ground Truth in `src/raw_data/`)

Any agent querying or analyzing Malaysian CPI data should use the clean, consolidated datasets located directly in `src/raw_data`:

| File Name | Format | Description & Usage |
| :--- | :--- | :--- |
| **`cpi_2d_annual.csv`** | CSV | Official DOSM Open Data annual series (1960–2025) for national total and 13 COICOP categories. |
| **`cpi_2d_state.csv`** | CSV | Official DOSM Open Data 16-state monthly series (2010–present) across all 14 divisions. |
| **`cpi_2d.csv`** | CSV | Official DOSM Open Data national 2-digit division monthly series (1980–present). |
| **`cpi_3d.csv`** | CSV | Official DOSM Open Data national 3-digit group monthly series (47 groups, 2010–present). |
| **`cpi_4d.csv`** | CSV | Official DOSM Open Data national 4-digit class monthly series (101 classes, 2010–present). |
| **`cpi_5d.csv`** | CSV | Official DOSM Open Data national 5-digit subclass monthly series (181 subclasses, 2010–present). |
| **`mcoicop.csv`** | CSV | Official DOSM MCOICOP 2018 lookup dictionary (343 codes with English and Malay descriptions). |
| **`CPI_Dataset_Complete.xlsx`** | Excel (.xlsx) | Master multi-tab workbook with metadata, national monthly (2010–Oct 2026), national annual (2000–2025), strata, and regional breakdowns. |
| **`cpi_dataset_monthly.csv`** | CSV (Tidy/Long) | 2,660 records (202 months). Schema: `date`, `year`, `month`, `month_name`, `series_type`, `segment`, `group_code`, `group_name`, `index_2010_100`, `mom_pct`, `yoy_pct`. |
| **`cpi_dataset_monthly_wide.csv`** | CSV (Wide) | 202 monthly rows with headline index, all 13 groups, MoM%, and YoY%. Ideal for modeling and plotting. |
| **`cpi_dataset_annual.csv`** | CSV (Long) | 1,105 records (2000 to 2025) covering national and regional annual indices and annual inflation rates. |
| **`cpi_dataset.json`** | JSON | Structured JSON format with metadata, data source links, annual summary, and full nested monthly records. |
| **`CPI Raw.xlsx`** | Excel (.xlsx) | Working master workbook with `Malaysia` (through Oct 2026), `Detailed` (COICOP 2018 block backfilled 2016–2026), `Detailed (COICOP 2018)`, `MCOICOP Dictionary`, `Detailed 3D (Groups)`, `Detailed 4D (Classes)`, and `Detailed 5D (Subclasses)`. |
| **`CpiDataset.xlsx`** | Excel (.xlsx) | Working regional workbook with verified headline numbers for Malaysia, Semenanjung, Sabah, and Sarawak. |

---

## 4. Critical Rules & Domain Gotchas for Agents

### Rule 1: Distinguish Headline CPI vs. Core CPI
DOSM publishes multiple indices in separate files each period:
- **`main.xlsx` (or PDF Jadual 1 / Jadual 5):** **Headline CPI (*IHP Keseluruhan*)**. This includes all goods and services.
- **`core.xlsx` (*Indeks Teras*):** **Core CPI**. Excludes volatile fresh food prices and administered goods (Alcohol & Tobacco shows as `'-'`).
- **Never mix Core CPI values into Headline series.**

### Rule 2: The 2024 COICOP 2018 Classification Shift
In early 2024, DOSM upgraded to the COICOP 2018 standard:
- **2010 – 2023 (12 Groups):** Group 12 was *Miscellaneous Goods & Services* (*Pelbagai Barangan & Perkhidmatan*), which included personal care, insurance, and financial services.
- **2024 – Present (13 Groups):**
  - **Group 12:** *Insurance & Financial Services* (*Insurans & Perkhidmatan Kewangan*).
  - **Group 13:** *Personal Care, Social Protection & Miscellaneous Goods & Services* (*Penjagaan Diri, Perlindungan Sosial & Pelbagai Barangan & Perkhidmatan*).

### Rule 3: Decrypting 2017–2018 Excel Files
The `.xlsx` files in `2017/` and `2018/` are encrypted with Microsoft Office's default read-only password (`VelvetSweatshop`). To open them in Python:
```python
import io, msoffcrypto, openpyxl

with open(file_path, "rb") as f:
  office_file = msoffcrypto.OfficeFile(f)
  office_file.load_key(password="VelvetSweatshop")
  decrypted = io.BytesIO()
  office_file.decrypt(decrypted)
  wb = openpyxl.load_workbook(decrypted, data_only=True)
```

### Rule 4: Regional Data Row Offsets in State Files (`*_state.xlsx` -> `IN_J3`)
When reading state and regional indices from sheet `IN_J3`:
- **Semenanjung:** Row 11 across all years.
- **Sabah & W.P. Labuan:** Row 407 (up to 2025) $\rightarrow$ shifted to **Row 389** in 2026.
- **Sarawak:** Row 437 (up to 2025) $\rightarrow$ shifted to **Row 417** in 2026.

---

## 5. Step-by-Step Instructions: How to Update Data for New Periods

When a new monthly release (e.g., November 2026 onwards) or annual report is published by DOSM:

### Step 1: Download Fresh OpenDOSM CSV Datasets
Download the latest versions of the open data CSV feeds:
```python
import urllib.request, ssl

ctx = ssl.create_default_context()
for filename, url in [
    ('src/raw_data/cpi_2d_annual.csv', 'https://storage.dosm.gov.my/cpi/cpi_2d_annual.csv'),
    ('src/raw_data/cpi_2d_state.csv', 'https://storage.dosm.gov.my/cpi/cpi_2d_state.csv'),
    ('src/raw_data/cpi_2d.csv', 'https://storage.dosm.gov.my/cpi/cpi_2d.csv'),
    ('src/raw_data/cpi_3d.csv', 'https://storage.dosm.gov.my/cpi/cpi_3d.csv'),
    ('src/raw_data/cpi_4d.csv', 'https://storage.dosm.gov.my/cpi/cpi_4d.csv'),
    ('src/raw_data/cpi_5d.csv', 'https://storage.dosm.gov.my/cpi/cpi_5d.csv'),
    ('src/raw_data/mcoicop.csv', 'https://storage.dosm.gov.my/dictionaries/mcoicop.csv'),
]:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx) as resp, open(filename, 'wb') as f:
        f.write(resp.read())
```

### Step 2: Download New Publication Files into `src/raw_data/YYYY/`
Using the standardized naming convention:
```text
https://storage.dosm.gov.my/cpi/cpi_YYYY-MM.pdf
https://storage.dosm.gov.my/cpi/cpi_YYYY-MM_main.xlsx
https://storage.dosm.gov.my/cpi/cpi_YYYY-MM_state.xlsx
https://storage.dosm.gov.my/cpi/cpi_YYYY-MM_core.xlsx
```
Place them under `src/raw_data/YYYY/`.

### Step 3: Compute Annual / YTD Averages from State Data
For the current year (e.g. 2026), calculate the mean across available months for each state and division:
```python
import pandas as pd

df_st = pd.read_csv('src/raw_data/cpi_2d_state.csv')
df_st['year'] = df_st['date'].str[:4].astype(int)

# Annual average per state, year, and COICOP division
state_annual = df_st.groupby(['state', 'year', 'division'])['index'].mean().round(2).unstack()
```

### Step 4: Synchronize Frontend TypeScript Datasets
1. **`src/assets/data/cpiMalaysia.ts`:**
   - Map `cpi_2d_annual.csv` divisions (`overall` $\rightarrow$ `total`, `01` $\rightarrow$ `food`, etc.).
   - Append YTD average for the ongoing year from `cpi_2d_state.csv` / `cpi_2026-MM_main.xlsx`.
2. **`src/assets/data/cpiStates.ts`:**
   - Update all 16 state objects with the latest annual averages.
3. **`src/assets/data/inflation.ts`:**
   - When a full year is complete (all 12 months), compute $\pi_{annual} = \left(\frac{I_y - I_{y-1}}{I_{y-1}}\right) \times 100$ and append the new year's inflation rate.

### Step 5: Update UI Components & Verify Build
1. In `src/components/Calculator.vue`, update option label year ranges if new years become available.
2. Ensure `src/components/DataSource.vue` retains links to both the Data Catalogue and Publications portals.
3. Run `npm run build` (`vue-tsc --noEmit && vite build`) to verify zero TypeScript errors.

---

## 6. Quick Reference Table: Latest Ground Truth Values

| Metric / Category | Period / Source | Latest Value |
| :--- | :--- | :--- |
| **Headline National CPI** | 2025 Annual Average (`cpi_2d_annual.csv`) | **134.6** |
| **Headline National CPI** | 2024 Annual Average (`cpi_2d_annual.csv`) | **132.8** |
| **Headline National CPI (YTD 2026)** | Jan–Oct 2026 Average (`cpi_2d.csv` / `cpi_2d_state.csv`) | **136.9** |
| **Headline National CPI (Single Month)** | October 2026 (`cpi_2026-10_main.xlsx`, YoY **+1.92%**) | **137.7** |
| **Annual Inflation Rate (2025)** | 2025 vs 2024 ($$134.6 \text{ vs } 132.8$$) | **+1.36%** |
| **Annual Inflation Rate (2024)** | 2024 vs 2023 ($$132.8 \text{ vs } 130.4$$) | **+1.84%** |
| **Food & Non-Alcoholic Beverages** | 2025 Annual Average | **158.2** |
| **Transport** | 2025 Annual Average | **122.2** |
| **Housing, Water, Electricity, Gas** | 2025 Annual Average | **131.1** |
| **Insurance & Financial Services** | 2025 Annual Average | **114.3** |
