---
name: disk-archive
description: Archive large inactive outputs to Dropbox with verified uploads and restore notes. Use when freeing disk space or retiring old artifacts.
---

# Disk archive

Use a project's own archive tool when its documents name one; this policy still applies to what it uploads.

- Keep an active working set: source code, essential dependencies, recent working data, and artifacts required by ongoing workflows.
- Aggressively archive large obsolete, inactive, reproducible, or unlikely-to-be-referenced artifacts. Treat generated outputs, renders, builds, intermediate files, old releases, and old session caches as archive candidates by default.
- Check code, configurations, scripts, running processes, and current handoffs for active references before moving anything. Historical references need restoration notes; active dependencies must remain available.
- On the user's local Mac, prefer direct `dbxcli` uploads to the verified Dropbox `projects/` directory, organized by project, date, and session. Avoid staging archive copies in a locally synced Dropbox directory or keeping redundant workspace/cache copies.
- Never upload credentials, secrets, sensitive private data, or restricted third-party datasets without explicit authorization.
- Upload first. Verify remote file sets and byte sizes, and checksums or a streamed read-back when possible. Recheck local inputs for changes before removing only the verified, inactive local copies. Preserve source, unique datasets, credentials, active working files, and important metadata; never infer inactivity from age alone.
- Maintain `~/ARCHIVE_INDEX.md` for every archive and removal on that machine: original path, remote path, size, verified purpose versus inferred context, checksums/receipts, and exact restoration instructions. Keep manifests and small recovery records locally.
- Apply this policy proactively where the storage environment supports it. Do not assume local Mac paths or Dropbox access on remote clusters. Measure actual free-space changes; APFS clones and shared extents make logical archived bytes different from physical bytes recovered.
