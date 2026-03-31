---
name: worker-census-report
model: claude-opus-4-6
description: >
  Export a complete census of all employees and contractors for a company. Includes
  full details such as addresses, SSN (last 4), start dates, workplace assignments,
  and active/terminated status. Useful for benefits enrollment, compliance audits,
  and annual reviews. Use this skill when someone asks for a worker roster, employee
  census, headcount report, workforce export, or needs a full list of workers with
  their details.
---

# Worker Census Report

This skill generates a complete census of all employees and contractors for a company.
It pulls full worker details and presents a structured report suitable for benefits
enrollment, compliance audits, and annual reviews.

## Prerequisites

Collect from the user:

1. **A Check company ID** (looks like `com_XXXXXXXXXXXXXXXXXX`). Ask for it if not provided.
2. **Optional filters** — ask the user:
   - **Worker types**: employees only, contractors only, or both (default: both)
   - **Status filter**: active only, terminated only, or all (default: all)

## Step 1: Gather Company Context

Pull the company details:

```
run_tool: get_company { "company_id": "<company_id>" }
```

Note the company name for the report header.

## Step 2: Build Workplace Lookup

Fetch all workplaces to map workplace IDs to addresses:

```
run_tool: list_workplaces { "company": "<company_id>", "limit": 500 }
```

Build a lookup table: `{ workplace_id: { name, line1, city, state, postal_code } }`.

If any workplace entry lacks address details, fetch it individually:

```
run_tool: get_workplace { "workplace_id": "<workplace_id>" }
```

## Step 3: Fetch Employees

Skip this step if the user requested contractors only.

### 3a. List all employees

```
run_tool: list_employees { "company": "<company_id>", "limit": 100 }
```

If the response includes a `next` cursor, paginate:

```
run_tool: list_employees { "company": "<company_id>", "limit": 100, "cursor": "<cursor>" }
```

Continue until all employees are fetched. Report progress for large companies:
"Fetched 100/247 employees..."

### 3b. Get full details for each employee

The list endpoint returns summary data. For full details (residence, SSN last 4, etc.),
fetch each employee individually:

```
run_tool: get_employee { "employee_id": "<employee_id>" }
```

Process these in batches and give progress updates (e.g., "Fetching employee details:
25/50...").

### 3c. Apply status filter

If the user requested active only, filter out employees with a `termination_date`.
If terminated only, keep only those with a `termination_date`.

## Step 4: Fetch Contractors

Skip this step if the user requested employees only.

### 4a. List all contractors

```
run_tool: list_contractors { "company": "<company_id>" }
```

Paginate if needed using the `cursor` parameter.

### 4b. Get full details for each contractor

```
run_tool: get_contractor { "contractor_id": "<contractor_id>" }
```

Give progress updates for large sets.

### 4c. Apply status filter

Same filtering logic as employees — use `termination_date` to determine active vs
terminated status.

## Step 5: Present the Report

### Report Header

```
Worker Census Report
Company: Acme Corp (com_XXXXXXXXXXXXXXXXXX)
Generated: YYYY-MM-DD
Filter: All workers (active + terminated)
```

### Summary Statistics

```
Total workers:       52
  Employees:         45 (40 active, 5 terminated)
  Contractors:        7 (6 active, 1 terminated)
Workplaces:           3
```

### Employee Table

Present a markdown table with one row per employee:

```
| Name            | ID          | Status     | SSN Last 4 | DOB        | Start Date | Term Date  | Email                  | Residence                          | Workplace              |
|-----------------|-------------|------------|------------|------------|------------|------------|------------------------|------------------------------------|------------------------|
| Smith, Jane     | emp_xxxxx   | Active     | 1234       | 1990-05-15 | 2023-01-10 | —          | jane@example.com       | 123 Main St, SF, CA 94105          | HQ - 456 Market St     |
| Doe, John       | emp_yyyyy   | Terminated | 5678       | 1985-11-22 | 2022-06-01 | 2024-12-15 | john@example.com       | 789 Oak Ave, Oakland, CA 94612     | HQ - 456 Market St     |
| ...             |             |            |            |            |            |            |                        |                                    |                        |
```

Sort by last name, then first name.

For the Residence column, format as: `line1, city, state postal_code`. Include `line2`
if present (e.g., "123 Main St Apt 4, SF, CA 94105").

For the Workplace column, use the workplace address from the lookup table. If an employee
has multiple workplaces, list the primary workplace. If no workplace is assigned, show "—".

### Contractor Table

Same structure, but use the contractor's `address` field instead of `residence`:

```
| Name            | ID          | Status | SSN Last 4 | DOB        | Start Date | Term Date  | Email                  | Address                            |
|-----------------|-------------|--------|------------|------------|------------|------------|------------------------|------------------------------------|
| Freelance, Fred | ctr_xxxxx   | Active | 9012       | 1988-03-10 | 2024-01-15 | —          | fred@freelance.com     | 321 Pine St, LA, CA 90001          |
| ...             |             |        |            |            |            |            |                        |                                    |
```

### Fields with Missing Data

If any worker is missing fields (no SSN, no DOB, no address, etc.), show "—" in that
cell and include a summary at the end:

```
Data Gaps:
- 3 employees missing email addresses
- 1 contractor missing home address
- 2 employees missing SSN
```

## Step 6: Offer Output Format

After presenting the report, ask the user if they'd like:

1. **Markdown table** (already shown above)
2. **CSV-formatted text** — output the same data as comma-separated values that the user
   can copy-paste into a spreadsheet:

```csv
Type,Name,ID,Status,SSN Last 4,DOB,Start Date,Term Date,Email,Address,Workplace
Employee,"Smith, Jane",emp_xxxxx,Active,1234,1990-05-15,2023-01-10,,jane@example.com,"123 Main St, SF, CA 94105","HQ - 456 Market St"
Employee,"Doe, John",emp_yyyyy,Terminated,5678,1985-11-22,2022-06-01,2024-12-15,john@example.com,"789 Oak Ave, Oakland, CA 94612","HQ - 456 Market St"
Contractor,"Freelance, Fred",ctr_xxxxx,Active,9012,1988-03-10,2024-01-15,,fred@freelance.com,"321 Pine St, LA, CA 90001",
```

Quote any fields that contain commas.

## Error Handling

- **API errors on individual workers**: Log the error, continue with remaining workers,
  and include a list of workers that could not be fetched at the end of the report.
- **Large companies (100+ workers)**: Process in batches with progress updates. Warn the
  user before starting that this may take a moment.
- **Pagination**: Always follow cursors until all results are fetched. Never assume a
  single page contains all workers.
- **No workers found**: If the company has no employees or contractors, report that
  clearly rather than showing empty tables.
- **Permission errors**: If a specific worker can't be fetched (403/404), note it and
  continue with the rest.
