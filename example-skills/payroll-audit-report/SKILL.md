---
name: payroll-audit-report
model: claude-opus-4-6
description: >
  Generate a comprehensive audit report for a company's payrolls over a date range.
  Summarizes totals by pay period, breaks down earnings/taxes/deductions, and flags
  anomalies like large swings between periods or missing workers. Use this skill when
  someone asks for a payroll summary, payroll audit, period-over-period comparison,
  or wants to review payroll data across multiple pay periods.
---

# Payroll Audit Report

This skill generates a structured audit report for a company's payrolls over a
specified date range. It pulls payroll data, aggregates totals per pay period, and
flags anomalies that may warrant investigation.

## Prerequisites

Collect two things from the user:

1. **A Check company ID** (looks like `com_XXXXXXXXXXXXXXXXXX`). Ask for it if not provided.
2. **A date range** — start and end dates for the audit window (e.g., "Q1 2025" or
   "2025-01-01 to 2025-03-31"). If no range is given, default to the last 3 months and
   confirm with the user.

## Step 1: Gather Company Context

Pull the company details for context:

```
run_tool: get_company { "company_id": "<company_id>" }
```

Note the company name for the report header.

## Step 2: Pull Payrolls in the Date Range

Fetch all payrolls whose payday falls within the audit window:

```
run_tool: list_payrolls {
  "company": "<company_id>",
  "payday_after": "YYYY-MM-DD",
  "payday_before": "YYYY-MM-DD",
  "limit": 100
}
```

Convert the user's date range to `YYYY-MM-DD` format:
- `payday_after` — the start of the range (inclusive)
- `payday_before` — the end of the range (inclusive)

If there are more results than the limit, paginate using the `cursor` parameter until
all payrolls are fetched.

Tell the user how many payrolls were found before proceeding:

```
Found 6 payrolls for Acme Corp between 2025-01-01 and 2025-03-31.
Fetching details for each payroll...
```

If no payrolls are found, inform the user and stop.

## Step 3: Fetch Payroll Details

For each payroll, use the composite tool to get items and contractor payments in one call:

```
run_tool: get_payroll_details {
  "payroll_id": "<payroll_id>",
  "include_items": true,
  "include_contractor_payments": true,
  "item_limit": 50
}
```

For payrolls with more than 50 items, note this limitation to the user. Most payrolls
will be well under this limit.

Give progress updates for large sets (e.g., "Fetched 3/6 payrolls...").

## Step 4: Pull Worker Headcounts for Cross-Reference

Fetch current employee and contractor lists to cross-reference against payroll items:

```
run_tool: list_employees { "company": "<company_id>", "limit": 100 }
run_tool: list_contractors { "company": "<company_id>" }
```

These provide the expected headcount to compare against workers appearing in payroll.

## Step 5: Aggregate Totals by Pay Period

For each payroll, compute:

### Employee Payroll Items
From the `payroll_items` in each payroll's details, aggregate:
- **Gross pay**: sum of `gross_pay` across all items
- **Net pay**: sum of `net_pay` across all items
- **Employee taxes**: sum of `employee_taxes` across all items
- **Employer taxes**: sum of `employer_taxes` across all items
- **Employee deductions**: sum of `employee_deductions` (benefits, retirement, etc.)
- **Headcount**: count of unique employee IDs in the payroll items

### Contractor Payments
From the `contractor_payments` in each payroll's details, aggregate:
- **Total contractor pay**: sum of `amount` across all contractor payments
- **Contractor count**: count of unique contractor IDs

### Period Totals
- **Total labor cost** = gross pay + employer taxes + total contractor pay
- **Total disbursements** = net pay + total contractor pay

Build a table with one row per payroll period.

## Step 6: Flag Anomalies

Compare each period against the prior period and against the overall average. Flag:

1. **Large swings** — gross pay or net pay changed by more than 20% period-over-period
   (adjust threshold if the user specifies one)
2. **Headcount changes** — employees appearing in one period but not an adjacent one
   (may indicate missed workers or new hires)
3. **Missing workers** — employees or contractors on the company roster who don't appear
   in any payroll during the audit window
4. **Unusually high/low amounts** — any individual payroll item where gross pay is more
   than 2x the per-worker average for that period
5. **Status issues** — payrolls in a non-final status (draft, pending) that may indicate
   incomplete processing

For each anomaly, include the payroll ID, worker name/ID, and the specific values.

## Step 7: Present the Report

Format the final report with these sections:

### Report Header
```
Payroll Audit Report
Company: Acme Corp (com_XXXXXXXXXXXXXXXXXX)
Period: 2025-01-01 to 2025-03-31
Generated: YYYY-MM-DD
```

### Summary
```
Total payrolls:        6
Total gross pay:       $XXX,XXX.XX
Total net pay:         $XXX,XXX.XX
Total employer taxes:  $XX,XXX.XX
Total contractor pay:  $XX,XXX.XX
Total labor cost:      $XXX,XXX.XX
Avg employees/period:  XX
Avg contractors/period: X
```

### Per-Period Breakdown

Present a table:

```
| Pay Date   | Status | Employees | Gross Pay    | Net Pay      | Emp Taxes  | Emplr Taxes | Deductions | Contractors | Ctr Pay    |
|------------|--------|-----------|--------------|--------------|------------|-------------|------------|-------------|------------|
| 2025-01-15 | paid   | 12        | $45,230.00   | $32,100.00   | $6,780.00  | $3,450.00   | $6,350.00  | 3           | $9,000.00  |
| 2025-01-31 | paid   | 12        | $45,500.00   | $32,300.00   | $6,820.00  | $3,480.00   | $6,380.00  | 3           | $9,000.00  |
| ...        |        |           |              |              |            |             |            |             |            |
```

### Anomalies

If anomalies were found:
```
Anomalies Detected:

1. HEADCOUNT CHANGE — 2025-02-15 payroll has 11 employees (was 12 in prior period).
   Missing: Jane Smith (emp_xxxxx)

2. LARGE SWING — Gross pay increased 35% from $45,500 to $61,425 on 2025-03-15.
   Cause: 3 new employees added.

3. HIGH AMOUNT — John Doe (emp_xxxxx) gross pay of $15,200 on 2025-03-15 is 2.5x
   the per-worker average of $6,100 for that period.
```

If no anomalies: "No anomalies detected."

### Offer Follow-Up

After presenting the report, ask the user if they'd like to:
- Drill into a specific payroll period's details
- See individual worker breakdowns for a period
- Adjust the anomaly thresholds and re-run the analysis
- Export the data in a different format

## Error Handling

- **API errors**: Log the error, continue with remaining payrolls, and note which
  payrolls could not be fetched in the report.
- **Empty payrolls**: Include them in the table with zero values and flag as an anomaly.
- **Large date ranges**: If more than 52 payrolls are found, warn the user and ask if
  they'd like to narrow the range or proceed. Large sets will take longer to process.
- **Pagination**: If any list endpoint returns a cursor indicating more results, follow
  it until all data is fetched.
