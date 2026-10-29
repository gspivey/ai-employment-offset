#!/usr/bin/env python3
"""
Preflight Check: Validates deliverables before claiming "done"

Run this before telling the user a task is complete.
Catches: stale PDFs, unverified claims, missing sources, broken references.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent
PAPER_DIR = WORKSPACE / "paper"
DATA_DIR = WORKSPACE / "data"
STATE_FILE = WORKSPACE / ".kiro" / "build_state.json"


def check_pdf_freshness():
    """Verify PDF exists and is newer than all .tex files."""
    pdf_path = PAPER_DIR / "main.pdf"
    issues = []
    
    if not pdf_path.exists():
        return [("CRITICAL", "main.pdf does not exist - must compile before delivery")]
    
    pdf_mtime = pdf_path.stat().st_mtime
    pdf_time = datetime.fromtimestamp(pdf_mtime)
    
    stale_sources = []
    for tex_file in PAPER_DIR.rglob("*.tex"):
        if tex_file.stat().st_mtime > pdf_mtime:
            stale_sources.append(tex_file.name)
    
    if stale_sources:
        issues.append(("WARNING", f"PDF is stale - these .tex files were modified after compile: {', '.join(stale_sources)}"))
    else:
        print(f"✓ PDF is fresh (compiled {pdf_time.strftime('%Y-%m-%d %H:%M')})")
    
    return issues


def check_unverified_claims():
    """Scan for [claim], [rigor], [placeholder] flags in .tex files."""
    issues = []
    flags_found = {}
    
    patterns = {
        r'\[claim\]': 'CLAIM - needs primary source',
        r'\[rigor\]': 'RIGOR - needs author review',
        r'\\placeholder': 'PLACEHOLDER - missing value',
        r'\[TODO\]': 'TODO - incomplete',
        r'\[CITE\]': 'CITE - missing citation',
    }
    
    for tex_file in PAPER_DIR.rglob("*.tex"):
        content = tex_file.read_text()
        for pattern, description in patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                key = f"{tex_file.name}: {description}"
                flags_found[key] = len(matches)
    
    if flags_found:
        for flag, count in flags_found.items():
            issues.append(("WARNING", f"{flag} ({count}x)"))
    else:
        print("✓ No unverified claim flags found")
    
    return issues


def check_claim_registry():
    """Verify claim registry exists and check for unverified entries."""
    registry_path = DATA_DIR / "claim_registry.md"
    issues = []
    
    if not registry_path.exists():
        issues.append(("INFO", "claim_registry.md not found - consider creating one"))
        return issues
    
    content = registry_path.read_text()
    unverified = content.count("| ✗ |") + content.count("[claim]")
    
    if unverified > 0:
        issues.append(("WARNING", f"Claim registry has {unverified} unverified entries"))
    else:
        print("✓ All claims in registry verified")
    
    return issues


def check_bibliography():
    """Check for common BibTeX issues."""
    bib_path = PAPER_DIR / "references.bib"
    issues = []
    
    if not bib_path.exists():
        issues.append(("WARNING", "references.bib not found"))
        return issues
    
    content = bib_path.read_text()
    
    # Count entries
    entries = len(re.findall(r'@\w+\{', content))
    print(f"✓ Bibliography has {entries} entries")
    
    # Check for empty fields
    empty_fields = re.findall(r'(\w+)\s*=\s*\{\s*\}', content)
    if empty_fields:
        issues.append(("INFO", f"Empty BibTeX fields found: {', '.join(set(empty_fields))}"))
    
    return issues


def update_build_state(issues):
    """Write current state to JSON for tracking."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    state = {
        "last_check": datetime.now().isoformat(),
        "pdf_exists": (PAPER_DIR / "main.pdf").exists(),
        "issue_count": len(issues),
        "critical_issues": len([i for i in issues if i[0] == "CRITICAL"]),
        "warnings": len([i for i in issues if i[0] == "WARNING"]),
    }
    
    STATE_FILE.write_text(json.dumps(state, indent=2))


def main():
    print("=" * 60)
    print("PREFLIGHT CHECK - Validating deliverables")
    print("=" * 60)
    print()
    
    all_issues = []
    
    print("1. Checking PDF freshness...")
    all_issues.extend(check_pdf_freshness())
    print()
    
    print("2. Scanning for unverified claims...")
    all_issues.extend(check_unverified_claims())
    print()
    
    print("3. Checking claim registry...")
    all_issues.extend(check_claim_registry())
    print()
    
    print("4. Checking bibliography...")
    all_issues.extend(check_bibliography())
    print()
    
    update_build_state(all_issues)
    
    # Summary
    print("=" * 60)
    if not all_issues:
        print("✓ ALL CHECKS PASSED - Safe to deliver")
        return 0
    
    critical = [i for i in all_issues if i[0] == "CRITICAL"]
    warnings = [i for i in all_issues if i[0] == "WARNING"]
    info = [i for i in all_issues if i[0] == "INFO"]
    
    if critical:
        print("✗ CRITICAL ISSUES - Cannot deliver:")
        for _, msg in critical:
            print(f"   ✗ {msg}")
    
    if warnings:
        print("\n⚠ WARNINGS - Should address:")
        for _, msg in warnings:
            print(f"   ⚠ {msg}")
    
    if info:
        print("\nℹ INFO:")
        for _, msg in info:
            print(f"   ℹ {msg}")
    
    print("=" * 60)
    return 1 if critical else 0


if __name__ == "__main__":
    exit(main())
