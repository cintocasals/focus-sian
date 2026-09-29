# Focus & Sian · the council of two

**English** · [Español](#español) · [Català](#català)

Two AI advisors that debate your project until they agree on a strategy, and show you how they got there.

- **Focus** is inspired by **Steve Jobs's method**: start from the customer experience, say no to almost everything,
  be clearly better or don't bother, decide with a demo, one owner per thing.
- **Sian** is inspired by **Taiichi Ohno's method** (Toyota Production System): facts before opinions, real demand,
  flow, waste, visible problems, small experiments, spend money last.

Jobs asks what is worth doing; Ohno asks what is being wasted. The value is in the friction.

> Focus and Sian are simulations inspired by the methods of Steve Jobs and Taiichi Ohno, built from their own
> words and from first-hand accounts. They are not those people and do not speak for them. Not affiliated with
> Apple or Toyota.

## How it works

| # | Phase | What happens |
|---|---|---|
| 0 | Brief | You describe the project and attach documents. The moderator builds a fact dossier |
| 1 | Questions | Each advisor may ask you up to three questions (optional) |
| 2 | Strategies | Each advisor writes its strategy **without seeing the other's** |
| 3 | Cross-critique | Each one analyses the other's strategy: strengths, objections, unseen risks |
| 4 | Rebuttal | Each one concedes what the evidence supports and holds the rest |
| 5 | Joint strategy | A neutral moderator drafts it, both sign it (or not), open disagreements stay visible |
| 6 | Approval | You approve, ask for changes, or send a point back to debate |
| 7 | Execution prompt | After your approval: a detailed prompt to give to an AI that will carry out the project, reviewed by both |

Every phase leaves a file, and an **acta** (minutes page, `acta.html`) shows the whole path from your brief to the
conclusion: what each advisor proposed, what they criticised, what each conceded and why, and where they still
disagree. The moderator never averages opinions and never invents agreement.

## Install

- **Claude desktop app:** download [`dist/focus-sian.plugin`](dist/focus-sian.plugin),
  open it in a conversation and accept it.
- **Claude Code:** add this repository as a marketplace and install the plugin:
  ```
  /plugin marketplace add cintocasals/focus-sian
  /plugin install focus-sian@focus-sian
  ```
  To get new versions: `/plugin marketplace update focus-sian`.

Needs a Claude plan. Works best where Claude can launch subagents (Claude desktop with plugins, Claude Code): then
the two advisors really work independently. Elsewhere it falls back to a single context and says so in the acta.

## Use

Just ask, in any language:

- "Focus and Sian: debate this project" + your description and documents.
- "Que Focus i Sian analitzin si hem d'obrir una segona línia de producte."
- "Consejo Focus & Sian: ¿cómo lanzamos este servicio?"

Then approve the joint strategy (or ask for changes) and ask for the execution prompt. You can also ask one advisor
alone: "What would Sian say about hiring before we have the orders?"

## Optional configuration

Put a file called `focus-sian-config.md` in your working folder to set where debates are saved, extra knowledge
sources (a documents folder, a company knowledge base or search command) and standing context about your company.
Format: `skills/debate/references/config.md`.

## What's inside

- `agents/focus.md`, `agents/sian.md`: the two advisors (method, questions, blind spots, verified quotes only).
- `skills/debate/`: the moderator (protocol, templates, execution-prompt template, acta builder in plain Python).

## Sources

The advisors are built from two research dossiers with over a hundred sources: for Ohno, his book *Toyota
Production System* (1978), *Workplace Management* (1982) and first-hand accounts of people he trained; for Jobs,
*Make Something Wonderful* (Steve Jobs Archive, 2023), his interviews and talks, and accounts by Catmull, Kocienda,
Lashinsky and Isaacson. Quotes known to be misattributed are excluded on purpose.

© 2026 Cinto Casals · [cintocasals.com](https://www.cintocasals.com)

---

## Español

Dos asesores de IA que debaten tu proyecto hasta ponerse de acuerdo en una estrategia, y te enseñan cómo han
llegado a ella.

- **Focus** se inspira en el **método de Steve Jobs**: empezar por la experiencia del cliente, decir que no a casi
  todo, ser claramente mejor o no hacerlo, decidir con una demostración, un responsable para cada cosa.
- **Sian** se inspira en el **método de Taiichi Ohno** (Sistema de Producción Toyota): hechos antes que opiniones,
  demanda real, flujo, despilfarro, problemas visibles, experimentos pequeños, gastar lo último.

Jobs pregunta qué vale la pena hacer; Ohno, qué se está desperdiciando. El valor está en la fricción.

> Focus y Sian son simulaciones inspiradas en los métodos de Steve Jobs y Taiichi Ohno. No son ellos y no hablan
> en su nombre. Sin relación con Apple ni con Toyota.

**Cómo funciona:** planteamiento → preguntas (opcional) → dos estrategias independientes → crítica cruzada →
réplica → estrategia conjunta firmada por los dos → tu aprobación → prompt de ejecución. Cada fase deja un fichero y
el **acta** (`acta.html`) muestra todo el camino: qué propuso cada uno, qué criticó, qué cedió y por qué, y dónde
siguen sin estar de acuerdo.

**Instalación:** en la app de escritorio de Claude, descarga `dist/focus-sian.plugin`, ábrelo en una conversación y
acéptalo. En Claude Code: `/plugin marketplace add cintocasals/focus-sian` y `/plugin install focus-sian@focus-sian`.

**Uso:** «Consejo Focus & Sian: debatid este proyecto» con tu descripción y tus documentos. Luego aprueba la
estrategia conjunta y pide el prompt de ejecución.

**Configuración opcional:** un fichero `focus-sian-config.md` en tu carpeta de trabajo con la carpeta de debates,
fuentes de conocimiento y contexto fijo de tu empresa.

---

## Català

Dos assessors d'IA que debaten el teu projecte fins que es posen d'acord en una estratègia, i t'ensenyen com hi
han arribat.

- **Focus** s'inspira en el **mètode de Steve Jobs**: començar per l'experiència del client, dir que no a gairebé tot,
  ser clarament millor o no fer-ho, decidir amb una demostració, un responsable per a cada cosa.
- **Sian** s'inspira en el **mètode de Taiichi Ohno** (Sistema de Producció Toyota): fets abans que opinions, demanda
  real, flux, malbaratament, problemes visibles, experiments petits, gastar l'últim.

Jobs pregunta què val la pena fer; Ohno, què s'està malbaratant. El valor és a la fricció.

> Focus i Sian són simulacions inspirades en els mètodes de Steve Jobs i Taiichi Ohno. No són ells i no parlen en
> nom seu. Sense relació amb Apple ni amb Toyota.

**Com funciona:** plantejament → preguntes (opcional) → dues estratègies independents → crítica creuada → rèplica
→ estratègia conjunta signada pels dos → la teva aprovació → prompt d'execució. Cada fase deixa un fitxer i l'**acta**
(`acta.html`) ensenya tot el camí: què va proposar cadascú, què va criticar, què va cedir i per què, i on encara no
estan d'acord.

**Instal·lació:** a l'app d'escriptori de Claude, descarrega `dist/focus-sian.plugin`, obre'l en una conversa i
accepta'l. A Claude Code: `/plugin marketplace add cintocasals/focus-sian` i `/plugin install focus-sian@focus-sian`.

**Ús:** «Consell Focus & Sian: debateu aquest projecte» amb la teva descripció i els teus documents. Després aprova
l'estratègia conjunta i demana el prompt d'execució.

**Configuració opcional:** un fitxer `focus-sian-config.md` a la carpeta de treball amb la carpeta de debats, fonts
de coneixement i context fix de la teva empresa.
