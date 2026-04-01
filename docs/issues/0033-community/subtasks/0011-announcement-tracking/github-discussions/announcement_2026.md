# Immich AutoTag – Major New Release Announcement

Hi Immich community!

I'm excited to announce a major new release of **Immich AutoTag**, the open-source tool for automatic photo and video classification and tagging in Immich.

## What’s new and improved in this release?

- 🚀 **Instant CLI from PyPI**: Run Immich AutoTag instantly with `pipx run immich-autotag` – no manual setup or environment creation required.
- 📝 **Quick Start & User-Focused Docs**: Clear, user-friendly documentation and a streamlined Quick Start guide.
- 🛠️ **Flexible Configuration**: Now supports both YAML and Python config files, with self-documented templates for easy customization.
- 🏷️ **Advanced Tagging & Album Logic**: Automatic classification based on albums, tags, and duplicates.
- 🕒 **Automatic Date Repair**: Detects and fixes incorrect or missing dates for your assets based on filenames and duplicate analysis.
- ⚠️ **Conflict Detection**: Instantly highlights assets with conflicting classifications, so you can resolve issues quickly.
- ❓ **Unclassified Asset Detection**: Easily find which photos or videos remain unorganized or unclassified.
- 🔄 **Continuous Tagging Script**: New loop script for continuous asset tagging/classification during heavy editing sessions.
- 📊 **Detailed Logs & Statistics**: Automatic generation of modification reports and statistics for tracking your library’s organization.
- 🗂️ **Exclude Assets by Web Link**: Easily exclude specific assets from processing.
- 🗃️ **Automatic Album Creation from Folders**: Now stable and enabled by default!
- 🐳 **(Experimental) Docker Support**: Early Docker image available for testing (not yet officially documented).

## Why use Immich AutoTag?
- Save hours organizing large photo libraries.
- Instantly detect unclassified or conflicting assets.
- Automate repetitive tagging and album management tasks.
- Keep your photo dates accurate and consistent.

## Get Started
- See the [README](https://github.com/txemi/immich-autotag#quick-start) for instant setup instructions.
- Full changelog: [CHANGELOG.md](https://github.com/txemi/immich-autotag/blob/main/CHANGELOG.md)

## Feedback & Support
- Questions, issues, or feature requests? Open a ticket on [GitHub Issues](https://github.com/txemi/immich-autotag/issues).

*(Previous announcement for reference: [https://github.com/immich-app/immich/discussions/24764](https://github.com/immich-app/immich/discussions/24764))* 

Thank you for your support and feedback!

---

## v0.80.0 — 2026-03-31

# Immich AutoTag v0.80.0 – User Groups, Smarter Rule Engine, Continuous Batch Mode & More!

Hi Immich community!

I'm excited to announce **v0.80.0** of **Immich AutoTag** — a major milestone that consolidates months of work across user permissions, rule engine improvements, and production-grade stability. This release marks the beginning of our stabilization roadmap toward v1.0.0.

## What's new in v0.80.0?

- 👥 **User Permissions & Groups:** Automatic assignment of permissions to users based on configured rules; full Phase 1+2 synchronization system now consolidated, stable, and tested with 500+ albums.
- 🔁 **Continuous Batch Mode:** The tool now runs continuously and automatically processes new assets as they arrive — fully stable for long-running production deployments.
- 🧩 **Enhanced Rule Engine:** Supports both regex patterns and simplified common-use patterns for flexible, powerful classification.
- 🗂️ **Duplicate Album-Name Recovery:** New flow with cleanup and rename strategies to resolve same-name album conflicts safely.
- ⚙️ **Configurable Execution Phases:** Enable/disable key phases independently (album assignment, classification validation, duplicate-tag analysis, album-date consistency, tag conversions).
- 🏥 **Automatic Temporary Album Cleanup:** Detects and removes unhealthy temporary albums.
- ✅ **Checkpoint Resume (stable):** Resume processing from the last processed asset after any interruption — now stable and enabled by default.
- 🗃️ **Auto Album Creation from Folders (stable):** Now stable and enabled by default.
- 🔧 **API Architecture Refactor:** Modular entrypoints (albums/assets/tags/users/server) for improved maintainability and architectural boundaries.

## ⚠️ Known Issue — Docker

In some environments, the **Docker image** (`0.80.3`) may fail to access the Immich API (suspected DNS/network issue). If you hit this, use the **pipx** method instead:

```bash
pipx run immich-autotag
```

Tracked at [GitHub Issue #43](https://github.com/txemi/immich-autotag/issues/43). Fix in progress.

## Get Started

- 📖 [Quick Start (README)](https://github.com/txemi/immich-autotag#quick-start)
- 📋 [Full Changelog](https://github.com/txemi/immich-autotag/blob/main/CHANGELOG.md)
- 🐣 [Explain Like I'm 5 (ELI5)](https://github.com/txemi/immich-autotag/blob/main/docs/explain-like-im-5.md)

## Feedback & Support

Questions, issues, or feature requests? → [GitHub Issues](https://github.com/txemi/immich-autotag/issues)

*(Previous major announcement: [https://github.com/immich-app/immich/discussions/25164](https://github.com/immich-app/immich/discussions/25164))*

Thank you for your continued support!

<!-- STATUS: draft — not yet posted -->
