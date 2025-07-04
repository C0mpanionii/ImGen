#!/usr/bin/env python3
"""
Release automation script for Image Generation Workspace.

This script automates the process of creating versioned releases with proper
tagging, changelog generation, and GitHub release creation.
"""

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional


class ReleaseManager:
    """Manages the release process for the Image Generation Workspace."""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.changelog_path = repo_root / "CHANGELOG.md"
        
    def get_current_version(self) -> Optional[str]:
        """Get the current version from pyproject.toml."""
        pyproject_path = self.repo_root / "pyproject.toml"
        if not pyproject_path.exists():
            return None
            
        content = pyproject_path.read_text()
        match = re.search(r'version = "([^"]+)"', content)
        return match.group(1) if match else None
    
    def update_version(self, new_version: str) -> None:
        """Update version in pyproject.toml."""
        pyproject_path = self.repo_root / "pyproject.toml"
        content = pyproject_path.read_text()
        updated_content = re.sub(
            r'version = "[^"]+"',
            f'version = "{new_version}"',
            content
        )
        pyproject_path.write_text(updated_content)
        print(f"✅ Updated version to {new_version} in pyproject.toml")
    
    def bump_version(self, current_version: str, bump_type: str) -> str:
        """Bump version according to semantic versioning."""
        parts = current_version.split(".")
        if len(parts) != 3:
            raise ValueError(f"Invalid version format: {current_version}")
        
        major, minor, patch = map(int, parts)
        
        if bump_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif bump_type == "minor":
            minor += 1
            patch = 0
        elif bump_type == "patch":
            patch += 1
        else:
            raise ValueError(f"Invalid bump type: {bump_type}")
        
        return f"{major}.{minor}.{patch}"
    
    def get_latest_tag(self) -> Optional[str]:
        """Get the latest git tag."""
        try:
            result = subprocess.run(
                ["git", "describe", "--tags", "--abbrev=0"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None
    
    def get_commits_since_tag(self, tag: Optional[str]) -> List[str]:
        """Get commit messages since the last tag."""
        if tag:
            cmd = ["git", "log", f"{tag}..HEAD", "--oneline"]
        else:
            cmd = ["git", "log", "--oneline"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
        except subprocess.CalledProcessError:
            return []
    
    def generate_changelog_entry(self, version: str, commits: List[str]) -> str:
        """Generate changelog entry for the new version."""
        date = datetime.now().strftime("%Y-%m-%d")
        entry = f"\n## [{version}] - {date}\n\n"
        
        if not commits:
            entry += "- Initial release\n"
            return entry
        
        # Categorize commits
        features = []
        fixes = []
        docs = []
        other = []
        
        for commit in commits:
            commit_lower = commit.lower()
            if any(keyword in commit_lower for keyword in ["feat:", "feature:", "add:", "new:"]):
                features.append(commit)
            elif any(keyword in commit_lower for keyword in ["fix:", "bug:", "patch:"]):
                fixes.append(commit)
            elif any(keyword in commit_lower for keyword in ["doc:", "docs:", "readme:"]):
                docs.append(commit)
            else:
                other.append(commit)
        
        if features:
            entry += "### ✨ Features\n"
            for commit in features:
                entry += f"- {commit}\n"
            entry += "\n"
        
        if fixes:
            entry += "### 🐛 Bug Fixes\n"
            for commit in fixes:
                entry += f"- {commit}\n"
            entry += "\n"
        
        if docs:
            entry += "### 📚 Documentation\n"
            for commit in docs:
                entry += f"- {commit}\n"
            entry += "\n"
        
        if other:
            entry += "### 🔧 Other Changes\n"
            for commit in other:
                entry += f"- {commit}\n"
            entry += "\n"
        
        return entry
    
    def update_changelog(self, version: str, commits: List[str]) -> None:
        """Update the changelog with the new version."""
        entry = self.generate_changelog_entry(version, commits)
        
        if self.changelog_path.exists():
            content = self.changelog_path.read_text(encoding='utf-8')
            # Insert after the header
            lines = content.split("\n")
            header_end = 0
            for i, line in enumerate(lines):
                if line.startswith("## "):
                    header_end = i
                    break
            
            lines.insert(header_end, entry.strip())
            new_content = "\n".join(lines)
        else:
            # Create new changelog
            new_content = f"""# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
{entry}"""
        
        self.changelog_path.write_text(new_content, encoding='utf-8')
        print(f"✅ Updated changelog with version {version}")
    
    def create_git_tag(self, version: str) -> None:
        """Create and push a git tag."""
        tag_name = f"v{version}"
        
        # Add and commit changes
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(
            ["git", "commit", "-m", f"Release {version}"],
            check=True
        )
        
        # Create annotated tag
        subprocess.run(
            ["git", "tag", "-a", tag_name, "-m", f"Release {version}"],
            check=True
        )
        
        print(f"✅ Created git tag {tag_name}")
        
        # Push changes and tag
        subprocess.run(["git", "push", "origin", "main"], check=True)
        subprocess.run(["git", "push", "origin", tag_name], check=True)
        
        print(f"✅ Pushed tag {tag_name} to origin")
    
    def create_release(self, version: str, auto_bump: Optional[str] = None) -> None:
        """Create a new release."""
        current_version = self.get_current_version()
        if not current_version:
            print("❌ Could not determine current version")
            sys.exit(1)
        
        if auto_bump:
            new_version = self.bump_version(current_version, auto_bump)
        else:
            new_version = version
        
        print(f"🚀 Creating release {new_version} (from {current_version})")
        
        # Get commits since last tag
        latest_tag = self.get_latest_tag()
        commits = self.get_commits_since_tag(latest_tag)
        
        print(f"📝 Found {len(commits)} commits since last tag")
        
        # Update version and changelog
        self.update_version(new_version)
        self.update_changelog(new_version, commits)
        
        # Create git tag
        self.create_git_tag(new_version)
        
        print(f"🎉 Release {new_version} created successfully!")
        print(f"   Tag: v{new_version}")
        print(f"   GitHub Actions will now build and publish the release")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Create a new release")
    parser.add_argument(
        "version",
        nargs="?",
        help="Version number (e.g., 1.2.3) or bump type (major, minor, patch)"
    )
    parser.add_argument(
        "--bump",
        choices=["major", "minor", "patch"],
        help="Automatically bump version"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    
    args = parser.parse_args()
    
    if not args.version and not args.bump:
        parser.error("Must specify either version or --bump")
    
    repo_root = Path(__file__).parent.parent
    manager = ReleaseManager(repo_root)
    
    if args.dry_run:
        current_version = manager.get_current_version()
        if args.bump:
            new_version = manager.bump_version(current_version, args.bump)
        else:
            new_version = args.version
        
        print(f"🔍 Dry run mode:")
        print(f"   Current version: {current_version}")
        print(f"   New version: {new_version}")
        print(f"   Would create tag: v{new_version}")
        return
    
    # Determine version
    if args.bump:
        manager.create_release(None, args.bump)
    elif args.version in ["major", "minor", "patch"]:
        manager.create_release(None, args.version)
    else:
        manager.create_release(args.version)


if __name__ == "__main__":
    main()
