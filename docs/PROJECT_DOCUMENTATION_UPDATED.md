# AI-Powered Educational Content Platform — Technical Documentation

**Version:** 2.1 (Shorts-first planning + development guardrails)
**Philosophy:** Knowledge & pedagogy first. Use Shorts first to build attention, trust, and demand. Video is one output among many. Start 100% free/local, architect every layer so paid services can be swapped in later without touching business logic.


**Business Goal:** Build this as a side-job income system. The first target is not a huge SaaS platform; the first target is a reliable content engine that helps create high-retention educational Shorts, builds an audience, and later converts that audience into longer videos, notes, quizzes, courses, tutoring leads, sponsorships, or an app.

**Important Strategy:** Do not wait for full automation before publishing. Build the smallest pipeline that helps publish useful Shorts consistently, learn from analytics, and improve the system step by step.

---

## 0A. Shorts-First Business Strategy

The project should be developed in the following order of business priority:

1. **Audience first** — publish Shorts that create curiosity and make students want to watch more.
2. **Trust second** — make every explanation factually correct, simple, and age-appropriate.
3. **Repeatable production third** — use the platform to reduce script/storyboard/voice/subtitle work.
4. **Monetization fourth** — do not depend only on YouTube ads. Build multiple revenue options after the audience starts growing.
5. **Full automation last** — automation is useful only after the content style and audience response are proven.

### First monetization direction

Shorts can be used to popularize the channel, but the long-term earning system should include more than Shorts ad revenue:

| Stage | Goal | Possible Revenue Path |
|---|---|---|
| Early stage | Build attention and trust | Shorts, comments, community feedback |
| Growth stage | Move viewers to deeper content | Long videos, playlists, downloadable notes |
| Trust stage | Convert audience | Paid PDFs, quizzes, worksheets, mini-courses |
| Scale stage | Build repeatable products | App, exam-prep packs, school/teacher packages |
| Brand stage | External income | Sponsorships, affiliate tools/books, collaborations |

### Platform policy reminder

YouTube monetization rules, Shorts revenue rules, copyright rules, and AI-content disclosure expectations can change. Before relying on ad revenue, always verify the latest official YouTube Partner Program, Shorts monetization, and channel monetization policy pages.

Useful official references to re-check during development:
- YouTube Partner Program overview and eligibility: https://support.google.com/youtube/answer/72851
- YouTube Shorts monetization policies: https://support.google.com/youtube/answer/12504220
- YouTube channel monetization policies: https://support.google.com/youtube/answer/1311392
- What content can be monetized: https://support.google.com/youtube/answer/2490020

---

## 0B. Development Compass

When the project gets delayed or confusing, use this decision rule:

> **If a feature does not help publish better Shorts faster, improve factual trust, or collect useful analytics, postpone it.**

### Build now vs build later

| Build Now | Build Later |
|---|---|
| Concept input form | Full curriculum automation |
| Script generator | Model router |
| Storyboard generator | Experiment engine |
| Voice narration | Advanced animation engine |
| Subtitle generation | Full scene library |
| Manual review screen | Automated review sampling |
| Basic thumbnail/title suggestions | Thumbnail prediction engine |
| Basic analytics entry | Full content intelligence |
| Cost/time log | Advanced cost optimization |
| Reusable prompt files | Prompt performance ML system |

### MVP success definition

The MVP is successful when it can help produce and publish **20–30 good Shorts** with less manual effort than creating them from scratch.

Do not call the MVP successful just because the backend runs. The MVP is successful only when it helps create real content that gets reviewed, published, and measured.

---

## 0C. First Working Product Scope

The first version should support this flow:

```
Topic/Concept Input
      ↓
Shorts Script
      ↓
Storyboard Scenes
      ↓
Narration Audio
      ↓
Subtitles
      ↓
Simple Video Assembly or Export Package
      ↓
Human Review
      ↓
Publish Manually
      ↓
Record Analytics
```

### MVP input form

The first form should ask only:

```text
Board/Source       : NCERT / Self-written / Open educational source
Class/Level        : Class 6 / Class 7 / Beginner / Intermediate
Subject            : Science / Maths / English / etc.
Topic/Concept      : Why are leaves green?
Audience           : School students / exam learners / general curiosity
Language           : English first; Telugu/Hindi later
Duration           : 30s / 45s / 60s
Output Type        : Short / Notes / Quiz / Worksheet
Tone               : Curious / Simple / Exam-focused / Story-based
```

### MVP output package

For every concept, the system should generate:

```text
1. Hook
2. 30–60 second script
3. Scene-by-scene storyboard
4. Voice narration file
5. Subtitle file
6. Visual prompts or reused visual assets
7. Title options
8. Description
9. Hashtags
10. One quiz question
11. Human review status
```

This makes the tool useful even if full video assembly is delayed.

---

## 0D. Practical Content Strategy for Shorts

### Recommended first niche

Start narrow. Do not create videos on every subject immediately.

Best first niche options:

1. **Class 6–8 Science curiosity Shorts**
   - Easy to visualize
   - Many evergreen topics
   - Good for Shorts hooks
   - Can later become notes, worksheets, and long videos

2. **Math trick/explanation Shorts**
   - Strong exam value
   - Easy to repeat
   - Good for viewer retention

3. **English grammar Shorts**
   - High demand
   - Easy to create daily
   - Can later become paid practice worksheets

Recommended starting choice:

```text
NCERT / school-level Science curiosity Shorts
```

Why: science concepts are visual, interesting, and easier to convert into Shorts than long theory-heavy topics.

### First 100 Shorts plan

| Batch | Focus | Purpose |
|---|---|---|
| Shorts 1–20 | Curiosity topics | Test hooks and visual style |
| Shorts 21–40 | Common textbook doubts | Build student trust |
| Shorts 41–60 | Exam-friendly explanations | Test saves/shares |
| Shorts 61–80 | Myth vs fact / mistakes | Increase comments |
| Shorts 81–100 | Series-based content | Push viewers to playlists |

### Hook formulas to store as prompt templates

```text
1. "Did you ever wonder why...?"
2. "Most students think ___, but actually..."
3. "Here is the easiest way to understand..."
4. "This one idea explains the whole chapter..."
5. "If you understand this, ___ becomes easy."
6. "Your textbook says ___, but let me show what it means."
7. "Imagine ___ like this..."
```

### Shorts quality rules

Every Short should have:

```text
0–3 sec     Hook
3–10 sec    Setup / problem
10–40 sec   Explanation with visual
40–55 sec   Example or memory trick
55–60 sec   Challenge / next-video reason
```

