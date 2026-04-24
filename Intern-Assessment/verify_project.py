#!/usr/bin/env python3
"""
RAG APPLICATION - COMPLETION VERIFICATION SCRIPT
This script verifies all project files are in place and ready for deployment.
"""

import os
from pathlib import Path

# Define expected project structure
PROJECT_FILES = {
    "Backend": [
        "backend/main.py",
        "backend/config.py",
        "backend/ingestion.py",
        "backend/retrieval.py",
        "backend/requirements.txt",
    ],
    "Frontend": [
        "frontend/app.py",
        "frontend/Dockerfile",
        "frontend/requirements.txt",
        "frontend/.streamlit/config.toml",
        "frontend/.streamlit/secrets.toml",
    ],
    "Docker & Deployment": [
        "Dockerfile",
        "docker-compose.yml",
        ".env.example",
        ".dockerignore",
        ".gitignore",
    ],
    "CI/CD": [
        ".github/workflows/docker-build.yml",
        ".github/workflows/tests.yml",
    ],
    "Testing": [
        "tests/test_api.py",
    ],
    "Scripts": [
        "start.sh",
        "start.bat",
    ],
    "Documentation": [
        "README.md",
        "QUICK_REFERENCE.md",
        "API.md",
        "ARCHITECTURE.md",
        "DEVELOPMENT.md",
        "DEPLOYMENT.md",
        "REQUIREMENTS.md",
        "CHECKLIST.md",
        "PROJECT_SUMMARY.md",
        "PROJECT_STRUCTURE.txt",
        "INDEX.md",
    ],
}


def verify_project():
    """Verify all project files are present."""
    print("=" * 80)
    print("RAG APPLICATION - PROJECT COMPLETION VERIFICATION")
    print("=" * 80)
    print()

    base_path = Path(".")
    all_present = True
    total_files = 0
    found_files = 0

    for category, files in PROJECT_FILES.items():
        print(f"📁 {category}")
        print("-" * 40)

        for file in files:
            file_path = base_path / file
            total_files += 1

            if file_path.exists():
                size = file_path.stat().st_size
                if size > 1024:
                    size_str = f"{size / 1024:.1f}KB"
                else:
                    size_str = f"{size}B"

                print(f"  ✅ {file:<35} ({size_str})")
                found_files += 1
            else:
                print(f"  ❌ {file:<35} (MISSING)")
                all_present = False

        print()

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total Files Expected: {total_files}")
    print(f"Files Found:         {found_files}")
    print(f"Files Missing:       {total_files - found_files}")
    print()

    if all_present:
        print("✅ ALL FILES PRESENT - PROJECT IS COMPLETE")
        print()
        print("🚀 NEXT STEPS:")
        print("-" * 40)
        print("1. Set up environment:")
        print("   cp .env.example .env")
        print("   # Edit .env with your Groq API key")
        print()
        print("2. Run the application:")
        print("   docker-compose up --build")
        print()
        print("3. Access services:")
        print("   - Frontend: http://localhost:8501")
        print("   - API: http://localhost:8000")
        print("   - API Docs: http://localhost:8000/docs")
        print()
        print("📚 DOCUMENTATION:")
        print("-" * 40)
        print("- README.md           - Start here")
        print("- QUICK_REFERENCE.md  - Common commands")
        print("- API.md              - API details")
        print("- DEPLOYMENT.md       - Cloud deployment")
        print()
        return True
    else:
        print("❌ SOME FILES ARE MISSING")
        print()
        print("Please verify the project structure and try again.")
        return False


def check_requirements():
    """Check if Python requirements can be read."""
    print("=" * 80)
    print("CHECKING REQUIREMENTS")
    print("=" * 80)
    print()

    for req_file in ["backend/requirements.txt", "frontend/requirements.txt"]:
        if Path(req_file).exists():
            with open(req_file) as f:
                packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            print(f"✅ {req_file}")
            print(f"   {len(packages)} packages defined")
        else:
            print(f"❌ {req_file} not found")

    print()


def main():
    """Main verification function."""
    print()
    verify_project()
    print()
    check_requirements()
    print("=" * 80)
    print("VERIFICATION COMPLETE")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
