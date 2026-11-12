# Tilbakemelding på PRD

| | |
|---|---|
| **Gruppe** | G09 – G09-govertsen |
| **PRD vurdert** | `.docs/planning-artifacts/prds/prd-PTS-2026-11-08/prd.md` (status `final`, sist endret 2026-11-08, commit 965c0ce) |
| **Dato** | 2026-11-12 |
| **Type** | Formativ tilbakemelding, ikke karakter |

## 1. Samlet inntrykk

Dette er en sterk PRD med tydelig tese, presise regler og krav som kan bli testtilfeller direkte. Risikoen ligger ikke i manglende substans, men i tre ting: noen sentrale regler (W14/W15, revisjonsavvik) er definert litt ulikt på ulike steder, grensen mellom Core og Extension er ikke renere enn at Extension-innhold ligger inne i Core-krav, og Core er stort for ett semester.

## 2. Dette fungerer godt

1. **Avveininger er synlige.** §0.1 viser hva som er endret og hvorfor, og FR-28 sier åpent: «Accepted risk for v1: a supplier-changed cell wins over a manual update on approval, and W15 is the only guard.» Det er en beslutning med pris, ikke en glatt formulering.
2. **Testbarhet er gjennomgående.** Hvert FR har «Consequences (testable)» med konkrete verdier (FR-24: forventet dato 09.12.2026 mot frist 27.11.2026 gir *Delayed*), og FR-27 knytter 15 eksempelfiler til forventet resultat per rad. Reglene F1–F4, R1–R7 og W8–W15 har stabile ID-er fra briefen til tester.
3. **Tydelig avgrensning og tese.** §6 og §7.2 sier hva PTS ikke er og hva som er utsatt, med begrunnelse. Motmålene SM-C1 («warnings are never hidden or collapsed by default») og SM-C2 (Approve er aldri forhåndsvalgt) følger av tesen om tillit til dataene.

## 3. Oversikt per dimensjon

| Dimensjon | Vurdering | Kort begrunnelse |
|---|---|---|
| Beslutningsklarhet | sterk | Valg og aksepterte risikoer er navngitt (§0.1, FR-28). Bare ett åpent spørsmål (§10), og det er reelt. |
| Substans | sterk | Én persona som driver alle reiser, domenespesifikke regler og NFR-er med tall (NFR-4, NFR-5). Ingen pynt. |
| Strategisk sammenheng | sterk | Tese: databasen er det eneste gyldige bildet, endringer skjer bare ved godkjenning eller registrert manuell oppdatering. Funksjonene og SM-ene følger av den. |
| Testbarhet | god | Nesten alle FR-er er testbare. W14/W15 og *Revision mismatch* har motstridende vilkår (se 4.1, 4.3). |
| Scope og avgrensning | god | Non-goals og Core/Extension er eksplisitte, men blandet inn i enkeltkrav og Core er stort (se 4.2). |
| Brukbarhet for neste fase | god | Glossar, kontiguøse ID-er og skisser i addendum. Noen FR-er er ikke koblet til noen reise (se 4.4). |
| Formtilpasning | sterk | Intern enkeltrolle-app med reiser og kapabilitetskrav. Passer. |

## 4. Viktigste forbedringer

### 4.1 W14 og W15 er definert ulikt i FR-14, FR-15, FR-20, FR-28 og addendum A2.2
- **Alvorlighet:** høy
- **Hvor:** FR-14 («W14 … this file changes the same field to a different value»), FR-15 («shown as *kept* … with W14 or W15»), FR-28 («shows W15 for the affected fields»), addendum A2.2 (rad F = E, D ≠ E: «kept with W14/W15»).
- **Problem og hvorfor det betyr noe:** Ifølge FR-14 og FR-20 får W14 bare rader der filen endrer feltet. Ifølge FR-15 og A2.2 kan W14 også vises for en celle leverandøren ikke rørte. W15 er derimot uttrykkelig uavhengig av om leverandøren endret cellen. Dette er appens vanskeligste regel, og to utviklere eller to tester vil tolke den ulikt. SM-8 (primærmål) hviler på W14.
- **Forslag:** Bruk E/D/F fra A2.2 som eneste definisjon og skriv den ett sted i PRD-en. Velg samme logikk for begge: «W14/W15 vises når D ≠ E (endret etter eksport) og F ≠ D». Legg inn et eksempel som testkonsekvens: *E = Stoppet, D = I produksjon (manuell oppdatering), F = Stoppet* gir «beholdt: I produksjon» med W15, ikke anvendt. *Samme E og D, F = Ferdig* gir D → F med W15, anvendt. Gjør W14 tilsvarende og rett UJ-6, FR-20 og SM-8.