Avoid:
- Long intros
- Too much theory
- Robotic narration
- Repetitive AI visuals
- Copyrighted textbook copying
- Same template every day
- Low-value “AI spam” videos

---

## 0E. Delay-Safe Development Rule

If development is delayed, do not stop publishing.

Use this fallback order:

| If this is delayed | Temporary fallback |
|---|---|
| Video assembly | Export script + storyboard + subtitles and assemble in CapCut manually |
| Image generation | Use reusable icon/diagram assets |
| TTS | Record your own voice or use one local TTS voice |
| Full curriculum ingestion | Manually enter 20–50 concepts |
| Knowledge graph | Store simple facts and examples only |
| Analytics API | Enter views/likes/retention manually once per week |
| SEO engine | Manually write title/description from templates |
| Automated QA | Use a checklist review screen |

Publishing consistently matters more than perfect automation in the first stage.

---

## 0. Core Architectural Principle

> **Separate Knowledge from Media.**

The system has two layers. The Knowledge Layer never knows what output format it feeds. The Media Layer never generates facts — it only renders what the Knowledge Layer hands it.

```
┌─────────────────────────────────────────────┐
│              KNOWLEDGE LAYER                 │
│  Books → Universal Knowledge Base            │
│  → Curriculum → Concepts                     │
│  → Concept Dependency Graph                  │
│  → Knowledge Graph (facts & relations)       │
│  → Learning Objectives (Bloom's Taxonomy)    │
│  → Audience Profile → Script                 │
└───────────────────┬───────────────────────────┘
                     │  (a Script + Concept is the contract
                     │   between the two layers)
┌───────────────────▼───────────────────────────┐
│               MEDIA LAYER                    │
│  Storyboard → Assets (image/scene library)   │
│  → Animation → Narration → Subtitles         │
│  → Video Assembly → Thumbnail → Publishing   │
└─────────────────────────────────────────────┘
```

Because of this split, the **same Knowledge Layer output** can later drive: YouTube Shorts, full lessons, revision notes, flashcards, quizzes, worksheets, classroom slides, or podcasts — without touching curriculum/fact/script logic at all. Only a new "renderer" needs to be added to the Media Layer.

---

## 1. Tech Stack (Free Now → Paid Later)

| Layer | Free/Local (Now) | Paid Upgrade (Later) | Swap Point |
|---|---|---|---|
| LLM (script, facts, QA, critic) | Ollama + Llama 3.1 8B / Mistral / Phi-3 / Qwen / Gemma | Claude API / GPT-4o | `services/llm_provider.py` |
| Text-to-Speech | Piper TTS / Coqui TTS (local) | ElevenLabs / PlayHT | `services/tts_provider.py` |
| Image/Illustration | Stable Diffusion (ComfyUI/A1111, local) | Midjourney API / DALL·E 3 | `services/image_provider.py` |
| Video assembly | FFmpeg + MoviePy | Remotion Cloud / Shotstack | `services/video_provider.py` |
| Knowledge graph | PostgreSQL (adjacency-list tables) | Neo4j AuraDB | `services/graph_provider.py` |
| Backend framework | FastAPI (Python) | same | — |
| Database | PostgreSQL (local Docker) | Managed Postgres (Supabase/RDS) | connection string only |
| Task queue | Celery + Redis (local Docker) | same, hosted Redis | broker URL only |
| File/media storage | Local filesystem | MinIO → AWS S3 | `services/storage_provider.py` |
| Vector search (asset/scene reuse, prompt search) | pgvector extension | Pinecone/Weaviate | `services/vector_provider.py` |
| Frontend/admin | Simple React (Vite) or FastAPI+Jinja | same, hosted | — |
| Monitoring/logs | Python logging + local files | Sentry / Grafana | — |
| SEO/trend data | Manual + YouTube Data API (free tier) | Paid keyword tools (TubeBuddy/VidIQ API) | `services/seo_provider.py` |

**Rule:** every external capability sits behind a one-method provider interface. Business logic never knows which concrete implementation answered the call.

---

## 2. Folder Structure

