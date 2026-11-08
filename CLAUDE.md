# PTS – Production Tracking System

Intern webapp for å følge produksjonsjobber hos eksterne leverandører. Leverandører har ikke tilgang til systemet; de oppdaterer en kontrollert Excel-fil som valideres og godkjennes før databasen oppdateres. Dette er Radmilas prosjekt i IBE160, planlagt med BMAD.

## Planleggingsdokumenter

- Product brief: `.docs/planning-artifacts/briefs/PRODUCT_BRIEF.md`
- PRD: `.docs/planning-artifacts/prds/` (lages med `/bmad-prd`)

## Arbeidsregler

- Briefen og PRD-en styrer prosjektet. Endres et krav, oppdateres PRD-en først, deretter arkitektur, stories og kode.
- Spør før du tar beslutninger som ikke står i briefen eller PRD-en; marker antakelser med `[ASSUMPTION]`.
- Bare fiktive data i repoet – ingen ekte bedriftsdata, tegninger eller leverandørnavn.
- Chat på norsk. Dokumenter, kode og kommentarer på engelsk.
- Commit etter hvert fullførte steg.

## Sesjonslogg

Når en oppgave eller økt avsluttes, før sluttoppsummeringen, bruk `sesjonslogg`-skillen: dokumenter Oppgave + Plan + Resultat + åpne punkter i `.logs/<bruker>/`, og før åpne punkter i `.logs/<bruker>/issues.md`. Skillen committer loggfila lokalt; push gjør du selv. Gruppens egne regler for commit og språk gjelder foran dette.
