# Coresearch development

Python 3.10+ and the standard library only. The installable, self-contained
payload is `skills/coresearch/`; this file is not installed into research projects.

`scripts/coresearch.py` installs skills, creates `research/brief.md`, and, only
through its `host` command, renders `host/` into the user's global agent files.
Evaluate a change to `host/` with `evals/host-policy` before installing it; that
evaluation uses live accounts and is not part of the unit tests. Name every model
it uses; Fable and Astra need the user's grant (`evals/host-policy/grants.py`),
which only the user makes, so ask for it and never create or work around one.

Local validation: `python3 -B -m unittest discover -s tests -v`.
Tests use disposable directories and mocked network boundaries, with no account
or production access. These checks and corrections need no intermediate approval.