```
edu-content-platform/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   ├── security.py
│   │   └── policy.py                     # Governance/safety rules engine
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   ├── knowledge_base.py             # UniversalConcept, KnowledgeBaseEntry
│   │   ├── curriculum.py                 # Board, ClassGrade, Subject, Chapter, Concept
│   │   ├── concept_dependency.py         # ConceptDependency (prerequisite graph)
│   │   ├── source.py                     # SourceDocument, ExtractedContent
│   │   ├── knowledge_graph.py            # GraphNode, GraphEdge
│   │   ├── fact.py                       # Fact, FactVerificationLog
│   │   ├── learning_objective.py         # LearningObjective (Bloom's levels)
│   │   ├── audience.py                   # AudienceProfile
│   │   ├── prompt.py                     # PromptTemplate, PromptVersion, PromptPerformance
│   │   ├── model_route.py                # ModelRoute (task → model mapping)
│   │   ├── script.py                     # Script, ScriptVersion, ScriptVariant (experiments)
│   │   ├── critic.py                     # CriticReview
│   │   ├── fingerprint.py                # FingerprintTemplate
│   │   ├── storyboard.py                 # Storyboard, StoryboardScene
│   │   ├── asset_library.py              # AssetLibraryItem, SceneLibraryItem
│   │   ├── asset.py                      # VisualAsset, AudioAsset, AnimationAsset, SubtitleFile
│   │   ├── qa.py                         # QAReport, HumanReviewLog, EvaluationScore
│   │   ├── video_dna.py                  # VideoDNA
│   │   ├── thumbnail.py                  # ThumbnailVariant
│   │   ├── seo.py                        # SEOPackage
│   │   ├── publish.py                    # PublishPackage
│   │   ├── video.py                      # Video (master record)
│   │   ├── pipeline.py                   # PipelineJob, PipelineStageLog
│   │   ├── analytics.py                  # AnalyticsSnapshot, ContentIntelligence
│   │   ├── style_learning.py             # StyleEditLog
│   │   └── cost.py                       # CostLog
│   ├── schemas/                          # Pydantic mirrors of models/
│   ├── services/
│   │   ├── llm_provider.py
│   │   ├── tts_provider.py
│   │   ├── image_provider.py
│   │   ├── video_provider.py
│   │   ├── storage_provider.py
│   │   ├── vector_provider.py
│   │   ├── knowledge_base_service.py          # Stage -1
│   │   ├── curriculum_service.py              # Stage 0
│   │   ├── concept_dependency_service.py      # Stage 0.5
│   │   ├── extraction_service.py              # Stage 1
│   │   ├── knowledge_graph_service.py         # Stage 2
│   │   ├── fact_verification_service.py       # Stage 3
│   │   ├── learning_objective_service.py      # Bloom's taxonomy tagging
│   │   ├── audience_analyzer_service.py       # Stage 4
│   │   ├── prompt_management_service.py       # versioning + performance tracking
│   │   ├── model_router_service.py            # task → best model
│   │   ├── script_generator_service.py        # Stage 5
│   │   ├── experiment_service.py              # A/B script variants
│   │   ├── critic_service.py                  # AI Critic & rewrite loop
│   │   ├── originality_checker_service.py     # Stage 6
│   │   ├── fingerprint_service.py             # Stage 7
│   │   ├── storyboard_service.py              # Stage 8
│   │   ├── asset_library_service.py           # reuse-before-generate logic
│   │   ├── scene_library_service.py
│   │   ├── visual_generation_service.py       # Stage 9
│   │   ├── narration_service.py               # Stage 10
│   │   ├── animation_service.py                # Stage 11
│   │   ├── subtitle_service.py                 # Stage 12
│   │   ├── evaluation_service.py               # automated multi-metric scoring
│   │   ├── qa_service.py                       # Stage 13
│   │   ├── video_dna_service.py                # metadata extraction per video
│   │   ├── thumbnail_service.py                # generate + evaluate
│   │   ├── seo_service.py                      # titles/descriptions/keywords
│   │   ├── publishing_service.py               # Stage 15
│   │   ├── analytics_service.py                # Stage 16, backward-looking
│   │   ├── content_intelligence_service.py     # forward-looking trend/topic signals
│   │   ├── style_learning_service.py           # learns from human edits
│   │   ├── policy_service.py                   # governance/safety checks
│   │   ├── orchestrator_service.py             # pipeline state machine + checkpointing
│   │   └── cost_tracker_service.py
│   ├── routes/
│   │   ├── knowledge_base.py
│   │   ├── curriculum.py
│   │   ├── concepts.py
│   │   ├── concept_dependency.py
│   │   ├── knowledge_graph.py
│   │   ├── prompts.py
│   │   ├── scripts.py
│   │   ├── experiments.py
│   │   ├── storyboards.py
│   │   ├── assets.py
│   │   ├── videos.py
│   │   ├── thumbnails.py
│   │   ├── seo.py
│   │   ├── pipeline_jobs.py
│   │   ├── review.py
│   │   ├── publish.py
│   │   ├── analytics.py
│   │   └── style.py
│   ├── tasks/
│   │   ├── celery_app.py
│   │   ├── extraction_tasks.py
│   │   ├── script_tasks.py
│   │   ├── critic_tasks.py
│   │   ├── visual_tasks.py
│   │   ├── narration_tasks.py
│   │   ├── assembly_tasks.py
│   │   ├── thumbnail_tasks.py
│   │   ├── publish_tasks.py
│   │   └── analytics_tasks.py
│   └── utils/
│       ├── similarity.py
│       ├── prompt_templates/             # versioned .jinja files, tracked in DB too
│       └── validators.py
├── storage/
│   ├── raw_uploads/
│   ├── extracted/
│   ├── asset_library/                    # reusable images/icons, keyed by concept tags
│   ├── scene_library/                    # reusable animated scenes
│   ├── audio/
│   ├── thumbnails/
│   ├── video_drafts/
│   └── final/
├── alembic/
├── scripts/
├── tests/
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## 3. Database Schema (Models)

All tables get `id (uuid, PK)`, `created_at`, `updated_at` unless noted.

### 3.1 Universal Knowledge Base (Stage -1)
```
KnowledgeBaseEntry   id, universal_topic (e.g. "Photosynthesis"), summary,
                     core_facts (jsonb), source_type, confidence_score,
                     reused_by_concepts_count
```
Concepts across boards link to a `KnowledgeBaseEntry` and only store the *delta* (board-specific phrasing, depth, examples) rather than duplicating the whole concept.

### 3.2 Curriculum domain
```
Board            id, name, region
ClassGrade       id, board_id (FK), grade_number, label
Subject          id, class_grade_id (FK), name
Chapter          id, subject_id (FK), name, order_index
Concept          id, chapter_id (FK), knowledge_base_entry_id (FK, nullable),
                 title, status, difficulty_default
```

### 3.3 Concept Dependency Graph (Stage 0.5)
```
ConceptDependency   id, concept_id (FK), prerequisite_concept_id (FK),
                    strength (required/recommended)
```
Distinct from the Knowledge Graph — this models *pedagogical sequencing* ("can't teach Photosynthesis before Plant Cells"), not factual relationships.

### 3.4 Source & extraction
```
SourceDocument     id, board_id, class_grade_id, subject_id, chapter_id,
                   file_path, edition, publish_year, checksum, ingested_at
ExtractedContent   id, source_document_id (FK), concept_id (FK),
                   raw_text, key_facts (jsonb), keywords (jsonb),
                   examples (jsonb), extraction_model_used, confidence_score
```

### 3.5 Knowledge graph
```
GraphNode   id, concept_id (FK), label, node_type
GraphEdge   id, from_node_id (FK), to_node_id (FK), relation, weight
```

### 3.6 Facts & verification
```
Fact                 id, concept_id (FK), statement, source_type,
                     confidence_score, status
FactVerificationLog  id, fact_id (FK), method, verdict, reviewer, notes
```

### 3.7 Learning Objectives (Bloom's Taxonomy)
```
LearningObjective   id, concept_id (FK), bloom_level
                    (remember/understand/apply/analyze/evaluate/create),
                    objective_text, target_grade
```
The Script Generator prompt is built directly from the `bloom_level` — this is what most improves prompt quality, per your note.

### 3.8 Audience
```
AudienceProfile   id, concept_id (FK), target_grade, difficulty_level,
                  vocabulary_level, max_sentence_length, example_style,
                  language, duration_seconds
```

### 3.9 Prompt Management (first-class, not just files)
```
PromptTemplate     id, name, task_type (script/critic/fact_check/translation),
                   template_text, active (bool)
PromptVersion      id, prompt_template_id (FK), version_number, template_snapshot,
                   change_reason
PromptPerformance  id, prompt_version_id (FK), video_id (FK, nullable),
                   success_rate, avg_watch_time, failure_rate, sample_size
