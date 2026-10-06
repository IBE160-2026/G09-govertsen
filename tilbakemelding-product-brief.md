# Tilbakemelding på product brief

| | |
|---|---|
| **Gruppe** | G09 – G09-govertsen |
| **Product brief** | `PRODUCT_BRIEF.md` (commit cb4be4a) |
| **Tilbakemelding fra** | Faglærer i IBE160 (utarbeidet med KI-støtte) |
| **Dato** | 2026-10-06 |

## Samlet vurdering

- **Godt utgangspunkt med justeringer.** Gruppen kan gå videre og innarbeide punktene under.

**Det som er bra:**

1. Problemet er realistisk og godt beskrevet. Flyten Engineering → Supplier → Production → Inspection → Delivery → Internal Assembly, og eksempelet med feil mål på en tegning som krever ny revisjon, gjør det lett å forstå hva Production Tracking System (PTS) skal løse.
2. Kjerneideen er tydelig og interessant: leverandører oppdaterer et kontrollert Excel-ark, systemet validerer og viser endringene, og databasen oppdateres først når en intern bruker har godkjent importen. Det gir konkret, testbar logikk.

**De viktigste endringene:**

1. Suksesskriteriene består for en stor del av forretningsmål med plassholdere, som «[target, e.g. 50%]». De kan ikke måles i emnet. Erstatt dem med funksjonelle kriterier, for eksempel «en import med ugyldig status blir avvist med en forståelig feilmelding».
2. Valideringsreglene for Excel-importen må beskrives konkret. Hvilke felt kan leverandøren endre, hvilke statuser er gyldige, og hva er en «revisjonsmismatch» eller en «uventet endring»? Dette er hjertet i appen og det dere må kunne kontrollere.
3. Avklar brukere og innlogging i v1. Briefen nevner fire brukergrupper, men ikke om de har ulike rettigheter, eller om v1 har én intern rolle. Bestem også at dere bruker fiktive data, siden caset bygger på en reell bedrift med gradert dokumentasjon.

## Vanskelighetsgrad og gjennomførbarhet

### Vurdert vanskelighetsgrad

- **Middels**

**Sammenlignbart med:** 2) AI CV- og søknadsassistent (middels) når det gjelder filhåndtering og flere sammenhengende funksjoner, men uten KI-funksjon. Domenet minner om en sterkt avgrenset del av 4) KI-støttet MRP II, men PTS planlegger ikke produksjon, den følger opp status.

**Begrunnelse:**

| Faktor | Nivå (lav / middels / høy) | Kommentar |
|---|---|---|
| Domenelogikk – hvor mange og hvor kompliserte regler og beregninger må stemme? | Middels | Statusflyt mellom stegene, validering av leverandørfelt, sammenligning med eksisterende data og flagging av revisjonsavvik. Reglene er ikke beregningstunge, men de må være presist definert. |
| Datamodell – antall entiteter og relasjoner mellom dem | Middels | Jobb, tegning/revisjon, leverandør, avvik (issue), inspeksjon og import med endringslinjer. Revisjonshistorikk og importlogg gir flere relasjoner. |
| Brukere, roller og innlogging | Middels | Fire brukergrupper er nevnt. Hvis de skal ha ulike rettigheter, blir dette krevende. Leverandører har ikke tilgang til systemet, og det forenkler. |
| KI-funksjonalitet i appen, f.eks. kall til språkmodell, prompts i koden og håndtering av usikre svar | Lav | Ingen språkmodell i appen. Det er greit. KI-bruken ligger i utviklingsprosessen. |
| Integrasjoner og eksterne tjenester, f.eks. API-er, betaling og e-post | Lav | Ingen integrasjoner mot ERP eller andre systemer i v1. «Sende» Excel-filer bør bety å laste ned en fil, ikke å sende e-post. |
| Sanntid, samtidighet eller flere brukere som påvirker hverandre | Lav–middels | Ingen sanntid, men to importer for samme jobb kan komme i konflikt. Beskriv hva som skjer da. |
| Filhåndtering, f.eks. opplasting, PDF-lesing og eksport | Høy | Generering av Excel per leverandør, opplasting, lesing, validering og visning av endringer er den mest krevende delen. Excel-filer endret av mennesker kan inneholde mye uventet. |
| Sikkerhet og personvern | Middels | Caset nevner gradert dokumentasjon. Bruk fiktive data i repoet, og beskriv at importen aldri skriver direkte til databasen. |

**Hva vanskelighetsgraden betyr for dere:**

