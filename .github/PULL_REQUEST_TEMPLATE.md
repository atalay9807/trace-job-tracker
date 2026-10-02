## What this changes

<!-- One or two sentences. The diff says what; explain why. -->

## Related issue

<!-- Closes #123, or "none — typo fix". Larger changes need an issue first. -->

## Verification

Paste the output, or say plainly which command you could not run and why.
An honest "I could not test this" is acceptable; an untested claim is not.

```
python3 src/veri.py
python3 -m unittest discover -s tests -v
python3 src/build_dashboard.py --site
npm ci --ignore-scripts
npm test
git diff --check
```

<!-- paste results here -->

## Checklist

- [ ] Generated files were regenerated, not hand-edited
      (`site/app.html` comes from `src/dashboard.template.html`)
- [ ] No real application records, real CV-derived profile, or third-party
      name or email address is included
- [ ] No invented URL — unverified links are Gmail search deep links
- [ ] The three measurement limits are still labelled in the interface
- [ ] Changed constants were updated in code *and* in their documentation
      (`config/rules.yaml`, `.claude/skills/`)
- [ ] User-visible strings have both a Turkish and an English entry
- [ ] Commit messages are in English, first line ≤ 72 characters, with no
      model name or session identifier