```

### 3.10 Model Router
```
ModelRoute   id, task_type (script/fact_check/translation/reasoning/critic),
             model_name, provider, priority_rank, active,
             avg_latency_ms, avg_cost, benchmark_score
```

### 3.11 Script (with experimentation)
```
Script          id, concept_id (FK), audience_profile_id (FK), learning_objective_id (FK),
                version, hook, explanation, example, challenge, ending,
                full_text, model_used, prompt_version_id (FK), status
ScriptVersion   id, script_id (FK), version_number, text_snapshot,
                similarity_score, rewrite_reason
ScriptVariant   id, script_id (FK), variant_label (A/B/C), hook_style,
                example_style, ending_style, evaluation_score, selected (bool)
```

### 3.12 AI Critic
```
CriticReview   id, script_id (FK), clarity_score, engagement_score,
               accuracy_flag, suggested_rewrite, model_used
```
Pipeline for text: `Writer AI → Critic AI → Rewrite AI → Human` — critic runs before originality check.

### 3.13 Brand / fingerprint
```
FingerprintTemplate   id, name, curiosity_question_style, analogy_style,
                      challenge_style, signature_ending_text,
                      visual_style_tag, narration_voice_id, active
```

### 3.14 Storyboard & reusable libraries
```
Storyboard          id, script_id (FK), fingerprint_template_id (FK)
StoryboardScene      id, storyboard_id (FK), order_index, script_segment,
                     visual_description, duration_seconds
AssetLibraryItem     id, tag (e.g. "sun","leaf","water_drop"), file_path,
                     asset_type, reuse_count, embedding (vector, nullable)
SceneLibraryItem     id, tag (e.g. "water_cycle_animation"), file_path,
                     reuse_count, embedding (vector, nullable)
```
`visual_generation_service` and `animation_service` **query the library first** (via tag or vector similarity) before calling the image/animation provider — generate only on a miss.

### 3.15 Assets
```
VisualAsset     id, scene_id (FK), asset_library_item_id (FK, nullable),
                asset_type, file_path, generation_prompt, model_used, status
AudioAsset      id, script_id (FK), file_path, voice_id, duration_seconds, tts_engine_used
AnimationAsset  id, scene_id (FK), scene_library_item_id (FK, nullable),
                file_path, animation_type, duration_seconds
SubtitleFile    id, video_id (FK), file_path, language, sync_status
```

### 3.16 QA, Evaluation & Review
```
EvaluationScore   id, video_id (FK), educational_accuracy, visual_quality,
                  narration_quality, engagement_score, age_appropriateness,
                  originality_score, retention_prediction, seo_score,
                  readability_score, production_quality, overall_pass (bool)
QAReport          id, video_id (FK), grammar_ok, pronunciation_ok, timing_ok,
                  factual_ok, subtitle_sync_ok, spelling_ok, image_quality_ok,
                  overall_status, notes
HumanReviewLog    id, video_id (FK), reviewer, hook_rating, accuracy_rating,
                  pacing_rating, clarity_rating, decision, improvement_made, comments
```

### 3.17 Video DNA
```
VideoDNA   id, video_id (FK), hook_type, analogy_used, humor_level,
           emotion_tag, visual_density, narration_speed, scene_count,
           animation_style
```
Purpose: later query "which DNA combination correlates with highest retention?" against `AnalyticsSnapshot`.

### 3.18 Thumbnail & SEO
```
ThumbnailVariant   id, video_id (FK), file_path, text_overlay,
                   predicted_ctr_score, selected (bool)
SEOPackage         id, video_id (FK), title_options (jsonb), description,
                   keywords (jsonb), hashtags (jsonb), search_intent,
                   competitor_keywords (jsonb), trending_variations (jsonb)
```

### 3.19 Publishing
```
PublishPackage    id, video_id (FK), seo_package_id (FK), thumbnail_variant_id (FK),
                  ai_disclosure_text, playlist_suggestion, published_at
```

### 3.20 Master video record & pipeline tracking (with checkpointing)
```
Video               id, concept_id (FK), script_id (FK), storyboard_id (FK),
                    current_stage (enum, includes all stages incl. -1 and 0.5),
                    overall_status (pending/in_progress/needs_review/failed/published),
                    last_successful_stage,          -- enables resume-from-failure
                    final_file_path, duration_seconds, language

PipelineJob         id, video_id (FK), stage_name, status
                    (queued/running/success/failed/retrying/needs_human),
                    attempt_count, max_attempts, checkpoint_data (jsonb),
                    started_at, finished_at, error_message

PipelineStageLog    id, pipeline_job_id (FK), stage_name, input_snapshot (jsonb),
                    output_snapshot (jsonb), duration_ms, cost_estimate
```
`checkpoint_data` + `last_successful_stage` mean a Stage 9 failure resumes **at Stage 9**, not from Stage 0.

### 3.21 Cost tracking
```
CostLog     id, video_id (FK), stage_name, provider, tokens_or_units,
            estimated_cost_usd, actual_cost_usd, created_at
```

### 3.22 Analytics & forward-looking intelligence
```
AnalyticsSnapshot      id, video_id (FK), platform, snapshot_date, views,
                       avg_watch_time_seconds, retention_pct, likes,
                       comments, shares, ctr_pct
ContentIntelligence    id, topic_or_concept_id (FK, nullable), signal_type
                       (topic_performance/best_length/best_hook/upload_time/
                       low_competition_topic), signal_value (jsonb),
                       computed_at
```

### 3.23 Personal Style Learning
```
StyleEditLog   id, script_id (FK), original_text, edited_text,
               editor, diff_summary, incorporated_into_prompt (bool)
```
After N edits, `style_learning_service` mines these diffs into a "house style" addendum injected into the script-generation prompt.

### 3.24 Governance
```
PolicyRule   id, rule_name, rule_type
             (no_medical_claims/no_political_opinion/no_stereotypes/
             no_unsafe_experiments/curriculum_only), description, active
PolicyViolationLog   id, video_id (FK), policy_rule_id (FK), stage_caught_at,
                     details, resolution