### 4.2 Core og Extension er blandet, og Core er stort
- **Alvorlighet:** medium
- **Hvor:** FR-14 («Priority: per warning, as marked»), FR-27 (Core, men med filer for W9, W12, W13), SM-8 (primær, men avhenger av Extension-regelen W14), NFR-7.
- **Problem og hvorfor det betyr noe:** Et FR med flere prioriteringer kan ikke bli én story, og «Core er ferdig og stabil» blir uklart hvis Core-krav inneholder Extension-arbeid. Core har rundt 25 av 30 FR-er, inkludert Excel-mal med validering, 15 testfiler og flerimport.
- **Forslag:** Del FR-14 i «FR-14a Core-advarsler (W8, W10, W11)» og «FR-14b Extension-advarsler (W9, W12–W15)». Del FR-27-tabellen i en Core-kolonne og en Extension-kolonne, og merk SM-8 og SM-15 som Extension. Definer en «Core-minimum» dere kan levere først, for eksempel FR-1, 3, 5–13, 15, 17, 18, 21–24, 26, med FR-19/20 rett etter.

### 4.3 «Revision mismatch» har to definisjoner
- **Alvorlighet:** medium
- **Hvor:** §3 («a returned supplier file reports a revision other than the job's current revision (warning W8)») mot FR-24 («an approved import reported a revision other than the one that was current … when the import was approved»).
- **Problem og hvorfor det betyr noe:** W8 beregnes mot nåværende data hver gang importen vises (FR-20). Flagget i FR-24 fastsettes ved godkjenning. Hva skjer hvis revisjonen endres etter godkjenning? Dashboard og tester trenger ett svar.
- **Forslag:** Gi flagget et eget navn i glossaret, for eksempel *Revisjonsavvik-flagg*, og legg til en scenariotest: «Fil melder B, gjeldende er C, import godkjennes: flagg satt. Planlegger registrerer D: flagget fjernes, *New revision* settes.»

### 4.4 Krav uten reise, og tolv ubekreftede antakelser i en PRD med status `final`
- **Alvorlighet:** lav
- **Hvor:** §0 («the 'Realized by' line … is the complete journey-to-FR mapping»); §11.
- **Problem og hvorfor det betyr noe:** FR-2, FR-4, FR-17, FR-26, FR-27, FR-29 og FR-30 står ikke i noen «Realized by»-linje, så påstanden stemmer ikke. Antakelser som avgjør testutfall (tekstdatoformater, tom forventet dato, *Completed* med delvis antall, FR-30 «ignored, not rejected») bør bli beslutninger før stories.
- **Forslag:** Legg til manglende FR-er i riktig reise, eller skriv «unntatt støttekrav». Bekreft de testpåvirkende antakelsene og fjern `[ASSUMPTION]`-merket når de er avgjort.

## 5. Mekaniske funn

- FR-1 … FR-30, UJ-1 … UJ-6 og SM-1 … SM-16 med SM-C1/C2 er komplette, uten duplikater. Rekkefølgen i §4 er ikke numerisk, og det er forklart i §0.
- Alle inline `[ASSUMPTION]` står i §11, og indeksen har ingen oppføringer uten treff.
- «Reject» brukes om rad (R-regler), import (tilstand `Rejected`) og fil (F-regler). Konsekvent bruk av «Rejected row», «Rejected import» og «File rejection» ville gjøre det tydeligere.
- Skjermbildene i addendum bruker emoji som plassholdere. Det er greit, siden de er merket som plassholdere.
- PRD-en er lang (ca. 8 400 ord). Struktur og glossar gjør den brukbar, men §0.1 kan flyttes til addendum når PRD-en er stabil.

## 6. Før dere går videre

**Må avklares før UX, arkitektur og epics:**
- Én definisjon av W14/W15 (4.1) og av *Revision mismatch* (4.3). Arkitekturen avhenger av hva som lagres og hva som beregnes.
- Hva som faktisk er Core-minimum (4.2), slik at epics får riktig rekkefølge.

**Kan vente:**
- Layout i jobbregisteret (§10, avgjøres i `bmad-ux`).
- Antakelser om filstørrelse, nettleser og antall rader, så lenge de bekreftes før testing.

**Oppfølging av tilbakemeldingen på product brief:** ja. Suksesskriteriene er gjort funksjonelle (SM-1 … SM-12), valideringsreglene er konkrete, Excel-malen er beskrevet med låste og redigerbare kolonner, én rolle uten innlogging og fiktive data er bestemt, og eksempelfiler med forventet resultat finnes i FR-27. Sketsjer ligger i addendum A3.

## 7. Refleksjonsspørsmål

1. FR-28 beskriver bevisst at leverandørens endring vinner over en manuell oppdatering. Hvordan kom dere frem til det, og hvilke alternativer vurderte dere og forkastet?
2. Hvordan sjekket dere at regelsettet W8–W15 er konsistent? Prøvde dere E/D/F-tabellen med konkrete verdier, eller godtok dere KI-ens formuleringer slik de var?

_Vurdert mot kvalitetsrubrikken i bmad-prd. Dette er veiledning, ikke sensur._
