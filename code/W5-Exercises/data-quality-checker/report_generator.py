import datetime
from typing import Dict, Any, Optional


def _severity_for_check(check: str, issues: int) -> str:
    """
    Determine severity for a check.
    Duplicates are FAIL if any issues.
    Other checks are WARNING when >0 issues, else PASS.
    """
    if issues == 0:
        return "PASS"
    if check == "Duplicates":
        return "FAIL"
    return "WARNING"


def _recommendations_for_check(check: str, details: Dict[str, Any]) -> str:
    """
    Provide one-line recommendation based on check type.
    Details can be used for personalized recommendations.
    """
    if check == "Null Values":
        if details.get("null_count", 0) > 0:
            return "Inspect source and impute or drop nulls in columns with missing data."
        return "No nulls detected."
    if check == "Duplicates":
        if details.get("duplicate_count", 0) > 0:
            return "Remove duplicate rows or collapse them with aggregation."
        return "No duplicates detected."
    if check == "Negative Values":
        if details.get("negative_count", 0) > 0:
            return "Verify negative numbers are allowed; correct or clamp invalid values."
        return "No invalid negative values found."
    if check == "Future Dates":
        if details.get("future_count", 0) > 0:
            return "Check date source and adjust future values where not plausible."
        return "No future dates found."
    if check == "Email Format":
        if details.get("invalid_count", 0) > 0:
            return "Normalize or validate emails; fix malformed entries."
        return "All emails appear valid."
    return "No recommendation available."


def generate_markdown_report(
    checks: Dict[str, Dict[str, Any]],
    file_name: Optional[str] = None,
    total_rows: Optional[int] = None,
) -> str:
    """
    Generate a Markdown report from quality-check results.
    checks keys: 'Null Values', 'Duplicates', 'Negative Values', 'Future Dates', 'Email Format'
    """
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    total_issues = 0
    for check_name, detail in checks.items():
        if check_name == "Null Values":
            issues = sum(c.get("null_count", 0) for c in detail.values()) if isinstance(detail, dict) else 0
        elif check_name == "Negative Values":
            issues = sum(c.get("negative_count", 0) for c in detail.values()) if isinstance(detail, dict) else 0
        else:
            issues = detail.get(
                "duplicate_count",
                detail.get("future_count", detail.get("invalid_count", 0)),
            )
        total_issues += int(issues)

    # build summary table
    summary_rows = []
    for check_name, detail in checks.items():
        if check_name == "Null Values":
            check_issues = sum(c.get("null_count", 0) for c in detail.values() if isinstance(detail, dict))
        elif check_name == "Negative Values":
            check_issues = sum(
                c.get("negative_count", 0) for c in detail.values() if isinstance(detail, dict)
            )
        elif check_name == "Duplicates":
            check_issues = int(detail.get("duplicate_count", 0))
        elif check_name == "Future Dates":
            check_issues = int(detail.get("future_count", 0))
        elif check_name == "Email Format":
            check_issues = int(detail.get("invalid_count", 0))
        else:
            check_issues = 0
        sev = _severity_for_check(check_name, check_issues)
        summary_rows.append((check_name, sev, check_issues))

    # markdown text
    md_lines = []
    md_lines.append("# Data Quality Report")
    md_lines.append("")
    md_lines.append(f"**Generated**: {timestamp}")
    if file_name:
        md_lines.append(f"**File**: {file_name}")
    if total_rows is not None:
        md_lines.append(f"**Total Rows**: {total_rows}")
    md_lines.append("")
    md_lines.append("## Summary")
    md_lines.append("")
    md_lines.append("| Check | Status | Issues Found |")
    md_lines.append("| ----- | ------ | ------------ |")
    for row in summary_rows:
        md_lines.append(f"| {row[0]} | {row[1]} | {row[2]} |")
    md_lines.append("")
    md_lines.append(f"**Total Issues**: {total_issues}")
    md_lines.append("")

    # detailed sections
    md_lines.append("## Detailed Results")
    md_lines.append("")
    for check_name, detail in checks.items():
        if check_name == "Null Values":
            total = sum(c.get("null_count", 0) for c in detail.values() if isinstance(detail, dict))
        elif check_name == "Negative Values":
            total = sum(c.get("negative_count", 0) for c in detail.values() if isinstance(detail, dict))
        else:
            total = int(
                detail.get("duplicate_count", detail.get("future_count", detail.get("invalid_count", 0)))
            )
        severity = _severity_for_check(check_name, total)
        recommendation = _recommendations_for_check(check_name, detail)

        md_lines.append(f"### {check_name}")
        md_lines.append(f"- Status: **{severity}**")
        md_lines.append(f"- Issues Found: **{total}**")
        md_lines.append(f"- Recommendation: {recommendation}")

        if check_name == "Null Values" and isinstance(detail, dict):
            md_lines.append("- Null details by column:")
            for col, col_info in detail.items():
                md_lines.append(
                    f"  - {col}: {col_info.get('null_count', 0)} nulls ({col_info.get('null_percent', 0)}%)"
                )
        if check_name == "Duplicates":
            md_lines.append(f"- Duplicate indices: {detail.get('duplicate_indices', [])}")
            md_lines.append(f"- Duplicate values: {detail.get('duplicate_values', [])}")
        if check_name == "Negative Values" and isinstance(detail, dict):
            for col, col_info in detail.items():
                if isinstance(col_info, dict):
                    md_lines.append(
                        f"  - {col}: {col_info.get('negative_count', 0)} negative ({col_info.get('negative_percent', 0)}%), indices {col_info.get('negative_indices', [])}"
                    )
        if check_name == "Future Dates":
            md_lines.append(f"- Future indices: {detail.get('future_indices', [])}")
            md_lines.append(f"- Future values: {detail.get('future_values', [])}")
        if check_name == "Email Format":
            md_lines.append(f"- Invalid indices: {detail.get('invalid_indices', [])}")
            md_lines.append(f"- Invalid values: {detail.get('invalid_values', [])}")
        md_lines.append("")

    return "\n".join(md_lines)