- _Middels:_ Et godt balansert valg. Pass på at kjerneflyten blir ferdig og stabil før dere legger til mer. For PTS er kjerneflyten: opprett jobber → eksporter Excel for én leverandør → importer utfylt fil → se valideringsfeil og endringer → godkjenn → se oppdatert status i oversikten. Få den til å virke før dere legger til inspeksjon og levering.

### Gjennomførbarhet med BMAD og Claude Code

Dere skal planlegge med BMAD (product brief → PRD → arkitektur → epics og stories) og implementere med Claude Code. Vurderingen under tar hensyn til at det må være tid til hele denne flyten, og til testing, retting og README til slutt.

| Spørsmål | Vurdering (OK / risiko / stor risiko) | Kommentar |
|---|---|---|
| **Tid og omfang** – kan v1 realistisk bli ferdig og stabil i løpet av semesteret, med tid til flere iterasjoner? | Risiko | Jobbregister, Excel-eksport, Excel-import med validering, godkjenning og dashboard er fem funksjonsområder. Det går, men bare hvis inspeksjon, levering og intern montering holdes enkle. Repoet har foreløpig bare briefen, så det haster å komme i gang med PRD. |
| **BMAD-flyten** – er briefen konkret nok til at PRD, arkitektur og stories kan lages uten store hull, og blir det overkommelig mange stories? | Risiko | Feltlisten per jobb er nyttig, men statusverdier, valideringsregler og roller mangler. Uten dem blir PRD-en og storiene vage nettopp der appen er mest krevende. |
| **Egnet for Claude Code** – bruker løsningen en vanlig, godt dokumentert teknologistakk som Claude Code håndterer godt, eller krever den nisjeteknologi, spesialmaskinvare eller mye manuell konfigurasjon? | OK | En webapp med database og et vanlig Excel-bibliotek (for eksempel openpyxl i Python eller tilsvarende i JavaScript) er godt dokumentert. |
| **Kontroll på KI-ens arbeid** – kan gruppen selv avgjøre om koden gjør det riktige? Krever domenet kunnskap gruppen ikke har, f.eks. avanserte beregninger eller fagregler, så er det vanskelig å kvalitetssikre. | OK | Domenet ser ut til å være kjent for dere, og reglene er av typen «gyldig/ugyldig», som er lett å kontrollere med eksempelfiler. |
| **Testbarhet** – finnes det tydelige regler og forventede resultater som tester kan skrives mot? | OK | Svært godt egnet: lag et sett Excel-testfiler (gyldig, ugyldig status, feil revisjon, manglende felt, endret låst felt) med forventet resultat. |
| **Kjørbar for sensor** – kan appen kjøres lokalt etter README, uten gruppens nøkler, betalte kontoer eller egen infrastruktur? | OK | Mulig med lokal database, seed-data og eksempelfiler i repoet. Planlegg dette fra starten. |
| **Avhengigheter og kostnader** – krever løsningen betalte API-er, f.eks. språkmodeller, og finnes det en plan for kostnad, testmodus eller mock-data? | OK | Ingen betalte tjenester er nødvendige. |

**Konklusjon om gjennomførbarhet:**

- **Gjennomførbart med justert omfang.** Se forslagene under.

**Forslag til justering av omfang eller vanskelighetsgrad:**

1. La v1 dekke stegene Supplier → Production → Inspection-forespørsel via Excel-utvekslingen, med én intern rolle (for eksempel produksjonsplanlegger) og enkel innlogging eller ingen innlogging. Legg inspeksjonsresultater, levering, intern montering og flere roller i senere trinn.
2. Lag en fast mal for Excel-arket med låste og redigerbare kolonner, og skriv valideringsreglene som en liste i PRD-en. Det gjør importen mye mer forutsigbar for både dere og Claude Code.

## Hvorfor product brief er viktig for mappen

Product brief er utgangspunktet for PRD, arkitektur, stories og til slutt koden. Del 1 av mappen vurderes blant annet på om sensor kan følge en sporbar vei fra plan til ferdig app. Den vurderes også på om appen gjør det dere har beskrevet, om den er testet, om den er godt designet, og om den kan kjøres etter README. Et uklart, for stort eller for lite brief gjør alt dette vanskeligere senere. Det er mye enklere å rette nå enn sent i semesteret.

## 1. Gjennomgang av briefens deler

