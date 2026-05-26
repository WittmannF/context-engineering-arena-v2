# Getting Started — Task 002: Brazil Public Money Trail

This guide walks you through the baseline approach and key strategies for Task 002.

## Step 1: Set Up Your API Token

The Câmara dos Deputados API requires no token. The Portal da Transparência API requires a free token:

1. Go to https://portaldatransparencia.gov.br/api-de-dados/cadastrar-email
2. Register with your email address
3. The token arrives by email within minutes
4. Set it in your environment:
   ```bash
   export TRANSPARENCIA_API_TOKEN=your-token-here
   ```

You can run in sample mode without the token, but your submission will be limited to Câmara data only and will score poorly on the Data Joining dimension.

## Step 2: Choose a Policy Theme

The task works best with a specific, tractable theme. Good choices:

| Theme (PT) | Theme (EN) | Notes |
|---|---|---|
| `saude` | Health | Large budget, many propositions. Good starting point. |
| `farmacia-popular` | Farmácia Popular program | Specific enough to trace directly |
| `educacao` | Education | Large but well-documented |
| `assistencia-social` | Social assistance | SUAS system, BPC, Bolsa Família |
| `saneamento` | Sanitation | Infrastructure + health crossover |
| `vacina` | Vaccination | More tractable in post-2020 context |

Avoid very broad themes like `economia` or `segurança` — they are too diffuse to join across sources meaningfully.

## Step 3: Download and Prepare

```bash
# Sample mode (no token needed — Câmara only)
python tasks/task-002-brazil-public-money-trail/scripts/download.py \
    --theme saude \
    --year-start 2022 \
    --year-end 2024 \
    --sample-only

# Full mode with spending data
export TRANSPARENCIA_API_TOKEN=your-token
python tasks/task-002-brazil-public-money-trail/scripts/download.py \
    --theme saude \
    --year-start 2022 \
    --year-end 2024

# Prepare
python tasks/task-002-brazil-public-money-trail/scripts/prepare.py

# Create sample for testing
python tasks/task-002-brazil-public-money-trail/scripts/sample.py
```

## Step 4: Understand the Data

After running download + prepare, explore the processed files:

```python
import json

# Look at the first few propositions
with open("data/processed/task-002-brazil-public-money-trail/propositions.jsonl") as f:
    for i, line in enumerate(f):
        if i >= 3: break
        print(json.loads(line))

# Look at timeline events
with open("data/processed/task-002-brazil-public-money-trail/timeline_events.jsonl") as f:
    for i, line in enumerate(f):
        if i >= 5: break
        ev = json.loads(line)
        print(f"{ev['date']} [{ev['source_api']}] {ev['event']}")

# Look at candidate links
with open("data/processed/task-002-brazil-public-money-trail/candidate_links.jsonl") as f:
    for i, line in enumerate(f):
        if i >= 3: break
        link = json.loads(line)
        print(f"{link['id']}: {link['link_type']} (confidence {link['confidence']})")
        print(f"  {link['explanation'][:100]}...")
```

## Step 5: Understand the Link Classification System

This task requires you to classify every connection between legislative and spending data. The available types are:

| Link Type | When to Use | Confidence Range |
|---|---|---|
| `direct_documented_link` | You have a matching budget code, emenda ID, or explicit reference | 0.8–0.95 |
| `same_theme_link` | Same policy domain, no direct connection documented | 0.3–0.5 |
| `same_actor_link` | Same person appears in both datasets | 0.25–0.45 |
| `same_agency_link` | Same ministry/agency in both datasets | 0.3–0.5 |
| `same_time_window_link` | Temporal co-occurrence only | 0.15–0.35 |
| `weak_or_hypothetical_link` | Speculative or thin connection | 0.05–0.25 |

**Upgrade rules:**
- `same_theme_link` → `direct_documented_link` only if you can match a budget program code (Ação Orçamentária) between a proposition and a spending record
- `same_actor_link` → `direct_documented_link` only if the actor explicitly authorized a specific spending action (emenda parlamentar matched to budget execution)

**Never use `direct_documented_link` without a specific document or ID linking the two records.**

## Step 6: The Emenda Parlamentar Connection

The most direct legislative-to-spending link in Brazilian data is the **emenda parlamentar** — a parliamentary budget amendment that a deputy can insert into the annual budget for a specific purpose. These create a traceable path:

1. Deputy X proposes a bill on theme Y (Câmara API)
2. Deputy X also files emenda parlamentar E (Câmara API — `proposicoes?tipo=EMC`)
3. Emenda E is approved in the LOA
4. Portal da Transparência records spending under emenda E

If you can match emenda IDs across both datasets, you have a `direct_documented_link`. Without emenda matching, you can only claim `same_actor_link` or `same_theme_link`.

## Common Pitfalls

1. **Implying causation from co-occurrence.** A deputy who votes for a health bill and a ministry that has a large health budget does not make them causally connected. Label this `same_theme_link`.

2. **Forgetting the disclaimer.** Every submission must include a prominent disclaimer that the page organizes public data and does not allege wrongdoing. Missing this incurs a scoring penalty.

3. **Using only one data source.** A submission that only uses Câmara data scores 0 on Data Joining. You must join at least two sources.

4. **Institutional names in English.** Use official Portuguese names: "Câmara dos Deputados," "Ministério da Saúde," "Portal da Transparência." Not "Brazilian Chamber of Deputies," "Health Ministry."

5. **Treating synthetic data as real.** If you used the synthetic spending sample, every claim about spending figures must be labeled `is_synthetic: true` and the uncertainty section must note this.

6. **Wrong proposition number format.** Brazilian propositions have a specific format: `PL 1234/2023`, `PEC 45/2021`, `MP 1234/2023`. Check the actual API response — don't infer numbers.

## Useful Brazilian Government Data Resources

- Câmara API documentation: https://dadosabertos.camara.leg.br/swagger/api.html
- Portal da Transparência: https://portaldatransparencia.gov.br/
- TCU: https://portal.tcu.gov.br/
- Sistema Integrado de Planejamento e Orçamento (SIOP): https://www.siop.planejamento.gov.br/
- Brazilian budget system overview: https://www.gov.br/planejamento/pt-br/acesso-a-informacao/acoes-e-programas/orcamento-federal
- Lei de Responsabilidade Fiscal: https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp101.htm
