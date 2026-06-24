# MCIP — Marketing & Communications Intelligence Platform

## What this is

MCIP is a domain extension of the Signal Intelligence Platform (SIP) architecture,
scoped specifically to Anthropic MBC talent. It runs inside Research_First_Sourcer_Automation
as a self-contained subdirectory, sharing the SIP/TIP backend without modifying it.

The platform maps influence, not popularity. Every scoring decision is evidence-based.
Followers, engagement, and virality are explicitly excluded as signals.

---

## Architecture

MCIP mirrors the SIP seed hub pattern:

    Seed Hub (688 seeds, 27 categories)
        -> Loader (mcip_seed_hub_loader.py)
        -> Classifier (mcip_role_classifier.py)
        -> Scorer (mcip_scoring.py)
        -> Hook Generator (mcip_scoring.py)
        -> Pipeline (mcip_pipeline.py)
        -> Output (mcip/outputs/mcip_run_output.json)

Source of truth: data/MCIP.xlsx
Runtime entry point: python3 -m mcip.mcip_pipeline

---

## Files

    mcip_config.json          Domain config. Workbook paths, scoring governance, source weights.
    mcip_seed_hub_loader.py   Loads MCIP_Seed_Hub_min.json. Filters by category, priority, surface type.
    mcip_crawler_registry.py  Maps 10 MBC crawler wrappers to existing SIP backend crawlers.
    mcip_role_classifier.py   Maps job titles to MBC role families and Anthropic target roles.
    mcip_scoring.py           Authority scoring engine + outreach hook generator.
    mcip_pipeline.py          Orchestrates the full stack. Entry point for all MCIP runs.
    MCIP_Seed_Hub_min.json    688 seed URLs exported from MASTER_COMMS_SEED_HUBS worksheet.

---

## Seed Hub — 688 seeds across 27 categories

    Company Surface          187    Anthropic, OpenAI, Mistral, Google DeepMind newsrooms and team pages
    Hidden Authority          61    Non-public authority surfaces: EU AI Office, UK AISI, think tanks
    Hidden Authority Surface  36    Secondary hidden authority: fellowship pages, standards bodies
    Conference Ecosystem      59    SXSW, Cannes Lions, Web Summit, Content Marketing World rosters
    Podcast Ecosystem         35    Lex Fridman, Hard Fork, Decoder, TBPN, All-In guest archives
    Design Credit Database    34    Brand New, Motionographer, Awwwards named designer credits
    Agency Ecosystem          31    Wieden+Kennedy, AKQA, Huge, R/GA client roster pages
    Community Surface         25    Luma event organizers, Slack community admins, Discord mods
    VC Ecosystem              23    Bessemer, Lightspeed, CapitalG, Spark platform team pages
    Award Ecosystem           22    Cannes Lions jury, D&AD judges, Clio Awards named recipients
    + 17 additional categories

Priority distribution:
    1 -- CRITICAL    102 seeds
    2 -- HIGH        230 seeds
    3 -- MEDIUM      356 seeds

---

## Scoring governance (standing rules — never override)

Forbidden signals: followers, likes, views, engagement, virality.

    Authority Score  = Trust_Signals x Source_Weight x Recurrence
    Influence Score  = Breadth x Recurrence x Authority
    Invisible Titan  = Authority + Influence - Public_Visibility

Source quality tiers:
    10   Congressional testimony, EU AI Act authorship, Tier 1 conference organizer
     9   Think tank author, major publication byline, hidden authority surface
     8   Major podcast guest, award judge, VC platform partner, arXiv acknowledgment
     7   Conference speaker, press wire named contact, newsletter author
     6   Community leader, agency portfolio named, event organizer
     3   Social platform (reference only)
     0   Followers, engagement (hard zero — governance rule)

Score columns in workbook: integers 1-10. No text. No floats.
Priority values: "Tier 1" / "Tier 2" / "Tier 3" only.
Contact confidence: "CONFIRMED" / "HIGH" / "MEDIUM" / "LOW" only.

---

## Five influence classes

    Creator      Produces original content with a named byline (newsletters, podcasts, articles)
    Amplifier    Distributes content at scale to a defined audience
    Validator    Lends credibility through institutional endorsement (jury, judge, fellow)
    Translator   Bridges technical AI concepts for non-technical audiences
    Architect    Shapes the structural conditions for AI communication (policy, standards, governance)

---

## Creative sourcing surfaces (non-LinkedIn)

These are MCIP equivalents of SIP invisible titan surfaces:

    Press wire footer credits      -> named PR contacts before LinkedIn
    Design credit databases        -> Brand New, Motionographer, Awwwards
    Conference roster pages        -> speaker bios with employer + title
    Podcast guest archives         -> episode descriptions with named guests
    VC platform team pages         -> Bessemer Fellows, Lightspeed Operators
    EU AI Office staff pages       -> Brussels policy comms talent
    UK AISI team pages             -> London AI safety comms talent
    connpass event organizers      -> Japan Claude community builders
    ArXiv acknowledgment sections  -> Anthropic non-research staff named in papers
    Agency client roster pages     -> named account leads on AI client work

599 of 801 leads (74.8%) were sourced before LinkedIn was consulted.

---

## Running the pipeline

    # Score all critical seeds
    python3 -m mcip.mcip_pipeline --priority 1

    # Score all seeds
    python3 -m mcip.mcip_pipeline

    # Score first 50 high-priority seeds
    python3 -m mcip.mcip_pipeline --priority 2 --limit 50

Output: mcip/outputs/mcip_run_output.json

---

## Workbook

    File:           data/MCIP.xlsx
    Version:        v19
    Seed sheet:     MASTER_COMMS_SEED_HUBS (688 rows, 48 columns)
    Leads sheet:    COMMS_TALENT_LEADS (801 rows, 23 columns)
    Header row:     2
    Data start:     3

Lead counts:
    Total leads          801
    Non-LinkedIn leads   599   (74.8%)
    Tier 1               425
    Tier 2               301
    Tier 3                53
    CONFIRMED              35
    HIGH                  565
    MEDIUM                185
    LOW                    13

---

## Cardinal distinction (mirrors SIP architecture)

Discovery seeds (company newsrooms, GitHub orgs, conference pages):
    -> NULL authority metadata is correct
    -> These find the surface, not the person

Authority seeds (EU AI Office, UK AISI, arXiv, connpass, Brand New):
    -> Must have: authority_strength, anthropic_relevance, candidate_yield_potential
    -> These produce named humans with verifiable credentials

This distinction governs which seeds feed the scoring pipeline
and which are discovery-only surfaces.

---

## Co-inventors

Dave Mendoza, Talent Engine.io — platform architecture, seed hub design, scoring governance
Chris Galy — co-inventor, Signal Intelligence Platform (SIP) and Talent Intelligence Platform (TIP)

Patent-pending: Constraint-Based Evidence Validation System
Patent-pending: Multi-Entity Simulation and Talent Optimization System

MCIP is a domain application of the SIP architecture, not a separate patent filing.