| Del av brief | Status | Kommentar |
|---|---|---|
| Executive Summary – er det klart hva appen er, og hvilket problem den løser? | OK | Klart hva PTS er: en intern webapp for å følge produksjonsjobber, med Excel-utveksling mot leverandører. |
| The Problem – er problemet konkret, med reelle situasjoner og brukere? | OK | Konkret, med jobbflyt, typiske feil (tegningsrevisjon, manglende materialer, forsinkelser) og begrunnelsen for at leverandører ikke får tilgang. |
| The Solution – beskriver løsningen brukeropplevelsen, ikke bare teknologi? | Juster | Godt beskrevet hva som vises per jobb og hvordan importen godkjennes. Beskriv også stegene en intern bruker går gjennom, og hvordan avvik vises. |
| What Makes This Different – er vurderingen ærlig og realistisk? | OK | Realistisk avgrensning mot ERP, med tydelig fokus på kontrollert leverandørutveksling. |
| Who This Serves – er primærbrukerne tydelige, og vet vi hva de trenger? | Juster | Fire grupper er beskrevet. Velg én primærbruker for v1 og si hvilke av de andre som faktisk bruker appen i første versjon. |
| Success Criteria – kan kriteriene faktisk sjekkes eller testes? | Endre | Flere kriterier er forretningsmål med plassholdere. Behold «ingen import skrives til databasen uten godkjenning», og legg til funksjonelle kriterier for validering, endringsvisning og revisjonsflagg. |
| Scope – er det klart hva som er med i første versjon, og hva som ikke er det? | Juster | God liste over hva som er ute. «In»-delen er én setning. List funksjonene i v1 punktvis, og si om inspeksjon og levering er med. |
| Vision – henger visjonen sammen med resten uten å blåse opp omfanget? | OK | Visjonen utvider flyten med Final Approval, men holder seg til samme idé og fokus. |

## 2. Utgangspunkt for del 1 av mappen

Punktene følger kriteriene i sensorveiledningen for del 1. Vektene i parentes viser hvor mye hvert kriterium teller i del 1.

| Kriterium i del 1 | Hva briefen bør legge til rette for | Status | Kommentar |
|---|---|---|---|
| **1. Prosess og KI-styring** (30 %) | Brief som er presis nok til at PRD og stories kan bygges direkte på den, slik at krav kan spores fra brief til kode. | Juster | Godt problemgrunnlag. Valideringsregler, statusverdier og roller må inn for at storiene skal kunne spores. Legg gjerne briefen i en BMAD-mappestruktur når dere lager PRD. |
| **2. Funksjonalitet og omfang** (20 %) | Realistisk omfang for gruppen og semesteret: en tydelig kjerneflyt som kan bli ferdig og stabil, og nok innhold til å vise reell funksjonalitet. | Juster | Nok reell funksjonalitet, men fare for at hele flyten til intern montering blir for mye. Avgrens v1 som foreslått over. |
| **3. Kvalitetssikring og testing** (15 %) | Suksesskriterier og funksjoner som er konkrete nok til å bli testtilfeller. | Juster | Importvalideringen er ideell for tester, men kriteriene må skrives som testbare regler. |
| **4. Design og brukeropplevelse** (10 %) | Tydelige brukere og brukssituasjoner som designet kan bygges rundt, gjerne med de viktigste skjermbildene eller flytene skissert. | Juster | Dashboardet og godkjenningsskjermen for import er tydelige kandidater. Skisser hvordan endringer og feil vises før godkjenning. |
| **5. Kodekvalitet og arkitektur** (10 %) | Teknologivalg som er begrunnet og ikke mer komplekse enn appen trenger. | OK | Briefen tar ikke teknologivalg. Hold arkitekturen enkel: én webapp og én lokal database. |
| **6. README og kjørbarhet** (10 %) | Løsning som andre kan kjøre lokalt uten betalte kontoer, og uten tilgang til gruppens egne tjenester og nøkler. | OK | Ingen eksterne tjenester. Legg ved seed-data og eksempel-Excel-filer slik at sensor kan prøve importen. |
| **7. Ryddighet i repoet** (5 %) | En plan for hvor hemmeligheter, testdata og dokumentasjon skal ligge. | Juster | Planlegg en egen mappe for testfiler og fiktive data. Ingen ekte bedriftsdata eller tegninger skal ligge i det offentlige repoet. |

## 3. Neste steg for gruppen

1. Skriv om suksesskriteriene til funksjonelle, testbare kriterier, og fjern eller flytt forretningsmålene med plassholdere til visjonen.
2. Beskriv Excel-malen (låste og redigerbare felt), gyldige statuser og valideringsreglene, inkludert hva som regnes som revisjonsavvik. Lag 4–5 eksempelfiler med forventet resultat.
3. Bestem rolle og innlogging for v1 og hvilke steg i jobbflyten som er med, og gå deretter videre til PRD.

Oppdater product brief i repoet når dere har gjort endringene, slik at historikken viser hvordan planen utviklet seg. Det er en del av prosessen sensor ser etter.
