# Rule–Evidence Matrix

The matrix is a bundled trace from rules to captured version decisions. `High`
means explicit or repeatedly selected. `Medium` means conditional or supported
by fewer iterations.

| ID | Rule | Section | Bundled evidence | Type | Confidence | Scope |
|---|---|---|---|---|---|---|
| R01 | Retell one causal story across sections | Global | writing notes synthesis | Explicit | High | General |
| R02 | Every Abstract sentence adds problem/contribution information | Abstract | notes + opening chain | Explicit | High | General |
| R03 | Avoid examples in Abstract unless indispensable | Abstract | writing notes | Explicit | High | General |
| R04 | Put concrete failure before abstract diagnosis | Abstract/Intro | D04 | Explicit | High | General |
| R05 | Delete redundant restatement after full explanation | Global | D04–D05 | Explicit | High | General |
| R06 | Parallelize distinct causes at matching abstraction | Global | D06 | Explicit | High | General |
| R07 | Ground non-obvious findings in analyses | Abstract/Intro | D07 | Explicit | High | General |
| R08 | Cover all central contribution classes in Abstract | Abstract | contribution feedback | Explicit | High | General |
| R09 | Prefer evidence axes over implementation names in Abstract | Abstract | D08 | Inferred | High | General |
| R10 | End Abstract on a supported bounded principle | Abstract | ending chain | Inferred | High | General |
| R11 | Introduction expands rather than copies Abstract | Intro | D09 | Explicit | High | General |
| R12 | Use field progress to expose a boundary when useful | Intro | D09 | Inferred | High | Conditional |
| R13 | Give each paragraph one main role | Intro/Method | D11 | Inferred | High | General |
| R14 | End a paragraph with a premise usable by the next | Intro | paragraph handoff revisions | Explicit | High | General |
| R15 | Explain mechanism before method assertion | Intro | P1/P5 decisions | Explicit | High | General |
| R16 | Make examples perform reasoning | Intro | writing notes + example revision | Explicit | High | General |
| R17 | Use opposing failures to derive a prerequisite | Intro | D10 | Inferred | High | Conditional |
| R18 | Group prior work; avoid paper-by-paper Introduction listing | Intro/RW | writing notes | Explicit | High | General |
| R19 | Make a major evidence figure part of the argument | Intro/Figure | D12 | Explicit | High | General |
| R20 | Stop evidence blocks at their licensed conclusion | Intro/Figure | D12–D14 | Inferred | High | General |
| R21 | Claim trend correspondence, not pointwise equality | Intro/Figure | D14 | Inferred | High | General |
| R22 | Introduction Method keeps distinguishing mechanisms | Intro | D15 | Inferred | High | General |
| R23 | Introduction experiments emphasize conclusions over dense numbers | Intro | D16 | Explicit | High | Conditional |
| R24 | Contributions map distinct scientific additions | Intro | D17 | Inferred | High | General |
| R25 | Method retells Introduction with operations and symbols | Method | writing notes synthesis | Explicit | High | General |
| R26 | Preliminaries defines the smallest sufficient setup | Method | D18 | Explicit | High | General |
| R27 | Overview maps components/dependencies rather than setup | Method | D19 | Explicit | High | General |
| R28 | Introduce notation just in time | Method | D18, D23–D25 | Explicit | High | General |
| R29 | Distinguish model from mapping/distribution/output | Method | preliminaries feedback | Explicit | High | General |
| R30 | Use connection→formula→immediate explanation | Method | method revisions | Explicit | High | General |
| R31 | Let one formula perform one logical action | Method | D21 | Inferred | High | General |
| R32 | Define ideal objective before approximation | Method | D22 | Inferred | High | General |
| R33 | Express priority order explicitly when lexicographic | Method | search design | Project-Specific | High | Conditional |
| R34 | Move implementation-only settings out of Method | Method | notes + method feedback | Explicit | High | General |
| R35 | Audit notation across the entire Method and assets | Method | D23–D25, D28 | Explicit | High | General |
| R36 | State component roles before complex operation | Method | D20 | Inferred | High | General |
| R37 | For multi-branch methods, specify shared/different state | Method | D26–D27 | Project-Specific | High | Conditional |
| R38 | State fusion/update order when it changes semantics | Method | D27 | Project-Specific | High | Conditional |
| R39 | Avoid guarantee verbs unsupported by proof/evidence | Global | D27 | Inferred | High | General |
| R40 | Make captions locally self-contained | Figures | writing notes | Explicit | High | General |
| R41 | Align artwork, caption, symbols, and main text | Figures | D28 | Explicit | High | General |
| R42 | Let table captions describe setting, not superiority | Tables | writing notes | Explicit | High | General |
| R43 | Organize Experiments by paper questions | Experiments | writing notes | Explicit | High | General |
| R44 | Ablate components with controlled variables | Experiments | notes + experiment outline | Explicit | High | General |
| R45 | Audit grammar, citations, equations, compilation, and visuals | Global | writing notes | Explicit | High | General |
| R46 | Treat length ranges as working targets | Abstract/Intro | length feedback | Explicit | Medium | Conditional |
| R47 | Inspect layout whitespace and orphan short lines | Global | layout notes | Explicit | Medium | Conditional |
| R48 | Keep detailed secondary-section advice Provisional | Secondary | limited iteration history | Provisional | Medium | General |

## Evidence interpretation

- `Explicit`: directly requested in the captured writing process.
- `Inferred`: supported by repeated accepted/rejected alternatives.
- `Project-Specific`: local technical decision illustrating a conditional rule.
- `Provisional`: useful guidance without equal iteration depth.

When a current user's instruction conflicts with this matrix, follow the current
instruction and update the preference only if the new evidence is explicit or
repeated.