```
`policy_service` runs as a **cross-cutting check**, called by the Critic (Stage 5.5) and again by QA (Stage 13) — not a single stage, since content can drift at multiple points.


### 3.25 User Roles & Permissions

The MVP needs clear roles even if only one person uses the system at first.

```
UserAccount       id, name, email, password_hash, role, active
RolePermission    id, role_name, permission_key, allowed
```

Recommended roles:

| Role | Permissions |
|---|---|
| Super Admin | Manage everything |
| Content Admin | Add curriculum, concepts, sources |
| Script Reviewer | Review/edit scripts and facts |
| Video Editor | Review storyboard, visuals, subtitles |
| Publisher | Approve publishing package |
| Viewer/Student | Future app/website user |

Important: publishing should require at least one human approval until the pipeline is proven reliable.

### 3.26 Teacher Trust Score

Each generated output should have a simple trust score before it is approved.

```
TeacherTrustScore   id, video_id (FK), script_id (FK),
                    factual_accuracy_score,
                    age_appropriateness_score,
                    simplicity_score,
                    source_coverage_score,
                    originality_score,
                    reviewer_confidence_score,
                    overall_trust_score,
                    approval_required (bool),
                    notes
```

Suggested rule:

```text
overall_trust_score >= 85  → safe for normal review
70–84                    → needs careful human review
below 70                 → regenerate or rewrite
```

This score helps avoid publishing weak, confusing, or risky educational content.

### 3.27 Content Batch & Publishing Calendar

Since the business strategy is Shorts-first, batch planning should be stored.

```
ContentBatch       id, name, niche, target_audience, start_date, end_date,
                   planned_count, completed_count, published_count, notes

PublishingCalendar id, video_id (FK), planned_publish_date, actual_publish_date,
                   platform, status, playlist_name
```

Use this to plan 20–30 Shorts at a time instead of generating random one-off videos.

### 3.28 Manual Analytics Entry

Before API automation, analytics can be entered manually each week.

```
ManualAnalyticsEntry   id, video_id (FK), platform, entry_date,
                       views, likes, comments, shares,
                       avg_view_duration_seconds,
                       retention_pct, ctr_pct,
                       notes
```

This keeps learning possible even before YouTube API integration.

### 3.29 Legal & Source Safety Metadata

Every source-based concept should track enough information to avoid future confusion.

```
SourceSafetyLog    id, source_document_id (FK), concept_id (FK),
                   source_license_type,
                   page_or_section_reference,
                   copied_text_used (bool),
                   transformation_notes,
                   similarity_score,
                   legal_review_status,
                   reviewer_notes
```

Rule:

```text
Never publish content that is only a rewritten textbook paragraph.
Always convert the source into an original explanation, analogy, example, and visual teaching flow.
```


---

## 4. Services Layer

| Service | Stage | Responsibility |
|---|---|---|
| `knowledge_base_service` | -1 | Universal, board-agnostic concept knowledge; boards adapt from this instead of duplicating |
| `curriculum_service` | 0 | CRUD for Board/Class/Subject/Chapter/Concept |
| `concept_dependency_service` | 0.5 | Prerequisite graph between concepts |
| `extraction_service` | 1 | Parse source docs into facts/keywords/examples |
| `knowledge_graph_service` | 2 | Concept-internal factual relationships |
| `fact_verification_service` | 3 | Validate facts; flag for human review |
| `learning_objective_service` | 3.5 | Tag concept with Bloom's-taxonomy objectives |
| `audience_analyzer_service` | 4 | Produce AudienceProfile |
| `prompt_management_service` | — | Version prompts, track performance per version |
| `model_router_service` | — | Pick best model per task type |
| `script_generator_service` | 5 | Generate Script via routed LLM + versioned prompt |
| `experiment_service` | 5.4 | Generate A/B/C script variants, track which wins |
| `critic_service` | 5.5 | AI Critic reviews script before originality check |
| `originality_checker_service` | 6 | Similarity vs source; trigger rewrite loop |
| `fingerprint_service` | 7 | Inject brand elements |
| `storyboard_service` | 8 | Script → scenes |
| `asset_library_service` / `scene_library_service` | 8.5 | Reuse-before-generate lookup |
| `visual_generation_service` | 9 | Generate only on library miss |
| `narration_service` | 10 | TTS |
| `animation_service` | 11 | Motion, reuse scene library first |
| `subtitle_service` | 12 | Subtitle generation |
| `evaluation_service` | 12.5 | Multi-metric automated scoring |
| `qa_service` | 13 | Mechanical checks |
| `video_dna_service` | 13.5 | Extract DNA metadata for analytics correlation |
| `thumbnail_service` | 14.5 | Generate + evaluate multiple thumbnails |
| `seo_service` | 14.6 | Titles, descriptions, keywords, competitor/trend data |
| `publishing_service` | 15 | Assemble PublishPackage |
| `analytics_service` | 16 | Backward-looking performance sync |
| `content_intelligence_service` | 16.5 | Forward-looking: what to make next |
| `style_learning_service` | — | Learn house style from human edits |
| `policy_service` | — | Cross-cutting governance checks |
| `orchestrator_service` | — | State machine, checkpointing, resume-from-failure |
| `cost_tracker_service` | — | Cost logging + budget ceilings |

---

## 5. API Routes

```
# Knowledge Layer
POST   /knowledge-base/entries
GET    /knowledge-base/entries/{id}
POST   /curriculum/boards | /classes | /subjects | /chapters | /concepts
GET    /concepts/{id}
POST   /concepts/{id}/dependencies
GET    /concepts/{id}/dependencies
POST   /concepts/{id}/extract
GET    /concepts/{id}/knowledge-graph
POST   /concepts/{id}/verify-facts
POST   /concepts/{id}/learning-objectives

# Prompts & routing
GET/POST /prompts
GET      /prompts/{id}/performance
GET/POST /model-routes

# Scripts & experimentation
POST   /concepts/{id}/scripts
GET    /scripts/{id}
POST   /scripts/{id}/variants                # experiment engine
POST   /scripts/{id}/critic-review
POST   /scripts/{id}/check-originality
POST   /scripts/{id}/apply-fingerprint

# Media Layer
POST   /scripts/{id}/storyboard
GET    /assets/library?tag=
POST   /storyboards/{id}/generate-visuals
POST   /scripts/{id}/generate-narration
POST   /storyboards/{id}/animate
POST   /videos/{id}/generate-subtitles
POST   /videos/{id}/evaluate
POST   /videos/{id}/run-qa
POST   /videos/{id}/video-dna
POST   /videos/{id}/thumbnails
POST   /videos/{id}/seo-package

GET    /review/queue
POST   /review/{video_id}/decision

POST   /videos/{id}/publish-package
GET    /videos/{id}

GET    /pipeline/jobs
GET    /pipeline/jobs/{id}
POST   /pipeline/jobs/{id}/retry             # resumes from last_successful_stage

GET    /analytics/videos/{id}
POST   /analytics/sync
GET    /analytics/content-intelligence        # forward-looking recommendations

