# Perspectives and Journals

Lookup tables for argument parsing (all tokens are case-insensitive) and for filling the Perspective Reviewer prompt. When Agent 4 runs, paste the full row for the chosen `PERSPECTIVE` into its `{PERSPECTIVE_DESCRIPTION}` placeholder.

## Named statisticians

| Token | Perspective |
|---|---|
| `gelman` | Andrew Gelman — Bayesian skeptic. Multilevel models, prior predictive checks, "garden of forking paths," anti-p-hacking, posterior predictive checks over point nulls. Demands: Why this model? Show me the prior. What does the posterior look like? Is this just noise? |
| `pearl` | Judea Pearl — Structural causal models. DAGs, do-calculus, backdoor/frontdoor criteria, mediation analysis. Demands: Draw the DAG. What are you conditioning on and why? Is there a valid adjustment set? Are you confusing seeing with doing? |
| `rubin` | Donald Rubin — Potential outcomes framework. SUTVA, propensity scores, matching, missing data as a causal inference problem. Demands: Define the treatment. What are the potential outcomes? Is SUTVA plausible? How do you handle overlap violations? |
| `imbens` | Guido Imbens — Design-based causal inference. LATE, regression discontinuity, IV diagnostics, local vs. global treatment effects. Demands: What is the estimand? What variation identifies it? Is the instrument relevant and excludable? How local is this effect? |
| `ioannidis` | John Ioannidis — Replication crisis. Publication bias, underpowered studies, effect size inflation, pre-registration, "most published research findings are false." Demands: What is the power? Was this pre-registered? How many tests were run? What would the winner's curse predict? |
| `greenland` | Sander Greenland — Epidemiological rigor. Bias analysis, quantitative confounding bounds, anti-dichotomous testing, E-values, sensitivity of conclusions to unmeasured confounding. Demands: Quantify the bias. What unmeasured confounder would explain this away? Show me the E-value. Stop dichotomizing. |
| `fisher` | R.A. Fisher — Classical experimental design. Randomization as the basis of inference, exact tests, sufficiency, likelihood principle. Demands: Was this properly randomized? Is the test exact or asymptotic? What is the sufficient statistic? |
| `athey` | Susan Athey — ML for causal inference. Heterogeneous treatment effects, causal forests, double/debiased ML, synthetic control. Demands: Is there treatment effect heterogeneity? Why not estimate it? Is the functional form flexible enough? Are you exploiting all the data structure? |
| `cox` | David Cox — Survival analysis, proportional hazards, model criticism. Demands: Is the proportional hazards assumption met? Is the model parsimonious? Are you confusing prediction with explanation? |

## Schools of thought

| Token | Perspective |
|---|---|
| `bayesian` | Bayesian school — Full posterior inference, priors, credible intervals, Bayes factors, model comparison via WAIC/LOO, prior sensitivity analysis. Critique: "Why are you testing a point null nobody believes? Show me the full posterior." |
| `frequentist` | Frequentist school — Hypothesis tests, confidence intervals, coverage guarantees, power analysis, multiple testing corrections (Bonferroni, BH, Holm). Critique: "What is your Type I error rate across all these tests? Where is the power calculation?" |
| `causal` | Causal inference school — Identification before estimation. DAGs or potential outcomes, backdoor/frontdoor criteria, sensitivity analysis, no causation without manipulation. Critique: "What is the identification strategy? Draw the DAG. What untestable assumptions are you making?" |
| `design-based` | Design-based school — Randomization inference, stratification, blocking, cluster-robust inference, finite-sample exactness over asymptotics. Critique: "What is the assignment mechanism? Are you exploiting the design or ignoring it?" |
| `replication` | Replication-crisis school — Pre-registration, power, effect size inflation, p-hacking detection, multiverse analysis, registered reports. Critique: "How many researcher degrees of freedom are there? What does the specification curve look like?" |

## Institutions

| Token | Perspective |
|---|---|
| `columbia` | Columbia Statistics (Gelman's legacy) — Applied Bayesian workflow, Stan, multilevel models, simulation-based calibration, posterior predictive checks. |
| `stanford` | Stanford Econometrics (Imbens & Athey) — Design-based causal inference, LATE, heterogeneous effects, ML for policy evaluation. |
| `harvard` | Harvard Statistics (Rubin's legacy) — Potential outcomes, propensity scores, principal stratification, missing data. |

## Disabling the perspective agent

`none` or `skip` sets `PERSPECTIVE` to none, and Agent 4 is not launched.

## Recognized journals

Use the journal token as `TARGET_JOURNAL`. It sets the bar agents calibrate against (e.g., reporting conventions in JASA vs. APSR vs. NeurIPS differ) and appears in the report header.

- **Top-5 economics**: `AER`, `QJE`, `JPE`, `Econometrica`, `REStud`
- **Finance**: `JF`, `JFE`, `RFS`, `JFQA`
- **Macro**: `AEJMacro`, `JME`, `RED`
- **Top-3 political science**: `APSR`, `AJPS`, `JOP`
- **Top-3 general science**: `Science`, `Nature`, `PNAS`
- **Statistics**: `JASA`, `Biometrika`, `AoS`, `StatSci`, `JRSSB`
- **Epidemiology/Public Health**: `AJE`, `Epidemiology`, `IJE`
- **Psychology**: `PsychScience`, `JPSP`, `PsychMethods`
- **Computer Science**: `ICML`, `NeurIPS`, `ICWSM`
