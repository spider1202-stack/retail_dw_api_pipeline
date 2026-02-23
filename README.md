# ---------------- CREATE README.md ----------------
$ReadmePath = "$LocalPath\README.md"
if (-not (Test-Path $ReadmePath)) {
    Write-Host "Creating README.md..."
    $ReadmeContent = @"
# $RepoName

This is a full API-based Data Warehouse ETL project.

## Tech Stack
- Python (Pandas, Requests, psycopg2)
- PostgreSQL
- Star Schema Data Warehouse
- Fake Store API (Products)
- Random User API (Customers)
- Fact & Dimension Tables

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run ETL: `python etl_api.py`
3. Connect to PostgreSQL to query data
"@
    # Write content to README.md
    $ReadmeContent | Out-File -Encoding UTF8 -FilePath $ReadmePath
    # Stage and commit README.md immediately
    git add README.md
    git commit -m "Add README.md"
} else {
    Write-Host "README.md already exists."
}