GET    /style/edits
```

---

## 6. Background Tasks (Celery)

```
tasks/
  extraction_tasks.py    → extract_content_task
  script_tasks.py        → generate_script_task, generate_variants_task
  critic_tasks.py        → critic_review_task, rewrite_task
                          → check_originality_task
  visual_tasks.py        → generate_visual_task (checks asset library first)
  narration_tasks.py     → generate_narration_task
  assembly_tasks.py      → animate_task, generate_subtitles_task,
                          evaluate_video_task, run_qa_task, extract_video_dna_task
  thumbnail_tasks.py     → generate_thumbnails_task, evaluate_thumbnails_task
  publish_tasks.py       → build_seo_package_task, build_publish_package_task
  analytics_tasks.py     → sync_analytics_task, compute_content_intelligence_task
```

**Checkpointing rule:** every task writes `PipelineJob.checkpoint_data` on success and updates `Video.last_successful_stage`. `orchestrator_service.retry(video_id)` always resumes from that stage, never from Stage 0.

---

## 7. Pipeline State Machine (Full)

```
Stage -1   Universal Knowledge Base       (KNOWLEDGE LAYER)
Stage 0    Curriculum Manager
Stage 0.5  Concept Dependency Graph
Stage 1    Content Extraction
Stage 2    Knowledge Graph
Stage 3    Fact Verification
Stage 3.5  Learning Objectives (Bloom's)
Stage 4    Audience Analyzer
Stage 5    Script Generator (via Prompt Mgmt + Model Router)
Stage 5.4  Experiment Engine (A/B/C variants)                 [optional, gated by config]
Stage 5.5  AI Critic → Rewrite loop
Stage 6    Originality Checker
Stage 7    Fingerprint Engine
                                          ── layer boundary ──
Stage 8    Storyboard Generator            (MEDIA LAYER)
Stage 8.5  Asset/Scene Library lookup
Stage 9    Visual Generation (on library miss only)
Stage 10   Narration
Stage 11   Animation
Stage 12   Subtitle Generator
Stage 12.5 Automated Evaluation (multi-metric scoring)
Stage 13   Automated QA
Stage 13.5 Video DNA extraction
Stage 14   Human Review
Stage 14.5 Thumbnail Generator + Evaluator
Stage 14.6 SEO Engine
Stage 15   Publishing Package
Stage 16   Analytics (backward-looking)
Stage 16.5 Content Intelligence (forward-looking, feeds Stage 0/5 topic & prompt choices)
```

Cross-cutting (run at multiple points, not a single stage):
- **Policy/Governance checks** — at Critic (5.5) and QA (13)
- **Cost tracking** — every stage
- **Style Learning** — captured whenever a human edits a Script or ScriptVersion

---

## 8. Cost & Budget Guardrails

- Per-video cost ceiling in config (₹0 while fully local)
- Retry loops (originality rewrite, critic rewrite) capped at N attempts, then `needs_human` — never infinite
- Cost logged even for local/free tools (GPU-seconds, token counts) to build a real baseline before any paid migration

---

## 9. Build Order — Revenue-First, MVP-First

The project should be built in a way that supports the side-job goal: create good Shorts, publish consistently, collect feedback, and improve.

Do not build the full 16-stage architecture before posting the first videos.

---

### Phase 0 — Planning & Channel Foundation

Goal: decide the first niche and avoid random content generation.

- [ ] Choose first niche: recommended `Class 6–8 Science curiosity Shorts`
- [ ] Choose first language: recommended `English first`
- [ ] Define target audience: school students + curious learners
- [ ] Define brand/fingerprint:
  - Hook style
  - Visual style
  - Voice style
  - Ending style
  - Thumbnail style
- [ ] Prepare first 100 concept ideas
- [ ] Prepare 10 reusable hook templates
- [ ] Prepare 5 script styles:
  - Curiosity
  - Mistake correction
  - Exam-focused
  - Story/analogy
  - Quick revision
- [ ] Prepare manual publishing checklist
- [ ] Verify latest platform monetization, copyright, and AI disclosure policies

Exit condition:

```text
You have a clear niche, first 100 topics, and a repeatable Short format.
```

---

### Phase 1 — Creator Assistant MVP

Goal: build a tool that helps create Shorts faster, even if video assembly is still manual.

Build only:

- [ ] Repo setup
- [ ] Basic FastAPI backend
- [ ] Simple React/admin UI or FastAPI templates
- [ ] Concept input form
- [ ] Script generator using one local/free LLM or manual prompt workflow
- [ ] Storyboard generator
- [ ] Title/description/hashtag generator
- [ ] Quiz question generator
- [ ] Human review/edit screen
- [ ] Export package:
  - script `.txt`
  - storyboard `.md`
  - subtitles `.srt`
  - visual prompts `.md`
  - title/description `.md`

Skip for now:

- Full Celery orchestration
- Full knowledge graph
- Model router
- Experiment engine
- Automated SEO engine
- Thumbnail prediction
- Advanced analytics

Exit condition:

```text
The system can generate a useful content package for 20–30 Shorts.
```

---

### Phase 2 — Shorts Production MVP

Goal: produce real Shorts consistently.

- [ ] Add TTS using Piper/Coqui or one reliable voice
- [ ] Generate `.srt` subtitles
- [ ] Add simple FFmpeg/MoviePy assembly OR export to CapCut workflow
- [ ] Add reusable visual asset folder
- [ ] Add basic content batch tracking
- [ ] Add publishing calendar
- [ ] Add manual analytics entry
- [ ] Publish 20–30 Shorts
- [ ] Record performance weekly:
  - views
  - likes
  - comments
  - shares
  - retention
  - saves if available
  - subscriber growth

Exit condition:

```text
You have published 20–30 Shorts and know which hook/topic/style performs better.
```

---

### Phase 3 — Quality & Trust Layer

Goal: reduce wrong, boring, or low-quality output.

- [ ] Add fact checklist
- [ ] Add source tracking
- [ ] Add originality/similarity checker
- [ ] Add Teacher Trust Score
- [ ] Add AI critic for script clarity
- [ ] Add reviewer decision:
  - approve
  - edit required
  - regenerate
  - reject
- [ ] Add source safety log
- [ ] Add policy/governance checks for:
  - unsafe experiments
  - medical claims
  - political opinion
  - stereotypes
  - copied textbook content

Exit condition:

```text
Every published video has a source record, review status, and trust score.
```

---

### Phase 4 — Automation of the Core Loop

Goal: reduce repeated manual work after the content style is proven.

- [ ] Add Celery + Redis
- [ ] Add PipelineJob and checkpointing
- [ ] Automate narration
- [ ] Automate subtitles
- [ ] Automate basic video assembly
- [ ] Add retry rules
- [ ] Add failed-stage resume
- [ ] Add asset reuse before generating new images
- [ ] Add cost/time tracking per video

Exit condition:

```text
A failed generation can resume from the failed stage, and one Short package can be generated with minimal manual work.
```

---

### Phase 5 — Scale Systems

Goal: build the advanced platform only after real content proves demand.

- [ ] Universal Knowledge Base
- [ ] Concept Dependency Graph
- [ ] Knowledge Graph
- [ ] Bloom's Taxonomy learning objectives
- [ ] Prompt versioning
- [ ] Model Router
- [ ] Scene Library
- [ ] Thumbnail engine
- [ ] SEO engine
- [ ] Video DNA
- [ ] Content Intelligence
- [ ] Style Learning
- [ ] A/B script experiment engine

Exit condition:

```text
You are publishing consistently and have enough analytics to justify optimization systems.
```

---

### Development Priority Rule

When choosing what to build next, ask:

```text
Will this help me publish better Shorts faster?
Will this reduce factual/content risk?
Will this help me understand what the audience wants?
Will this save repeated manual time?
```

If the answer is no, postpone it.

---

### What Not to Build Too Early

Avoid building these before publishing real videos:

- Multi-model routing
- Full A/B testing
- Automated trend prediction
- Complex knowledge graph
- Paid API integrations
- Advanced admin permissions
- Full SaaS billing
- Multi-board support
- Multi-language pipeline
- Perfect animation automation

These are useful later, but they can delay the first earning path.


---

## 10. Appendix A — Original Project Vision (for reference)

**The end goal, as originally framed:** a system where you type a simple spec —

```
Board      : NCERT
Class      : 7
Subject    : Science
Chapter    : Photosynthesis
Concept    : Why are leaves green?
Language   : English
Duration   : 35 sec
```

— click **Generate**, and 2–3 minutes later get a complete package: script, storyboard, voice, illustrations, animations, music, subtitles, thumbnail, title suggestions, description, tags, and a quiz question. Your job becomes review-and-publish, not creation.

**The core reframe:** this is not "YouTube automation." It's an **AI-powered educational content platform** where video is just one output. The same knowledge engine could later produce classroom presentations, revision notes, flashcards, quizzes, worksheets, podcasts, or interactive lessons — which is exactly why Section 0 (Knowledge Layer vs. Media Layer) exists in this document.

---

## 11. Appendix B — Full Question List From Original Discussion

These were posed as design decisions to answer before/while building. Not all have firm answers yet — see Section 13 for the ones still open.

**Content & Learning**
- Which boards will you support first? Which grades, subjects?
- How many concepts per chapter?
- How will you decide whether a concept deserves one Short or several?
- How will you explain abstract ideas visually?
- How will you handle topics that require experiments?

**AI**
- Which local LLM performs best for educational rewriting?
- One model for everything, or specialized models per task? *(→ addressed by Model Router, Section 3.10)*
- How will you measure factual accuracy? Detect hallucinations? *(→ Fact Verification, Section 3.6)*
- How will you ensure scripts stay age-appropriate? *(→ Audience Analyzer + Policy Engine)*
- How will you generate multiple languages while preserving meaning?

**Video Generation**
- What animation style becomes your signature? *(→ Fingerprint Template, Section 3.13)*
- How much variation should there be between videos?
- How will you avoid repetitive pacing?
- Will every video have background music?
- How will you maintain a consistent visual identity? *(→ Asset/Scene Library + Fingerprint)*

**Quality**
- What similarity threshold is acceptable vs. source text? *(still open, Section 13)*
- How will you detect factual errors automatically? *(→ Fact Verification + QA)*
- What happens if image generation fails? What if narration is too long for target duration? *(→ checkpointing/retry, Section 7)*
- How will you test the pipeline before publishing?

**Legal & Compliance**
- How will you ensure scripts are original? *(→ Originality Checker)*
- How will you document your content sources? *(→ SourceDocument versioning, Section 3.4)*
- How will you disclose AI-generated/altered content where required? *(→ ai_disclosure_text, Section 3.19)*
- How will you respond if a textbook edition changes? *(still open, Section 13)*

**Scaling**
- How will you regenerate videos after curriculum updates?
- How will you organize thousands of generated assets? *(→ Asset/Scene Library)*
- How will you support multiple languages efficiently?
- Can one pipeline produce both Shorts and longer videos from the same concept? *(→ Knowledge/Media layer split makes this possible)*
- How will you reuse visuals across related concepts without feeling repetitive?

**Business**
- What defines success in the first six months?
- Are you optimizing for subscribers, watch time, or educational impact?
- When will you introduce PDFs, courses, or an app?
- What will make your channel different from hundreds of other educational channels?
- If someone copies your workflow, what is your lasting competitive advantage?

*None of the Business-category questions have firm answers yet in our discussion — worth deciding before or during Phase 1, since they'll shape what "success" means when you look at your first batch of analytics.*

---

## 12. Appendix C — Engineering Review Notes (from earlier critique pass)

These were raised as gaps before the Knowledge/Media-layer rewrite, and are folded into the architecture above — listed here so the reasoning isn't lost:

1. **Orchestration/failure handling** — no stage should fail silently; every task retries with a cap, then flags `needs_human` rather than looping or dropping the video. *(→ Section 6–7, PipelineJob/checkpointing)*
2. **Cost model** — every AI call costs money/time even locally (GPU-seconds); a cost ceiling per video prevents silent runaway loops (e.g. repeated rewrite cycles). *(→ Section 8, CostLog)*
3. **Curriculum/textbook versioning** — every generated video should trace back to a specific textbook edition/date so syllabus changes don't silently orphan content. *(→ Section 3.4, still needs a defined re-generation policy — open question)*
4. **Fact feedback loop** — a wrong fact caught once should correct the shared Knowledge Base/Graph, not just that one script. *(→ Section 3.1/3.5 — KnowledgeBaseEntry is the single source of truth)*
5. **Human review at scale** — reviewing every video works at 1/day, not at 20/day; needs either a sampling strategy or an AI pre-filter that only escalates likely-problem videos. *(still open — decide the sampling rule in Phase 2)*
6. **Legal risk on textbook basis** — bigger question than disclosure/originality: is deriving content from NCERT/board textbooks actually within fair use in your jurisdiction, even reworded? Worth a real legal opinion before scaling, not just a documentation checklist. *(still open — flagged as highest-severity open item)*
7. **MVP sequencing** — build a manual-passthrough version first (Phase 1) and gather real analytics before automating the upstream stages, rather than finishing all 16+ stages before shipping video #1. *(→ Section 9, Phase 1)*

---

## 13. Open Design Questions Still Worth Revisiting
- Similarity threshold value for originality checker
- Which board/class/subject to launch with
- Sampling strategy for human review once volume increases
- Legal review of textbook-derived content basis, per board/jurisdiction
- Versioning strategy when a textbook edition changes mid-catalog
- At what video volume does the Asset/Scene Library start paying for itself vs. added complexity
- When to introduce the Experiment Engine (it adds real generation cost — only worth it once base pipeline is stable)

---

## 14. Critical Fixes to Remember During Development

### 14.1 Scope Control Fix

Problem:
The full architecture is too large to build at once.

Fix:
Build a vertical slice first.

```text
Concept → Script → Storyboard → Voice → Subtitles → Review → Publish Package
```

Everything else is future enhancement until the first 20–30 Shorts are published.

---

### 14.2 Legal/Copyright Fix

Problem:
Textbook-derived content may create copyright or licensing risk.

Fix:
Track sources and transform the teaching explanation.

Rules:

```text
1. Do not copy textbook wording.
2. Store source name, edition, year, chapter, and page/section.
3. Generate original explanation, analogy, example, and visual flow.
4. Run similarity check.
5. Require human approval before publishing.
6. Prefer open educational resources or self-written explanations for MVP.
```

---

### 14.3 Human Review Scaling Fix

Problem:
Reviewing every video manually works in the beginning but may not scale.

Fix:
Use risk-based review.

| Risk Level | Condition | Action |
|---|---|---|
| High | Low trust score, sensitive topic, poor source confidence | Mandatory human review |
| Medium | Normal topic but AI made many changes | Human spot check |
| Low | High trust score, simple topic, approved template | Fast review |

During MVP, review every video manually. Later, review based on risk.

---

### 14.4 Fact Feedback Loop Fix

Problem:
If one wrong fact is corrected only in one script, the same mistake may repeat.

Fix:
When a fact is corrected, update the shared KnowledgeBaseEntry or Fact table.

Rule:

```text
Wrong fact found → update source fact → regenerate affected script/storyboard → log correction
```

---

### 14.5 Delay Fix

Problem:
Development delays can stop publishing.

Fix:
Always keep a manual fallback workflow.

Minimum fallback workflow:

```text
AI/script prompt → manual edit → CapCut/Canva assembly → publish → manual analytics entry
```

The platform should improve the workflow, not block it.

---

### 14.6 Repetitive Content Fix

Problem:
Mass-produced, repetitive AI Shorts can reduce trust and may create monetization risk.

Fix:
Each video must include at least one original element:

```text
1. Unique analogy
2. Unique example
3. Unique visual explanation
4. Unique student mistake correction
5. Unique quiz/challenge
6. Human-edited hook or ending
```

Do not publish hundreds of nearly identical AI-generated videos.

---

### 14.7 Quality Fix

Problem:
Generated content may be technically correct but boring.

Fix:
Track both educational quality and viewer interest.

Quality checklist:

```text
- Is the first 3 seconds interesting?
- Can a Class 6–8 student understand it?
- Is there one clear learning point?
- Is the visual connected to the explanation?
- Is the ending giving a reason to watch another video?
- Is the language simple?
- Is the script under the target duration?
```

---

## 15. Revenue-First Product Roadmap

### Stage 1: Attention

Goal:
Use Shorts to get reach and identify what topics people like.

Build:
- Script generator
- Storyboard generator
- Title/hashtag generator
- Manual publishing workflow

Measure:
- Views
- Retention
- Shares
- Comments
- Subscriber growth

---

### Stage 2: Trust

Goal:
Make students believe the channel explains better than normal textbook reading.

Build:
- Fact review
- Teacher Trust Score
- Quiz generator
- Notes generator
- Playlist structure

Measure:
- Returning viewers
- Saves
- Comments asking doubts
- Long-video clicks

---

### Stage 3: Conversion

Goal:
Move viewers from Shorts to deeper learning products.

Build:
- Long-video script generator
- Downloadable notes
- Practice worksheets
- Mini-course landing page
- Email/Telegram/WhatsApp community capture, if appropriate

Possible products:
- Chapter notes PDF
- Quiz packs
- Revision worksheets
- Exam preparation mini-course
- Doubt-solving community
- School/teacher content package

---

### Stage 4: Scale

Goal:
Turn the project into a repeatable content business.

Build:
- Batch generation
- Automated subtitles
- Asset library
- Analytics-based topic selection
- Multi-language support
- App or website

---

## 16. Weekly Development Routine

Use this routine to avoid getting stuck in planning.

### Every week

```text
1. Build or improve one small feature.
2. Produce at least 3–5 Shorts.
3. Publish or schedule the Shorts.
4. Record analytics.
5. Note what worked.
6. Improve prompts/templates based on real results.
```

### Weekly review questions

```text
Which Short got the highest retention?
Which hook worked best?
Which topic got comments?
Which visual style looked clear?
Which part took too much manual time?
Which feature should be built next to reduce that manual work?
```

---

## 17. Final MVP Checklist

The first serious version is ready when:

```text
[ ] I can enter a concept.
[ ] I can generate a Short script.
[ ] I can generate storyboard scenes.
[ ] I can generate narration or export script for recording.
[ ] I can generate subtitles.
[ ] I can review/edit the output.
[ ] I can export a publish package.
[ ] I can store title/description/hashtags.
[ ] I can record basic analytics after publishing.
[ ] I have published 20–30 Shorts using the system.
[ ] I know which topics and hooks perform better.
```

Only after this checklist is complete should Phase 3–5 advanced automation become the focus.

---

## 18. Practical Build Reminder

This project is not only an AI system. It is a content business engine.

The right development order is:

```text
Audience proof → Content quality → Repeatable workflow → Automation → Monetization expansion → SaaS/platform scale
```

Do not reverse this order.


---

*This is a living spec. Update model/service/route lists here as the actual codebase evolves — don't let docs and code drift apart. Phase 3–4 items are the "production-grade SaaS" layer; resist building them before Phase 1–2 have shipped real videos and real analytics, since several of these (Model Router, Experiment Engine, Content Intelligence) are only useful once you have data to act on.*
