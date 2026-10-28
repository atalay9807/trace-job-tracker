# Verification reports

Every completed step of the web application is checked by the `code-verifier`
agent before it is committed. Its report is saved here **verbatim**, one file
per step:

```
YYYY-MM-DD-<step-slug>.md
```

The main session writes its response under the report — what it fixed, what it
disputes and why. It never edits or removes the verifier's text, so the file
records both the finding and the decision taken on it.

A report with a `BLOCKER` finding means the step is not done.
