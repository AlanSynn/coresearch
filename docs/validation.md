# Validation

Run from the checkout:

```bash
python3 -B -m unittest discover -s tests -v
```

## Automated contracts

The suite uses real temporary files and subprocess CLI calls, with HTTP/DNS/TLS
boundaries mocked. It covers copies and links, idempotency, refusal of conflicts
and recursive installs, preservation of host prompts and existing briefs,
cleanup after copy failure, publish-last skill metadata, and a copied utility
running outside the checkout.

Source tests cover manifest validation, byte/hash provenance, relative redirects,
redirect revalidation and limits, mixed public/private DNS answers, IP-pinned TLS
with the original hostname, private/reserved/multicast targets, invalid schemes
and credentials, timeouts, bad PDF signatures, truncated and oversized responses,
partial-batch reports, interruption, and refusal to reuse output directories.
Dry-run performs no network requests or writes.

Bundle tests check local Markdown links, one discoverable skill, routing-only
frontmatter, portable dependencies, and an installed end-to-end fixture workflow.
This is software integration testing, **not** an evaluation of a model's research
quality. The PDF transport fixture is synthetic and is never represented as a
real publication or verified scientific evidence.

## Host scenarios

These are acceptance scenarios for a configured model host, not a mandatory
workflow and not claims that live agents were exercised by the unit tests.

| Scenario | Expected behavior and evidence |
|---|---|
| One citation correction | Inspect the relevant source and edit the claim directly. No project initialization, worker, whole-repo preload, or stage re-entry. |
| Broad research idea to experiment | Astra chooses a discriminating experiment. A bounded worker may implement/test it. Actual commands and results support the final interpretation, including negative evidence. |
| Independent literature collection | Workers get disjoint search scopes and return source locators, verification limits, and compact findings. Astra resolves overlap and contradictory results without ingesting full transcripts. |
| Manuscript/rebuttal | Reuse the existing draft. Separate proposed changes from implemented ones and unrun experiments from results. Finish revisions and verification within authorization. |
| Resuming a project | Read the relevant brief/artifacts, not every skill. Preserve rejected directions and uncertainty; update notes only as needed. |
| No worker or search tool available | Do supported work directly; state any evidence gap rather than invent a worker result, citation, or successful experiment. |
| A consequential permission boundary | Continue safe independent work, but do not publish, expose restricted data, or consume unapproved resources. Ask only for the unresolved decision. |

Evaluate both the quality of the deliverable and overhead: unnecessary loaded
references, worker launches, repeated status checks, and user approvals. No
numerical performance improvement is claimed without comparative host runs.

## Final-review boundary

The redesign can be reviewed structurally: one payload, no runtime dependencies,
no orchestration or prompt injection, explicit lead/worker responsibility, and
research standards available on demand. The tests establish those software
contracts. Live Astra/Claude delegation, external publisher availability, and
host skill-discovery behavior additionally require the user's configured runtime
and authorized network. Record those runs separately rather than treating an
offline test pass as proof of them.
