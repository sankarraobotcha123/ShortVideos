import { useEffect, useMemo, useState } from 'react'
import {
  addAnalytics,
  audioDownloadUrl,
  assemblyDownloadUrl,
  assignPackageBatch,
  createBatch,
  createCalendarEntry,
  deleteCalendarEntry,
  deleteVisualAsset,
  exportUrl,
  fetchAiSettings,
  fetchAnalyticsInsights,
  fetchAudioSettings,
  fetchBatch,
  fetchBatches,
  fetchCalendar,
  fetchPackage,
  fetchPackages,
  fetchProviderLogs,
  fetchVisualAssets,
  generateAssembly,
  generateAudio,
  generateContent,
  generateSourceSafetyReview,
  generateThumbnailGuide,
  generateTrustReview,
  generateLearningOutput,
  generateVideoDraft,
  thumbnailGuideDownloadUrl,
  sourceSafetyDownloadUrl,
  trustReviewDownloadUrl,
  learningOutputDownloadUrl,
  createPromptTemplate,
  deletePromptTemplate,
  fetchPromptTemplates,
  previewPromptTemplate,
  seedPromptTemplates,
  updatePromptTemplate,
  updateBatch,
  uploadVisualAsset,
  updateCalendarEntry,
  updateReview,
  updateTrustReview,
  videoDraftDownloadUrl,
  visualAssetUrl
} from './api.js'

const initialForm = {
  board_source: 'NCERT / Self-written',
  class_level: 'Class 7',
  subject: 'Science',
  topic: 'Why are leaves green?',
  audience: 'School students',
  language: 'English',
  duration_seconds: 60,
  output_type: 'Short',
  tone: 'Curious',
  batch_id: '',
  prompt_template_id: '',
  source_name: 'Self-written concept notes',
  source_license_type: 'Self-written / Original',
  page_or_section_reference: '',
  copied_text_used: false,
  source_notes:
    'Leaves contain chlorophyll. Chlorophyll absorbs sunlight and helps plants make food through photosynthesis. Chlorophyll reflects green light, so leaves look green.',
  transformation_notes:
    'Converted source facts into a simple original explanation with analogy, visual scenes, and a student challenge.'
}

const initialBatch = {
  name: 'First 20 Science Curiosity Shorts',
  niche: 'Class 6-8 Science curiosity Shorts',
  target_audience: 'School students and curious learners',
  start_date: today(),
  end_date: '',
  planned_count: 20,
  status: 'planning',
  notes: 'Test hooks, visual style, retention, and comments before automating more.'
}

const initialCalendar = {
  package_id: '',
  planned_publish_date: today(),
  actual_publish_date: '',
  platform: 'YouTube Shorts',
  status: 'planned',
  playlist_name: 'Science Curiosity Shorts',
  notes: ''
}

const initialVisualAsset = {
  title: 'Leaf chlorophyll diagram',
  tags: 'leaf, chlorophyll, photosynthesis, science',
  description: 'Simple reusable visual for explaining why leaves look green.',
  source_type: 'self_created',
  license_type: 'Self-created / Original',
  notes: 'Use for Class 6-8 science Shorts about plants.'
}

function today() {
  return new Date().toISOString().slice(0, 10)
}

function useHashRoute() {
  const [hash, setHash] = useState(window.location.hash || '#/')
  useEffect(() => {
    const onChange = () => setHash(window.location.hash || '#/')
    window.addEventListener('hashchange', onChange)
    return () => window.removeEventListener('hashchange', onChange)
  }, [])
  return hash
}

function navigate(hash) {
  window.location.hash = hash
}

function App() {
  const hash = useHashRoute()
  const route = useMemo(() => parseRoute(hash), [hash])

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-block">
          <div className="brand-mark">Edu</div>
          <div>
            <h1>Shorts Creator</h1>
            <p>React frontend + FastAPI backend</p>
          </div>
        </div>
        <nav>
          <a className={route.name === 'dashboard' ? 'active' : ''} href="#/">Dashboard</a>
          <a className={route.name === 'new' ? 'active' : ''} href="#/new">Create package</a>
          <a className={route.name === 'batches' || route.name === 'batch' ? 'active' : ''} href="#/batches">Batches</a>
          <a className={route.name === 'calendar' ? 'active' : ''} href="#/calendar">Calendar</a>
          <a className={route.name === 'assets' ? 'active' : ''} href="#/assets">Visual assets</a>
          <a className={route.name === 'templates' ? 'active' : ''} href="#/templates">Prompt templates</a>
          <a className={route.name === 'analytics' ? 'active' : ''} href="#/analytics">Analytics insights</a>
          <a className={route.name === 'providerLogs' ? 'active' : ''} href="#/provider-logs">Provider logs</a>
          <a className={route.name === 'settings' ? 'active' : ''} href="#/settings/ai">AI fallback status</a>
          <a className={route.name === 'audioSettings' ? 'active' : ''} href="#/settings/audio">Audio fallback status</a>
          <a href="http://127.0.0.1:8000" target="_blank" rel="noreferrer">Legacy Jinja UI</a>
        </nav>
        <div className="side-note">
          <strong>Current rule</strong>
          <span>Plan 20-30 Shorts as batches. Publish consistently. Automate only after the workflow proves value.</span>
        </div>
      </aside>

      <main className="main-area">
        {route.name === 'dashboard' && <Dashboard />}
        {route.name === 'new' && <CreatePackage />}
        {route.name === 'package' && <PackageDetail id={route.id} />}
        {route.name === 'batches' && <BatchesPage />}
        {route.name === 'batch' && <BatchDetail id={route.id} />}
        {route.name === 'calendar' && <CalendarPage />}
        {route.name === 'assets' && <VisualAssetsPage />}
        {route.name === 'templates' && <PromptTemplatesPage />}
        {route.name === 'analytics' && <AnalyticsInsightsPage />}
        {route.name === 'providerLogs' && <ProviderLogsPage />}
        {route.name === 'settings' && <AiSettings />}
        {route.name === 'audioSettings' && <AudioSettings />}
      </main>
    </div>
  )
}

function parseRoute(hash) {
  const clean = hash.replace(/^#/, '') || '/'
  const parts = clean.split('/').filter(Boolean)
  if (clean === '/' || parts.length === 0) return { name: 'dashboard' }
  if (parts[0] === 'new') return { name: 'new' }
  if (parts[0] === 'packages' && parts[1]) return { name: 'package', id: parts[1] }
  if (parts[0] === 'batches' && parts[1]) return { name: 'batch', id: parts[1] }
  if (parts[0] === 'batches') return { name: 'batches' }
  if (parts[0] === 'calendar') return { name: 'calendar' }
  if (parts[0] === 'assets') return { name: 'assets' }
  if (parts[0] === 'templates') return { name: 'templates' }
  if (parts[0] === 'analytics') return { name: 'analytics' }
  if (parts[0] === 'provider-logs') return { name: 'providerLogs' }
  if (parts[0] === 'settings' && parts[1] === 'ai') return { name: 'settings' }
  if (parts[0] === 'settings' && parts[1] === 'audio') return { name: 'audioSettings' }
  return { name: 'dashboard' }
}

function Dashboard() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchPackages().then(setData).catch((err) => setError(err.message))
  }, [])

  if (error) return <ErrorCard title="Could not load packages" message={error} />
  if (!data) return <Loading />

  return (
    <section>
      <Header
        title="Creator dashboard"
        subtitle="Track generated Shorts packages, content batches, calendar items, review status, and production progress."
        action={<button onClick={() => navigate('#/new')}>Create new package</button>}
      />

      <div className="stats-grid">
        <StatCard label="Total packages" value={data.stats.total} />
        <StatCard label="Published" value={data.stats.published} />
        <StatCard label="Active batches" value={data.stats.active_batches} />
        <StatCard label="Scheduled items" value={data.stats.scheduled_items} />
        <StatCard label="Visual assets" value={data.stats.visual_assets || 0} />
      </div>

      <div className="quick-actions card">
        <button onClick={() => navigate('#/batches')}>Plan a 20-Short batch</button>
        <button className="secondary" onClick={() => navigate('#/calendar')}>Open publishing calendar</button>
        <button className="secondary" onClick={() => navigate('#/assets')}>Upload visual assets</button>
        <button className="secondary" onClick={() => navigate('#/templates')}>Manage prompt templates</button>
        <button className="secondary" onClick={() => navigate('#/analytics')}>View analytics insights</button>
        <button className="secondary" onClick={() => navigate('#/provider-logs')}>Review provider logs</button>
        <button className="secondary" onClick={() => navigate('#/settings/ai')}>Check AI fallback</button>
      </div>

      <div className="card">
        <div className="card-header">
          <h2>Recent content packages</h2>
          <span>{data.packages.length} items</span>
        </div>
        {data.packages.length === 0 ? (
          <EmptyState />
        ) : (
          <div className="package-list">
            {data.packages.map((item) => (
              <button key={item.id} className="package-row" onClick={() => navigate(`#/packages/${item.id}`)}>
                <div>
                  <h3>{item.topic}</h3>
                  <p>{item.class_level} • {item.subject} • {item.language}</p>
                  {item.batch_name && <p>Batch: {item.batch_name}</p>}
                </div>
                <div className="row-meta">
                  <TrustBadge score={item.trust_score} />
                  <StatusBadge status={item.review_status} />
                </div>
              </button>
            ))}
          </div>
        )}
      </div>
    </section>
  )
}

function CreatePackage() {
  const [form, setForm] = useState(initialForm)
  const [batches, setBatches] = useState([])
  const [promptTemplates, setPromptTemplates] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchBatches().then((result) => setBatches(result.batches || [])).catch(() => setBatches([]))
    fetchPromptTemplates('script').then((result) => setPromptTemplates(result.prompt_templates || [])).catch(() => setPromptTemplates([]))
  }, [])

  function update(name, value) {
    setForm((current) => ({ ...current, [name]: value }))
  }

  async function onSubmit(event) {
    event.preventDefault()
    setLoading(true)
    setError('')
    try {
      const payload = {
        ...form,
        duration_seconds: Number(form.duration_seconds),
        copied_text_used: Boolean(form.copied_text_used)
      }
      if (form.batch_id) payload.batch_id = Number(form.batch_id)
      else delete payload.batch_id
      if (form.prompt_template_id) payload.prompt_template_id = Number(form.prompt_template_id)
      else delete payload.prompt_template_id
      const result = await generateContent(payload)
      navigate(`#/packages/${result.package.id}`)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section>
      <Header
        title="Create Shorts package"
        subtitle="Generate script, storyboard, subtitles, title options, quiz, and review metadata. Assign it to a batch if you are planning a content sprint."
      />

      <form className="card form-grid" onSubmit={onSubmit}>
        {error && <div className="form-error">{error}</div>}

        <Input label="Board / Source" value={form.board_source} onChange={(v) => update('board_source', v)} />
        <Input label="Class / Level" value={form.class_level} onChange={(v) => update('class_level', v)} />
        <Input label="Subject" value={form.subject} onChange={(v) => update('subject', v)} />
        <Input label="Topic / Concept" value={form.topic} onChange={(v) => update('topic', v)} />
        <Input label="Audience" value={form.audience} onChange={(v) => update('audience', v)} />
        <Input label="Language" value={form.language} onChange={(v) => update('language', v)} />
        <Input type="number" label="Duration seconds" value={form.duration_seconds} onChange={(v) => update('duration_seconds', v)} />

        <Select
          label="Output type"
          value={form.output_type}
          options={['Short', 'Notes', 'Quiz', 'Worksheet']}
          onChange={(v) => update('output_type', v)}
        />
        <Select
          label="Tone"
          value={form.tone}
          options={['Curious', 'Simple', 'Exam-focused', 'Story-based', 'Mistake correction']}
          onChange={(v) => update('tone', v)}
        />
        <Select
          label="Content batch"
          value={form.batch_id}
          options={[{ value: '', label: 'No batch yet' }, ...batches.map((b) => ({ value: String(b.id), label: b.name }))]}
          onChange={(v) => update('batch_id', v)}
        />
        <Select
          label="Prompt template"
          value={form.prompt_template_id}
          options={[{ value: '', label: 'Use tone default' }, ...promptTemplates.filter((t) => t.active).map((t) => ({ value: String(t.id), label: `${t.name} (${t.style_key})` }))]}
          onChange={(v) => update('prompt_template_id', v)}
        />

        <Input label="Source name" value={form.source_name} onChange={(v) => update('source_name', v)} />
        <Input label="Source license type" value={form.source_license_type} onChange={(v) => update('source_license_type', v)} />
        <Input label="Page / section reference" value={form.page_or_section_reference} onChange={(v) => update('page_or_section_reference', v)} />

        <TextArea label="Source notes / facts" value={form.source_notes} onChange={(v) => update('source_notes', v)} rows={6} wide />
        <TextArea label="Transformation notes" value={form.transformation_notes} onChange={(v) => update('transformation_notes', v)} rows={4} wide />

        <label className="checkbox-line wide">
          <input
            type="checkbox"
            checked={form.copied_text_used}
            onChange={(event) => update('copied_text_used', event.target.checked)}
          />
          <span>Copied textbook wording was used directly. This should normally stay unchecked.</span>
        </label>

        <div className="form-actions wide">
          <button type="button" className="secondary" onClick={() => setForm(initialForm)}>Reset sample</button>
          <button type="submit" disabled={loading}>{loading ? 'Generating...' : 'Generate package'}</button>
        </div>
      </form>
    </section>
  )
}

function BatchesPage() {
  const [data, setData] = useState(null)
  const [form, setForm] = useState(initialBatch)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  function load() {
    setError('')
    fetchBatches().then(setData).catch((err) => setError(err.message))
  }

  useEffect(load, [])

  function update(name, value) {
    setForm((current) => ({ ...current, [name]: value }))
  }

  async function submit(event) {
    event.preventDefault()
    setMessage('')
    setError('')
    try {
      await createBatch({ ...form, planned_count: Number(form.planned_count) })
      setForm(initialBatch)
      setMessage('Batch created. Now create packages and assign them to this batch.')
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  if (error && !data) return <ErrorCard title="Could not load batches" message={error} />
  if (!data) return <Loading />

  return (
    <section>
      <Header
        title="Content batch planner"
        subtitle="Plan 20-30 Shorts at a time so the project supports consistent publishing instead of random one-off generation."
        action={<button onClick={() => navigate('#/new')}>Create package</button>}
      />

      {message && <div className="success-banner">{message}</div>}
      {error && <div className="form-error">{error}</div>}

      <form className="card form-grid" onSubmit={submit}>
        <Input label="Batch name" value={form.name} onChange={(v) => update('name', v)} />
        <Input label="Niche" value={form.niche} onChange={(v) => update('niche', v)} />
        <Input label="Target audience" value={form.target_audience} onChange={(v) => update('target_audience', v)} />
        <Input type="date" label="Start date" value={form.start_date} onChange={(v) => update('start_date', v)} />
        <Input type="date" label="End date" value={form.end_date} onChange={(v) => update('end_date', v)} />
        <Input type="number" label="Planned count" value={form.planned_count} onChange={(v) => update('planned_count', v)} />
        <Select label="Status" value={form.status} options={['planning', 'active', 'completed', 'paused']} onChange={(v) => update('status', v)} />
        <TextArea label="Notes" value={form.notes} onChange={(v) => update('notes', v)} rows={4} wide />
        <div className="form-actions wide"><button type="submit">Create batch</button></div>
      </form>

      <div className="card">
        <div className="card-header">
          <h2>Batches</h2>
          <span>{data.batches.length} total</span>
        </div>
        {data.batches.length === 0 ? (
          <p className="muted">No batches yet. Create your first 20-Short batch above.</p>
        ) : (
          <div className="package-list">
            {data.batches.map((batch) => (
              <button key={batch.id} className="package-row" onClick={() => navigate(`#/batches/${batch.id}`)}>
                <div>
                  <h3>{batch.name}</h3>
                  <p>{batch.niche} • {batch.target_audience}</p>
                  <p>{batch.completed_count}/{batch.planned_count} packages • {batch.scheduled_count} scheduled • {batch.published_count} published</p>
                </div>
                <div className="row-meta"><StatusBadge status={batch.status} /></div>
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="card">
        <div className="card-header">
          <h2>Unassigned packages</h2>
          <span>{data.unassigned_packages.length} items</span>
        </div>
        {data.unassigned_packages.length === 0 ? <p className="muted">All packages are assigned to batches.</p> : (
          <div className="package-list compact">
            {data.unassigned_packages.map((item) => (
              <button key={item.id} className="package-row" onClick={() => navigate(`#/packages/${item.id}`)}>
                <div><h3>{item.topic}</h3><p>{item.class_level} • {item.subject}</p></div>
                <div className="row-meta"><TrustBadge score={item.trust_score} /><StatusBadge status={item.review_status} /></div>
              </button>
            ))}
          </div>
        )}
      </div>
    </section>
  )
}

function BatchDetail({ id }) {
  const [data, setData] = useState(null)
  const [form, setForm] = useState(null)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  function load() {
    setError('')
    fetchBatch(id)
      .then((result) => {
        setData(result)
        setForm(result.batch)
      })
      .catch((err) => setError(err.message))
  }

  useEffect(load, [id])

  function update(name, value) {
    setForm((current) => ({ ...current, [name]: value }))
  }

  async function submit(event) {
    event.preventDefault()
    setMessage('')
    setError('')
    try {
      await updateBatch(id, { ...form, planned_count: Number(form.planned_count) })
      setMessage('Batch updated.')
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  if (error && !data) return <ErrorCard title="Could not load batch" message={error} />
  if (!data || !form) return <Loading />

  return (
    <section>
      <Header
        title={data.batch.name}
        subtitle={`${data.batch.completed_count}/${data.batch.planned_count} packages • ${data.batch.scheduled_count} scheduled • ${data.batch.published_count} published`}
        action={<button onClick={() => navigate('#/new')}>Create package for batch</button>}
      />
      {message && <div className="success-banner">{message}</div>}
      {error && <div className="form-error">{error}</div>}

      <form className="card form-grid" onSubmit={submit}>
        <Input label="Batch name" value={form.name} onChange={(v) => update('name', v)} />
        <Input label="Niche" value={form.niche} onChange={(v) => update('niche', v)} />
        <Input label="Target audience" value={form.target_audience} onChange={(v) => update('target_audience', v)} />
        <Input type="date" label="Start date" value={form.start_date || ''} onChange={(v) => update('start_date', v)} />
        <Input type="date" label="End date" value={form.end_date || ''} onChange={(v) => update('end_date', v)} />
        <Input type="number" label="Planned count" value={form.planned_count} onChange={(v) => update('planned_count', v)} />
        <Select label="Status" value={form.status} options={['planning', 'active', 'completed', 'paused']} onChange={(v) => update('status', v)} />
        <TextArea label="Notes" value={form.notes || ''} onChange={(v) => update('notes', v)} rows={4} wide />
        <div className="form-actions wide"><button type="submit">Save batch</button></div>
      </form>

      <div className="card">
        <div className="card-header">
          <h2>Packages in this batch</h2>
          <span>{data.packages.length} items</span>
        </div>
        {data.packages.length === 0 ? <p className="muted">No packages yet. Create a package and select this batch.</p> : (
          <div className="package-list">
            {data.packages.map((item) => (
              <button key={item.id} className="package-row" onClick={() => navigate(`#/packages/${item.id}`)}>
                <div>
                  <h3>{item.topic}</h3>
                  <p>{item.class_level} • {item.subject} • {item.language}</p>
                  {item.planned_publish_date && <p>Calendar: {item.planned_publish_date} • {item.calendar_status} • {item.platform}</p>}
                </div>
                <div className="row-meta"><TrustBadge score={item.trust_score} /><StatusBadge status={item.review_status} /></div>
              </button>
            ))}
          </div>
        )}
      </div>
    </section>
  )
}

function CalendarPage() {
  const [data, setData] = useState(null)
  const [form, setForm] = useState(initialCalendar)
  const [editing, setEditing] = useState(null)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  function load() {
    setError('')
    fetchCalendar().then(setData).catch((err) => setError(err.message))
  }

  useEffect(load, [])

  function update(name, value) {
    setForm((current) => ({ ...current, [name]: value }))
  }

  function startEdit(entry) {
    setEditing(entry.id)
    setForm({
      package_id: String(entry.package_id),
      planned_publish_date: entry.planned_publish_date || today(),
      actual_publish_date: entry.actual_publish_date || '',
      platform: entry.platform || 'YouTube Shorts',
      status: entry.status || 'planned',
      playlist_name: entry.playlist_name || '',
      notes: entry.notes || ''
    })
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  function resetForm() {
    setEditing(null)
    setForm(initialCalendar)
  }

  async function submit(event) {
    event.preventDefault()
    setMessage('')
    setError('')
    try {
      const payload = { ...form, package_id: Number(form.package_id) }
      if (!payload.package_id) throw new Error('Select a package to schedule.')
      if (editing) {
        const { package_id, ...updatePayload } = payload
        await updateCalendarEntry(editing, updatePayload)
        setMessage('Calendar entry updated.')
      } else {
        await createCalendarEntry(payload)
        setMessage('Package scheduled.')
      }
      resetForm()
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  async function remove(id) {
    setMessage('')
    setError('')
    try {
      await deleteCalendarEntry(id)
      setMessage('Calendar entry removed.')
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  if (error && !data) return <ErrorCard title="Could not load calendar" message={error} />
  if (!data) return <Loading />

  const packageOptions = [
    { value: '', label: 'Select package' },
    ...data.unscheduled_packages.map((p) => ({ value: String(p.id), label: `${p.topic} (${p.review_status})` })),
    ...data.calendar.map((p) => ({ value: String(p.package_id), label: `${p.topic} (already scheduled)` }))
  ]

  return (
    <section>
      <Header
        title="Publishing calendar"
        subtitle="Schedule Shorts manually first. This keeps production moving before YouTube API automation is needed."
        action={<button onClick={() => navigate('#/new')}>Create package</button>}
      />
      {message && <div className="success-banner">{message}</div>}
      {error && <div className="form-error">{error}</div>}

      <form className="card form-grid" onSubmit={submit}>
        <Select label="Package" value={form.package_id} options={packageOptions} onChange={(v) => update('package_id', v)} disabled={Boolean(editing)} />
        <Input type="date" label="Planned publish date" value={form.planned_publish_date} onChange={(v) => update('planned_publish_date', v)} />
        <Input type="date" label="Actual publish date" value={form.actual_publish_date} onChange={(v) => update('actual_publish_date', v)} />
        <Input label="Platform" value={form.platform} onChange={(v) => update('platform', v)} />
        <Select label="Status" value={form.status} options={['planned', 'scheduled', 'published', 'skipped']} onChange={(v) => update('status', v)} />
        <Input label="Playlist name" value={form.playlist_name} onChange={(v) => update('playlist_name', v)} />
        <TextArea label="Notes" value={form.notes} onChange={(v) => update('notes', v)} rows={3} wide />
        <div className="form-actions wide">
          {editing && <button type="button" className="secondary" onClick={resetForm}>Cancel edit</button>}
          <button type="submit">{editing ? 'Save calendar entry' : 'Schedule package'}</button>
        </div>
      </form>

      <div className="card">
        <div className="card-header"><h2>Scheduled content</h2><span>{data.calendar.length} items</span></div>
        {data.calendar.length === 0 ? <p className="muted">No scheduled content yet.</p> : (
          <div className="calendar-list">
            {data.calendar.map((entry) => (
              <div className="calendar-entry" key={entry.id}>
                <div>
                  <strong>{entry.planned_publish_date} • {entry.topic}</strong>
                  <p>{entry.platform} • {entry.playlist_name || 'No playlist'} • {entry.batch_name || 'No batch'}</p>
                  {entry.notes && <p>{entry.notes}</p>}
                </div>
                <div className="row-meta">
                  <StatusBadge status={entry.status} />
                  <button className="secondary small" onClick={() => startEdit(entry)}>Edit</button>
                  <button className="secondary small" onClick={() => remove(entry.id)}>Remove</button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="card">
        <div className="card-header"><h2>Unscheduled packages</h2><span>{data.unscheduled_packages.length} items</span></div>
        {data.unscheduled_packages.length === 0 ? <p className="muted">All packages are scheduled.</p> : (
          <div className="package-list compact">
            {data.unscheduled_packages.map((item) => (
              <button key={item.id} className="package-row" onClick={() => setForm({ ...initialCalendar, package_id: String(item.id) })}>
                <div><h3>{item.topic}</h3><p>{item.class_level} • {item.subject} • {item.batch_name || 'No batch'}</p></div>
                <div className="row-meta"><TrustBadge score={item.trust_score} /><StatusBadge status={item.review_status} /></div>
              </button>
            ))}
          </div>
        )}
      </div>
    </section>
  )
}

function VisualAssetsPage() {
  const [assets, setAssets] = useState([])
  const [form, setForm] = useState(initialVisualAsset)
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  function load() {
    setLoading(true)
    fetchVisualAssets()
      .then((result) => {
        setAssets(result.assets || [])
        setError('')
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }

  useEffect(load, [])

  function update(name, value) {
    setForm((current) => ({ ...current, [name]: value }))
  }

  async function submit(event) {
    event.preventDefault()
    setMessage('')
    setError('')
    if (!file) {
      setError('Please choose an image file first.')
      return
    }
    try {
      const formData = new FormData()
      Object.entries(form).forEach(([key, value]) => formData.append(key, value))
      formData.append('file', file)
      const result = await uploadVisualAsset(formData)
      setAssets((current) => [result.asset, ...current])
      setFile(null)
      event.target.reset()
      setForm(initialVisualAsset)
      setMessage('Visual asset uploaded. It can now be reused in video drafts when tags match the scene.')
    } catch (err) {
      setError(err.message)
    }
  }

  async function remove(assetId) {
    setMessage('')
    setError('')
    try {
      await deleteVisualAsset(assetId)
      setAssets((current) => current.filter((asset) => asset.id !== assetId))
      setMessage('Visual asset removed.')
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <section>
      <Header
        title="Reusable visual assets"
        subtitle="Upload icons, diagrams, screenshots, or simple images once. Matching assets are reused in MP4 draft scene cards before you move to CapCut."
        action={<button onClick={() => navigate('#/new')}>Create package</button>}
      />
      {message && <div className="success-banner">{message}</div>}
      {error && <div className="form-error">{error}</div>}

      <div className="detail-grid">
        <form className="card stack" onSubmit={submit}>
          <h2>Upload asset</h2>
          <p className="muted">Use clear tags such as <strong>leaf, chlorophyll, photosynthesis</strong>. The draft generator matches tags with scene text.</p>
          <Input label="Title" value={form.title} onChange={(v) => update('title', v)} />
          <Input label="Tags" value={form.tags} onChange={(v) => update('tags', v)} />
          <TextArea label="Description" value={form.description} onChange={(v) => update('description', v)} rows={3} />
          <Input label="Source type" value={form.source_type} onChange={(v) => update('source_type', v)} />
          <Input label="License type" value={form.license_type} onChange={(v) => update('license_type', v)} />
          <TextArea label="Notes" value={form.notes} onChange={(v) => update('notes', v)} rows={3} />
          <label className="field">
            <span>Image file</span>
            <input type="file" accept="image/png,image/jpeg,image/webp,image/gif" onChange={(event) => setFile(event.target.files?.[0] || null)} />
          </label>
          <button type="submit">Upload visual asset</button>
        </form>

        <div className="card stack">
          <h2>How matching works</h2>
          <p className="muted">When you generate a vertical MP4 draft, the backend checks each scene's topic, script, subtitle, and visual direction. If those words match asset tags, the image appears in the scene card.</p>
          <ul className="check-list">
            <li>Use simple PNG/JPG/WebP images.</li>
            <li>Prefer self-created, open-license, or Canva-made assets.</li>
            <li>Use 3–8 meaningful tags per asset.</li>
            <li>Do not upload copyrighted textbook screenshots unless you have rights.</li>
          </ul>
        </div>
      </div>

      <div className="card stack">
        <div className="card-header">
          <h2>Asset library</h2>
          <span>{assets.length} assets</span>
        </div>
        {loading ? <Loading /> : assets.length === 0 ? (
          <p className="muted">No visual assets yet. Upload your first reusable diagram or icon.</p>
        ) : (
          <div className="asset-grid">
            {assets.map((asset) => (
              <div className="asset-card" key={asset.id}>
                <img src={visualAssetUrl(asset.id)} alt={asset.title} />
                <div>
                  <h3>{asset.title}</h3>
                  <p>{asset.description || 'No description'}</p>
                  <p className="tag-line">{asset.tags}</p>
                  <p className="muted">{asset.source_type} • {asset.license_type || 'license not set'}</p>
                  <div className="row-meta">
                    <a className="button-link small" href={visualAssetUrl(asset.id)} target="_blank" rel="noreferrer">Open</a>
                    <button className="danger small" onClick={() => remove(asset.id)}>Delete</button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  )
}


function PromptTemplatesPage() {
  const [templates, setTemplates] = useState([])
  const [form, setForm] = useState(initialPromptTemplate)
  const [editingId, setEditingId] = useState(null)
  const [preview, setPreview] = useState(null)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  function load() {
    setLoading(true)
    fetchPromptTemplates()
      .then((result) => {
        setTemplates(result.prompt_templates || [])
        setError('')
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }

  useEffect(load, [])

  function update(name, value) {
    setForm((current) => ({ ...current, [name]: value }))
  }

  function edit(template) {
    setEditingId(template.id)
    setPreview(null)
    setForm({
      name: template.name,
      task_type: template.task_type,
      style_key: template.style_key,
      active: Boolean(template.active),
      notes: template.notes || '',
      template_text: template.template_text || ''
    })
  }

  function reset() {
    setEditingId(null)
    setPreview(null)
    setForm(initialPromptTemplate)
  }

  async function save(event) {
    event.preventDefault()
    setMessage('')
    setError('')
    try {
      const payload = {
        ...form,
        active: Boolean(form.active)
      }
      const result = editingId
        ? await updatePromptTemplate(editingId, payload)
        : await createPromptTemplate(payload)
      setTemplates((current) => {
        if (editingId) return current.map((item) => item.id === result.prompt_template.id ? result.prompt_template : item)
        return [result.prompt_template, ...current]
      })
      setMessage(editingId ? 'Prompt template updated.' : 'Prompt template created.')
      reset()
    } catch (err) {
      setError(err.message)
    }
  }

  async function remove(templateId) {
    setMessage('')
    setError('')
    try {
      await deletePromptTemplate(templateId)
      setTemplates((current) => current.filter((item) => item.id !== templateId))
      if (editingId === templateId) reset()
      setMessage('Prompt template deleted.')
    } catch (err) {
      setError(err.message)
    }
  }

  async function seedDefaults() {
    setMessage('')
    setError('')
    try {
      const result = await seedPromptTemplates()
      setTemplates(result.prompt_templates || [])
      setMessage(result.created ? `Seeded ${result.created} default templates.` : 'Default templates already exist.')
    } catch (err) {
      setError(err.message)
    }
  }

  async function previewTemplate(template) {
    setMessage('')
    setError('')
    try {
      const payload = {
        ...initialForm,
        duration_seconds: Number(initialForm.duration_seconds),
        copied_text_used: Boolean(initialForm.copied_text_used)
      }
      delete payload.batch_id
      delete payload.prompt_template_id
      const result = await previewPromptTemplate(template.id, payload)
      setPreview(result.preview)
      setMessage(`Preview generated for ${template.name}.`)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <section>
      <Header
        title="Prompt template manager"
        subtitle="Create reusable hook/script styles so every Short does not sound the same. Templates are selected when generating a package."
        action={<button onClick={seedDefaults}>Seed default templates</button>}
      />
      {message && <div className="success-banner">{message}</div>}
      {error && <div className="form-error">{error}</div>}

      <div className="detail-grid">
        <form className="card stack" onSubmit={save}>
          <h2>{editingId ? 'Edit prompt template' : 'Create prompt template'}</h2>
          <Input label="Name" value={form.name} onChange={(v) => update('name', v)} />
          <Input label="Task type" value={form.task_type} onChange={(v) => update('task_type', v)} />
          <Input label="Style key" value={form.style_key} onChange={(v) => update('style_key', v)} />
          <Select label="Active" value={form.active ? 'true' : 'false'} options={[{ value: 'true', label: 'Active' }, { value: 'false', label: 'Inactive' }]} onChange={(v) => update('active', v === 'true')} />
          <TextArea label="Template text" value={form.template_text} onChange={(v) => update('template_text', v)} rows={12} />
          <TextArea label="Notes" value={form.notes} onChange={(v) => update('notes', v)} rows={3} />
          <div className="button-row">
            <button type="submit">{editingId ? 'Save template' : 'Create template'}</button>
            {editingId && <button type="button" className="secondary" onClick={reset}>Cancel edit</button>}
          </div>
        </form>

        <div className="card stack">
          <h2>Available placeholders</h2>
          <p className="muted">Use these inside template text. Unknown placeholders stay unchanged instead of breaking generation.</p>
          <div className="pill-list">
            {['{hook}', '{topic}', '{topic_lower}', '{top_fact}', '{simple_meaning}', '{analogy}', '{memory_line}', '{class_level}', '{subject}', '{audience}', '{duration_seconds}', '{source_notes}', '{hashtags}'].map((item) => <span key={item}>{item}</span>)}
          </div>
          <p className="muted">Recommended: create 5-10 templates only. Too many templates make the workflow confusing.</p>
        </div>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Templates</h2><span>{templates.length} items</span></div>
        {loading ? <Loading /> : templates.length === 0 ? (
          <p className="muted">No templates yet. Click Seed default templates.</p>
        ) : (
          <div className="template-list">
            {templates.map((template) => (
              <div className="template-entry" key={template.id}>
                <div>
                  <h3>{template.name}</h3>
                  <p>{template.task_type} • {template.style_key} • {template.active ? 'active' : 'inactive'}</p>
                  {template.notes && <p className="muted">{template.notes}</p>}
                </div>
                <div className="row-meta">
                  <StatusBadge status={template.active ? 'active' : 'inactive'} />
                  <button className="secondary small" onClick={() => previewTemplate(template)}>Preview</button>
                  <button className="secondary small" onClick={() => edit(template)}>Edit</button>
                  <button className="danger small" onClick={() => remove(template.id)}>Delete</button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {preview && (
        <TextCard title={`Preview: ${preview.template_name}`} value={preview.rendered_text} />
      )}
    </section>
  )
}

function PackageDetail({ id }) {
  const [data, setData] = useState(null)
  const [batches, setBatches] = useState([])
  const [scriptText, setScriptText] = useState('')
  const [reviewStatus, setReviewStatus] = useState('draft')
  const [reviewerNotes, setReviewerNotes] = useState('')
  const [selectedBatchId, setSelectedBatchId] = useState('')
  const [audioGenerating, setAudioGenerating] = useState(false)
  const [assemblyGenerating, setAssemblyGenerating] = useState(false)
  const [videoDraftGenerating, setVideoDraftGenerating] = useState(false)
  const [thumbnailGenerating, setThumbnailGenerating] = useState(false)
  const [sourceSafetyGenerating, setSourceSafetyGenerating] = useState(false)
  const [trustReviewGenerating, setTrustReviewGenerating] = useState(false)
  const [learningOutputGenerating, setLearningOutputGenerating] = useState(false)
  const [editingTrustReview, setEditingTrustReview] = useState(null)
  const [trustReviewSaving, setTrustReviewSaving] = useState(false)
  const [analytics, setAnalytics] = useState({
    platform: 'YouTube Shorts',
    entry_date: today(),
    views: 0,
    likes: 0,
    comments: 0,
    shares: 0,
    avg_view_duration_seconds: 0,
    retention_pct: 0,
    ctr_pct: 0,
    notes: ''
  })
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  function load() {
    setData(null)
    fetchPackage(id)
      .then((result) => {
        setData(result)
        setScriptText(result.package.script_text || '')
        setReviewStatus(result.package.review_status || 'draft')
        setReviewerNotes(result.package.reviewer_notes || '')
        setSelectedBatchId(result.package.batch_id ? String(result.package.batch_id) : '')
      })
      .catch((err) => setError(err.message))
    fetchBatches().then((result) => setBatches(result.batches || [])).catch(() => setBatches([]))
  }

  useEffect(load, [id])

  async function saveReview() {
    setMessage('')
    setError('')
    try {
      const result = await updateReview(id, { review_status: reviewStatus, script_text: scriptText, reviewer_notes: reviewerNotes })
      setData((current) => ({ ...current, package: result.package }))
      setMessage('Review saved.')
    } catch (err) {
      setError(err.message)
    }
  }

  async function saveBatch() {
    setMessage('')
    setError('')
    try {
      const result = await assignPackageBatch(id, { batch_id: selectedBatchId ? Number(selectedBatchId) : null })
      setData((current) => ({ ...current, package: result.package }))
      setMessage('Batch assignment saved.')
    } catch (err) {
      setError(err.message)
    }
  }



  async function createNarrationAudio() {
    setMessage('')
    setError('')
    setAudioGenerating(true)
    try {
      const result = await generateAudio(id)
      setData((current) => ({
        ...current,
        audio_assets: [result.audio_asset, ...(current.audio_assets || [])]
      }))
      setMessage(result.audio_asset.status === 'generated' ? 'Narration audio generated.' : 'Manual recording guide created.')
    } catch (err) {
      setError(err.message)
    } finally {
      setAudioGenerating(false)
    }
  }

  async function createAssemblyPlan() {
    setMessage('')
    setError('')
    setAssemblyGenerating(true)
    try {
      const result = await generateAssembly(id)
      setData((current) => ({
        ...current,
        assembly_plans: [result.assembly_plan, ...(current.assembly_plans || [])]
      }))
      setMessage('CapCut/manual assembly plan generated.')
    } catch (err) {
      setError(err.message)
    } finally {
      setAssemblyGenerating(false)
    }
  }


  async function createThumbnailGuide() {
    setMessage('')
    setError('')
    setThumbnailGenerating(true)
    try {
      const result = await generateThumbnailGuide(id)
      setData((current) => ({
        ...current,
        thumbnail_guides: [result.thumbnail_guide, ...(current.thumbnail_guides || [])]
      }))
      setMessage('Thumbnail helper generated.')
    } catch (err) {
      setError(err.message)
    } finally {
      setThumbnailGenerating(false)
    }
  }


  async function createSourceSafetyReview() {
    setMessage('')
    setError('')
    setSourceSafetyGenerating(true)
    try {
      const result = await generateSourceSafetyReview(id)
      setData((current) => ({
        ...current,
        source_safety_reviews: [result.source_safety_review, ...(current.source_safety_reviews || [])]
      }))
      const review = result.source_safety_review
      setMessage(`Source safety review generated. Risk: ${review.risk_level}. Similarity: ${review.similarity_score}%.`)
    } catch (err) {
      setError(err.message)
    } finally {
      setSourceSafetyGenerating(false)
    }
  }


  async function createTrustReview() {
    setMessage('')
    setError('')
    setTrustReviewGenerating(true)
    try {
      const result = await generateTrustReview(id)
      setData((current) => ({
        ...current,
        package: result.package,
        trust_reviews: [result.trust_review, ...(current.trust_reviews || [])]
      }))
      setEditingTrustReview(result.trust_review)
      setMessage(`Teacher Trust Score generated: ${result.trust_review.overall_trust_score}.`)
    } catch (err) {
      setError(err.message)
    } finally {
      setTrustReviewGenerating(false)
    }
  }

  async function saveTrustReview() {
    if (!editingTrustReview) return
    setMessage('')
    setError('')
    setTrustReviewSaving(true)
    try {
      const payload = {
        factual_accuracy_score: Number(editingTrustReview.factual_accuracy_score),
        age_appropriateness_score: Number(editingTrustReview.age_appropriateness_score),
        simplicity_score: Number(editingTrustReview.simplicity_score),
        visual_clarity_score: Number(editingTrustReview.visual_clarity_score),
        engagement_score: Number(editingTrustReview.engagement_score),
        source_safety_score: Number(editingTrustReview.source_safety_score),
        reviewer_confidence_score: Number(editingTrustReview.reviewer_confidence_score),
        reviewer_decision: editingTrustReview.reviewer_decision || 'pending',
        reviewer_notes: editingTrustReview.reviewer_notes || '',
        checklist_json: editingTrustReview.checklist_json || '[]'
      }
      const result = await updateTrustReview(id, editingTrustReview.id, payload)
      setData((current) => ({
        ...current,
        package: result.package,
        trust_reviews: (current.trust_reviews || []).map((item) => item.id === result.trust_review.id ? result.trust_review : item)
      }))
      setEditingTrustReview(result.trust_review)
      setMessage(`Teacher Trust Score saved: ${result.trust_review.overall_trust_score}.`)
    } catch (err) {
      setError(err.message)
    } finally {
      setTrustReviewSaving(false)
    }
  }

  function updateEditingTrustReview(name, value) {
    setEditingTrustReview((current) => ({ ...current, [name]: value }))
  }

  async function createLearningOutput() {
    setMessage('')
    setError('')
    setLearningOutputGenerating(true)
    try {
      const result = await generateLearningOutput(id)
      setData((current) => ({
        ...current,
        learning_outputs: [result.learning_output, ...(current.learning_outputs || [])]
      }))
      setMessage('Learning outputs generated: notes, flashcards, quiz, and worksheet.')
    } catch (err) {
      setError(err.message)
    } finally {
      setLearningOutputGenerating(false)
    }
  }


  async function createVideoDraft() {
    setMessage('')
    setError('')
    setVideoDraftGenerating(true)
    try {
      const result = await generateVideoDraft(id)
      setData((current) => ({
        ...current,
        video_drafts: [result.video_draft, ...(current.video_drafts || [])]
      }))
      setMessage(result.video_draft.status === 'generated' ? 'Vertical MP4 draft generated.' : 'Manual video draft guide created.')
    } catch (err) {
      setError(err.message)
    } finally {
      setVideoDraftGenerating(false)
    }
  }

  async function saveAnalytics(event) {
    event.preventDefault()
    setMessage('')
    setError('')
    try {
      const result = await addAnalytics(id, {
        ...analytics,
        views: Number(analytics.views),
        likes: Number(analytics.likes),
        comments: Number(analytics.comments),
        shares: Number(analytics.shares),
        avg_view_duration_seconds: Number(analytics.avg_view_duration_seconds),
        retention_pct: Number(analytics.retention_pct),
        ctr_pct: Number(analytics.ctr_pct)
      })
      setData((current) => ({ ...current, analytics: result.analytics }))
      setMessage('Analytics entry saved.')
    } catch (err) {
      setError(err.message)
    }
  }

  if (error && !data) return <ErrorCard title="Could not load package" message={error} />
  if (!data) return <Loading />

  const pkg = data.package

  return (
    <section>
      <Header
        title={pkg.topic}
        subtitle={`${pkg.class_level} • ${pkg.subject} • ${pkg.duration_seconds}s • ${pkg.provider_used}`}
        action={<a className="button-link" href={exportUrl(id)}>Export ZIP</a>}
      />
      {message && <div className="success-banner">{message}</div>}
      {error && <div className="form-error">{error}</div>}

      <div className="detail-grid">
        <div className="card stack">
          <div className="card-header"><h2>Review</h2><TrustBadge score={pkg.trust_score} /></div>
          <Select label="Review status" value={reviewStatus} options={['draft', 'approved', 'edit_required', 'rejected', 'published']} onChange={setReviewStatus} />
          <TextArea label="Script editor" value={scriptText} onChange={setScriptText} rows={12} />
          <TextArea label="Reviewer notes" value={reviewerNotes} onChange={setReviewerNotes} rows={4} />
          <div className="button-row">
            <button onClick={saveReview}>Save review</button>
            <button className="secondary" onClick={() => copyText(scriptText)}>Copy script</button>
            <button className="secondary" onClick={() => speak(scriptText)}>Preview voice</button>
          </div>
        </div>

        <div className="card stack">
          <h2>Publishing package</h2>
          <InfoBlock title="Hook" value={pkg.hook} />
          <InfoList title="Title options" values={pkg.title_options_list} />
          <InfoBlock title="Description" value={pkg.description} />
          <InfoList title="Hashtags" values={pkg.hashtags_list} inline />
          <InfoBlock title="Quiz question" value={pkg.quiz_question} />
        </div>
      </div>


      <div className="card stack">
        <div className="card-header">
          <div>
            <h2>AI provider attempt log</h2>
            <p className="muted">Shows why the package used its final provider and whether fallback protected the generation.</p>
          </div>
          <button className="secondary small" onClick={() => navigate('#/provider-logs')}>Open all logs</button>
        </div>
        {(data.provider_logs || []).length === 0 ? (
          <p className="muted">No provider logs stored for this package yet. New v15 packages will record detailed attempt logs.</p>
        ) : (
          <div className="performance-table provider-log-table">
            <div className="performance-head"><span>Order</span><span>Provider</span><span>Status</span><span>Duration</span><span>Message</span></div>
            {(data.provider_logs || []).map((log) => (
              <div className="performance-row" key={log.id}>
                <strong>#{log.attempt_order}</strong>
                <span>{log.provider}</span>
                <span>{log.success ? 'success' : 'failed'}</span>
                <span>{log.duration_ms} ms</span>
                <span>{log.message}</span>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="card stack">
        <div className="card-header">
          <div>
            <h2>Thumbnail helper</h2>
            <p className="muted">Generate thumbnail text ideas, a manual layout guide, and a Canva/CapCut prompt for this Short.</p>
          </div>
          <button onClick={createThumbnailGuide} disabled={thumbnailGenerating}>
            {thumbnailGenerating ? 'Generating...' : 'Generate thumbnail helper'}
          </button>
        </div>
        {!data.thumbnail_guides || data.thumbnail_guides.length === 0 ? (
          <p className="muted">No thumbnail helper yet. Generate one before creating the final YouTube/Shorts thumbnail.</p>
        ) : (
          <div className="thumbnail-guide-list">
            {data.thumbnail_guides.map((guide, index) => (
              <div className="thumbnail-guide-entry" key={guide.id}>
                <div>
                  <strong>{guide.file_name}</strong>
                  <p>{guide.status} • {guide.thumbnail_mode}</p>
                  {index === 0 && <p className="muted">Latest guide is included in the export ZIP as thumbnail_guide.md.</p>}
                </div>
                <div className="row-meta">
                  <StatusBadge status={guide.status} />
                  <a className="button-link small" href={thumbnailGuideDownloadUrl(id, guide.id)}>Download guide</a>
                </div>
              </div>
            ))}
          </div>
        )}
        {data.thumbnail_guides && data.thumbnail_guides.length > 0 && (
          <TextCard title="Latest thumbnail layout guide" value={data.thumbnail_guides[0].layout_guide} />
        )}
      </div>

      <div className="card stack">
        <div className="card-header">
          <div>
            <h2>Source safety & originality</h2>
            <p className="muted">Run this before publishing. It checks source metadata, copied-text flag, transformation notes, and similarity between source notes and script.</p>
          </div>
          <button onClick={createSourceSafetyReview} disabled={sourceSafetyGenerating}>
            {sourceSafetyGenerating ? 'Checking...' : 'Generate source safety review'}
          </button>
        </div>
        {!data.source_safety_reviews || data.source_safety_reviews.length === 0 ? (
          <p className="muted">No source safety review yet. Generate one before approving or publishing this Short.</p>
        ) : (
          <div className="source-safety-list">
            {data.source_safety_reviews.map((review, index) => (
              <div className="source-safety-entry" key={review.id}>
                <div>
                  <strong>Review #{review.id}</strong>
                  <p>Risk: {review.risk_level} • Similarity: {review.similarity_score}% • Status: {review.status}</p>
                  <p>{review.recommendation}</p>
                  {index === 0 && <p className="muted">Latest review is included in the export ZIP as source_safety_review.md.</p>}
                </div>
                <div className="row-meta">
                  <StatusBadge status={review.risk_level} />
                  <a className="button-link small" href={sourceSafetyDownloadUrl(id, review.id)}>Download review</a>
                </div>
              </div>
            ))}
          </div>
        )}
        {data.source_safety_reviews && data.source_safety_reviews.length > 0 && (
          <TextCard title="Latest source safety review" value={data.source_safety_reviews[0].review_markdown} />
        )}
      </div>

      <div className="card stack">
        <div className="card-header">
          <div>
            <h2>Teacher Trust Score review</h2>
            <p className="muted">Use this after source safety review. Edit the category scores, add reviewer notes, and save a final approval recommendation.</p>
          </div>
          <button onClick={createTrustReview} disabled={trustReviewGenerating}>
            {trustReviewGenerating ? 'Generating...' : 'Generate trust review'}
          </button>
        </div>
        {!data.trust_reviews || data.trust_reviews.length === 0 ? (
          <p className="muted">No Teacher Trust Score review yet. Generate one before approving or publishing this Short.</p>
        ) : (
          <div className="trust-review-list">
            {data.trust_reviews.map((review, index) => (
              <div className="trust-review-entry" key={review.id}>
                <div>
                  <strong>Trust review #{review.id}</strong>
                  <p>Score: {review.overall_trust_score} • Decision: {review.reviewer_decision} • Approval required: {review.approval_required ? 'Yes' : 'No'}</p>
                  <p>{review.recommendation}</p>
                  {index === 0 && <p className="muted">Latest review is included in the export ZIP as teacher_trust_review.md.</p>}
                </div>
                <div className="row-meta">
                  <TrustBadge score={review.overall_trust_score} />
                  <button className="secondary small" onClick={() => setEditingTrustReview(review)}>Edit scores</button>
                  <a className="button-link small" href={trustReviewDownloadUrl(id, review.id)}>Download review</a>
                </div>
              </div>
            ))}
          </div>
        )}
        {editingTrustReview && (
          <div className="trust-editor">
            <h3>Edit latest trust review</h3>
            <div className="analytics-grid">
              <Input type="number" label="Factual accuracy" value={editingTrustReview.factual_accuracy_score} onChange={(v) => updateEditingTrustReview('factual_accuracy_score', v)} />
              <Input type="number" label="Age appropriateness" value={editingTrustReview.age_appropriateness_score} onChange={(v) => updateEditingTrustReview('age_appropriateness_score', v)} />
              <Input type="number" label="Simplicity" value={editingTrustReview.simplicity_score} onChange={(v) => updateEditingTrustReview('simplicity_score', v)} />
              <Input type="number" label="Visual clarity" value={editingTrustReview.visual_clarity_score} onChange={(v) => updateEditingTrustReview('visual_clarity_score', v)} />
              <Input type="number" label="Engagement" value={editingTrustReview.engagement_score} onChange={(v) => updateEditingTrustReview('engagement_score', v)} />
              <Input type="number" label="Source safety" value={editingTrustReview.source_safety_score} onChange={(v) => updateEditingTrustReview('source_safety_score', v)} />
              <Input type="number" label="Reviewer confidence" value={editingTrustReview.reviewer_confidence_score} onChange={(v) => updateEditingTrustReview('reviewer_confidence_score', v)} />
              <Select label="Reviewer decision" value={editingTrustReview.reviewer_decision || 'pending'} options={['pending', 'approved', 'edit_required', 'rewrite_required', 'rejected']} onChange={(v) => updateEditingTrustReview('reviewer_decision', v)} />
              <TextArea label="Trust reviewer notes" value={editingTrustReview.reviewer_notes || ''} onChange={(v) => updateEditingTrustReview('reviewer_notes', v)} rows={4} wide />
              <div className="wide button-row">
                <button onClick={saveTrustReview} disabled={trustReviewSaving}>{trustReviewSaving ? 'Saving...' : 'Save trust review'}</button>
                <button className="secondary" onClick={() => setEditingTrustReview(null)}>Close editor</button>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="card stack">
        <div className="card-header">
          <div>
            <h2>Learning outputs</h2>
            <p className="muted">Generate reusable revision notes, flashcards, quiz questions, and a worksheet from this Short package.</p>
          </div>
          <button onClick={createLearningOutput} disabled={learningOutputGenerating}>
            {learningOutputGenerating ? 'Generating...' : 'Generate learning outputs'}
          </button>
        </div>
        {!data.learning_outputs || data.learning_outputs.length === 0 ? (
          <p className="muted">No learning output pack yet. Generate this after the script and trust review look good.</p>
        ) : (
          <div className="learning-output-list">
            {data.learning_outputs.map((output, index) => (
              <div className="learning-output-entry" key={output.id}>
                <div>
                  <strong>{output.file_name}</strong>
                  <p>{output.status} • {output.output_mode}</p>
                  {index === 0 && <p className="muted">Latest pack is included in the export ZIP as revision_notes.md, flashcards.json, quiz_questions.json, and worksheet.md.</p>}
                </div>
                <div className="row-meta">
                  <StatusBadge status={output.status} />
                  <a className="button-link small" href={learningOutputDownloadUrl(id, output.id)}>Download pack</a>
                </div>
              </div>
            ))}
          </div>
        )}
        {data.learning_outputs && data.learning_outputs.length > 0 && (
          <div className="detail-grid">
            <TextCard title="Latest revision notes" value={data.learning_outputs[0].revision_notes_markdown} />
            <TextCard title="Latest worksheet" value={data.learning_outputs[0].worksheet_markdown} />
          </div>
        )}
      </div>

      <div className="detail-grid">
        <div className="card stack">
          <h2>Batch & calendar</h2>
          <Select
            label="Content batch"
            value={selectedBatchId}
            options={[{ value: '', label: 'No batch' }, ...batches.map((b) => ({ value: String(b.id), label: b.name }))]}
            onChange={setSelectedBatchId}
          />
          <button onClick={saveBatch}>Save batch assignment</button>
          {data.calendar ? (
            <InfoBlock title="Calendar" value={`${data.calendar.planned_publish_date} • ${data.calendar.platform} • ${data.calendar.status}`} />
          ) : (
            <p className="muted">Not scheduled yet. Use the Calendar page to plan a publish date.</p>
          )}
        </div>
        <div className="card stack">
          <h2>AI provider attempts</h2>
          <p className="muted">The app works without Ollama because the template provider is always available.</p>
          {pkg.prompt_template_name && <InfoBlock title="Prompt template used" value={`${pkg.prompt_template_name} • ${pkg.prompt_template_style || 'style not set'}`} />}
          <div className="attempt-list">
            {pkg.provider_attempts_list.length === 0 ? <span className="muted">No provider attempts recorded.</span> : pkg.provider_attempts_list.map((attempt, index) => (
              <div className="attempt" key={`${attempt.provider}-${index}`}>
                <strong>{attempt.provider}</strong>
                <span>{attempt.success ? 'success' : 'skipped/failed'}</span>
                <p>{attempt.message}</p>
              </div>
            ))}
          </div>
        </div>
      </div>


      <div className="card stack">
        <div className="card-header">
          <div>
            <h2>Narration audio</h2>
            <p className="muted">Generate offline narration when possible. If no local TTS is ready, the system creates a manual recording guide.</p>
          </div>
          <button onClick={createNarrationAudio} disabled={audioGenerating}>
            {audioGenerating ? 'Generating...' : 'Generate narration'}
          </button>
        </div>
        {!data.audio_assets || data.audio_assets.length === 0 ? (
          <p className="muted">No narration asset yet. Use browser voice preview or generate a backend asset.</p>
        ) : (
          <div className="audio-list">
            {data.audio_assets.map((asset) => (
              <div className="audio-entry" key={asset.id}>
                <div>
                  <strong>{asset.file_name}</strong>
                  <p>{asset.status} • {asset.provider_used} • estimated {asset.duration_seconds}s</p>
                  {asset.provider_notes && <p>{asset.provider_notes}</p>}
                </div>
                <div className="row-meta">
                  <StatusBadge status={asset.status} />
                  {asset.mime_type === 'audio/wav' && (
                    <audio controls src={audioDownloadUrl(id, asset.id)} />
                  )}
                  <a className="button-link small" href={audioDownloadUrl(id, asset.id)}>Download</a>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="card stack">
        <div className="card-header">
          <div>
            <h2>CapCut / manual assembly plan</h2>
            <p className="muted">Generate a scene-by-scene editing timeline for CapCut before full automatic video assembly is ready.</p>
          </div>
          <button onClick={createAssemblyPlan} disabled={assemblyGenerating}>
            {assemblyGenerating ? 'Generating...' : 'Generate assembly plan'}
          </button>
        </div>
        {!data.assembly_plans || data.assembly_plans.length === 0 ? (
          <p className="muted">No assembly plan yet. Generate one after reviewing the script and narration status.</p>
        ) : (
          <div className="assembly-list">
            {data.assembly_plans.map((plan, index) => (
              <div className="assembly-entry" key={plan.id}>
                <div>
                  <strong>Plan #{plan.id}</strong>
                  <p>{plan.scene_count} scenes • {plan.estimated_duration_seconds}s • {plan.assembly_mode}</p>
                  {index === 0 && <p className="muted">Latest plan is included in the export ZIP as capcut_assembly_plan.md.</p>}
                </div>
                <div className="row-meta">
                  <a className="button-link small" href={assemblyDownloadUrl(id, plan.id)}>Download plan</a>
                </div>
              </div>
            ))}
          </div>
        )}
        {data.assembly_plans && data.assembly_plans.length > 0 && (
          <TextCard title="Latest CapCut assembly plan" value={data.assembly_plans[0].plan_markdown} />
        )}
      </div>



      <div className="card stack">
        <div className="card-header">
          <div>
            <h2>Suggested reusable visuals</h2>
            <p className="muted">These assets match this package's topic/script tags and can appear in the MP4 draft scene cards.</p>
          </div>
          <button className="secondary" onClick={() => navigate('#/assets')}>Manage assets</button>
        </div>
        {!data.suggested_visual_assets || data.suggested_visual_assets.length === 0 ? (
          <p className="muted">No matching assets yet. Upload assets with tags like leaf, chlorophyll, photosynthesis, math, grammar, etc.</p>
        ) : (
          <div className="asset-strip">
            {data.suggested_visual_assets.map((asset) => (
              <div className="asset-mini" key={asset.id}>
                <img src={visualAssetUrl(asset.id)} alt={asset.title} />
                <div>
                  <strong>{asset.title}</strong>
                  <span>{asset.tags}</span>
                  <small>match score: {asset.match_score}</small>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="card stack">
        <div className="card-header">
          <div>
            <h2>Vertical MP4 draft</h2>
            <p className="muted">Generate a simple 9:16 review video from scene cards. Replace these cards with final visuals later in CapCut.</p>
          </div>
          <button onClick={createVideoDraft} disabled={videoDraftGenerating}>
            {videoDraftGenerating ? 'Generating...' : 'Generate video draft'}
          </button>
        </div>
        {!data.video_drafts || data.video_drafts.length === 0 ? (
          <p className="muted">No video draft yet. Generate one after reviewing the script, narration, and assembly plan.</p>
        ) : (
          <div className="video-draft-list">
            {data.video_drafts.map((draft) => (
              <div className="video-draft-entry" key={draft.id}>
                <div>
                  <strong>{draft.file_name}</strong>
                  <p>{draft.status} • {draft.draft_mode} • {draft.duration_seconds}s • {draft.scene_count} scenes</p>
                  {draft.provider_notes && <p>{draft.provider_notes}</p>}
                </div>
                <div className="row-meta">
                  <StatusBadge status={draft.status} />
                  {draft.mime_type === 'video/mp4' && (
                    <video controls width="220" src={videoDraftDownloadUrl(id, draft.id)} />
                  )}
                  <a className="button-link small" href={videoDraftDownloadUrl(id, draft.id)}>Download</a>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="detail-grid">
        <TextCard title="Storyboard" value={pkg.storyboard_markdown} />
        <TextCard title="Visual prompts" value={pkg.visual_prompts_markdown} />
        <TextCard title="Subtitles (.srt)" value={pkg.subtitle_srt} />
      </div>

      <div className="card stack">
        <h2>Manual analytics</h2>
        <form className="analytics-grid" onSubmit={saveAnalytics}>
          <Input label="Platform" value={analytics.platform} onChange={(v) => setAnalytics({ ...analytics, platform: v })} />
          <Input type="date" label="Entry date" value={analytics.entry_date} onChange={(v) => setAnalytics({ ...analytics, entry_date: v })} />
          <Input type="number" label="Views" value={analytics.views} onChange={(v) => setAnalytics({ ...analytics, views: v })} />
          <Input type="number" label="Likes" value={analytics.likes} onChange={(v) => setAnalytics({ ...analytics, likes: v })} />
          <Input type="number" label="Comments" value={analytics.comments} onChange={(v) => setAnalytics({ ...analytics, comments: v })} />
          <Input type="number" label="Shares" value={analytics.shares} onChange={(v) => setAnalytics({ ...analytics, shares: v })} />
          <Input type="number" label="Avg view seconds" value={analytics.avg_view_duration_seconds} onChange={(v) => setAnalytics({ ...analytics, avg_view_duration_seconds: v })} />
          <Input type="number" label="Retention %" value={analytics.retention_pct} onChange={(v) => setAnalytics({ ...analytics, retention_pct: v })} />
          <Input type="number" label="CTR %" value={analytics.ctr_pct} onChange={(v) => setAnalytics({ ...analytics, ctr_pct: v })} />
          <TextArea label="Notes" value={analytics.notes} onChange={(v) => setAnalytics({ ...analytics, notes: v })} rows={3} wide />
          <div className="wide"><button type="submit">Save analytics</button></div>
        </form>

        <div className="analytics-list">
          {data.analytics.length === 0 ? <p className="muted">No analytics entered yet.</p> : data.analytics.map((entry) => (
            <div className="analytics-entry" key={entry.id}>
              <strong>{entry.entry_date} • {entry.platform}</strong>
              <span>{entry.views} views • {entry.likes} likes • {entry.retention_pct}% retention</span>
              {entry.notes && <p>{entry.notes}</p>}
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}


function AnalyticsInsightsPage() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  function load() {
    setError('')
    fetchAnalyticsInsights().then(setData).catch((err) => setError(err.message))
  }

  useEffect(load, [])

  function downloadReport() {
    if (!data?.report_markdown) return
    const blob = new Blob([data.report_markdown], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'analytics_dashboard_insights.md'
    document.body.appendChild(link)
    link.click()
    link.remove()
    URL.revokeObjectURL(url)
  }

  if (error) return <ErrorCard title="Could not load analytics insights" message={error} />
  if (!data) return <Loading />

  const totals = data.totals || {}

  return (
    <section>
      <Header
        title="Analytics dashboard insights"
        subtitle="Turn manual YouTube Shorts analytics into practical decisions: best videos, weak videos, best tone/template/batch, weekly summary, and next actions."
        action={<button onClick={downloadReport}>Download report</button>}
      />

      {totals.total_entries === 0 ? (
        <div className="card stack">
          <h2>No analytics yet</h2>
          <p className="muted">Open a published package and enter views, retention, likes, comments, shares, CTR, and notes. After a few entries, this page will show what is working.</p>
          <button onClick={() => navigate('#/')}>Go to dashboard</button>
        </div>
      ) : (
        <>
          <div className="stats-grid analytics-stats-grid">
            <StatCard label="Packages tracked" value={totals.packages_with_analytics} />
            <StatCard label="Latest total views" value={totals.total_latest_views} />
            <StatCard label="Avg retention %" value={totals.avg_retention_pct} />
            <StatCard label="Engagement rate %" value={totals.engagement_rate_pct} />
            <StatCard label="Avg CTR %" value={totals.avg_ctr_pct} />
            <StatCard label="Avg views/package" value={totals.avg_views_per_package} />
          </div>

          {!data.has_enough_data && (
            <div className="form-error soft-warning">
              You have useful early data, but not enough for strong conclusions yet. Try to collect analytics from at least 10–20 Shorts before locking the content formula.
            </div>
          )}

          <div className="card stack">
            <div className="card-header"><h2>Recommended next actions</h2><span>{data.recommendations.length} suggestions</span></div>
            <ul className="recommendation-list">
              {data.recommendations.map((item) => <li key={item}>{item}</li>)}
            </ul>
          </div>

          <div className="detail-grid">
            <VideoRanking title="Top videos by views" videos={data.top_videos_by_views} metric="views" />
            <VideoRanking title="Top videos by retention" videos={data.top_videos_by_retention} metric="retention_pct" suffix="%" />
          </div>

          <div className="card stack">
            <div className="card-header"><h2>Weak videos to improve</h2><span>{data.weak_videos.length} items</span></div>
            {data.weak_videos.length === 0 ? (
              <p className="muted">No weak videos detected yet, or not enough analytics data. Keep entering weekly numbers.</p>
            ) : (
              <div className="package-list compact">
                {data.weak_videos.map((item) => (
                  <button key={item.package_id} className="package-row" onClick={() => navigate(`#/packages/${item.package_id}`)}>
                    <div>
                      <h3>{item.topic}</h3>
                      <p>{item.views} views • {item.retention_pct}% retention • {item.engagement_rate_pct}% engagement</p>
                      <p>{item.tone} • {item.prompt_template_name} • {item.batch_name}</p>
                    </div>
                    <div className="row-meta"><StatusBadge status={item.review_status} /><TrustBadge score={item.trust_score} /></div>
                  </button>
                ))}
              </div>
            )}
          </div>

          <div className="detail-grid">
            <PerformanceTable title="Tone performance" rows={data.grouped.tones} />
            <PerformanceTable title="Prompt template performance" rows={data.grouped.templates} />
            <PerformanceTable title="Subject performance" rows={data.grouped.subjects} />
            <PerformanceTable title="Batch performance" rows={data.grouped.batches} />
          </div>

          <WeeklySummary rows={data.weekly_summary} />
          <TextCard title="Analytics report markdown" value={data.report_markdown} />
        </>
      )}
    </section>
  )
}

function VideoRanking({ title, videos = [], metric, suffix = '' }) {
  return (
    <div className="card stack">
      <div className="card-header"><h2>{title}</h2><span>{videos.length} items</span></div>
      {videos.length === 0 ? <p className="muted">No videos yet.</p> : (
        <div className="insight-list">
          {videos.map((item, index) => (
            <button key={`${title}-${item.package_id}`} className="insight-row" onClick={() => navigate(`#/packages/${item.package_id}`)}>
              <span className="rank-number">#{index + 1}</span>
              <div>
                <strong>{item.topic}</strong>
                <p>{item.views} views • {item.retention_pct}% retention • {item.engagement_rate_pct}% engagement</p>
                <p>{item.tone} • {item.prompt_template_name} • {item.batch_name}</p>
              </div>
              <strong>{item[metric]}{suffix}</strong>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

function PerformanceTable({ title, rows = [] }) {
  return (
    <div className="card stack">
      <div className="card-header"><h2>{title}</h2><span>{rows.length} groups</span></div>
      {rows.length === 0 ? <p className="muted">No grouped analytics yet.</p> : (
        <div className="performance-table">
          <div className="performance-head"><span>Name</span><span>Videos</span><span>Views</span><span>Retention</span></div>
          {rows.map((row) => (
            <div className="performance-row" key={`${title}-${row.name}`}>
              <strong>{row.name}</strong>
              <span>{row.count}</span>
              <span>{row.total_views}</span>
              <span>{row.avg_retention_pct}%</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

function WeeklySummary({ rows = [] }) {
  return (
    <div className="card stack">
      <div className="card-header"><h2>Weekly analytics summary</h2><span>{rows.length} weeks</span></div>
      {rows.length === 0 ? <p className="muted">No weekly entries yet.</p> : (
        <div className="performance-table weekly-table">
          <div className="performance-head"><span>Week</span><span>Entries</span><span>Views</span><span>Retention</span><span>CTR</span></div>
          {rows.map((row) => (
            <div className="performance-row" key={row.week}>
              <strong>{row.week}</strong>
              <span>{row.entries}</span>
              <span>{row.total_views}</span>
              <span>{row.avg_retention_pct}%</span>
              <span>{row.avg_ctr_pct}%</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}


function ProviderLogsPage() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchProviderLogs().then(setData).catch((err) => setError(err.message))
  }, [])

  if (error) return <ErrorCard title="Could not load provider logs" message={error} />
  if (!data) return <Loading />

  const summary = data.summary || {}
  const totals = summary.totals || {}
  const providerStats = summary.provider_stats || []
  const recentLogs = summary.recent_logs || []
  const fallbackPackages = summary.fallback_packages || []
  const recommendations = summary.recommendations || []

  return (
    <section>
      <Header
        title="AI provider fallback logs"
        subtitle="See which provider generated each package, why providers failed, and whether template fallback protected the workflow."
        action={<button onClick={() => downloadMarkdown('ai_provider_fallback_report.md', summary.report_markdown || '# AI Provider Report')}>Download report</button>}
      />

      <div className="stats-grid">
        <StatCard label="Provider attempts" value={totals.total_logs || 0} />
        <StatCard label="Packages logged" value={totals.packages_logged || 0} />
        <StatCard label="Successes" value={totals.successes || 0} />
        <StatCard label="Failures" value={totals.failures || 0} />
        <StatCard label="Template fallbacks" value={totals.fallback_to_template_count || 0} />
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Recommended actions</h2><span>{recommendations.length} items</span></div>
        {recommendations.length === 0 ? <p className="muted">No recommendations yet.</p> : (
          <ul className="check-list">
            {recommendations.map((item) => <li key={item}>{item}</li>)}
          </ul>
        )}
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Provider performance</h2><span>{providerStats.length} providers</span></div>
        {providerStats.length === 0 ? <p className="muted">Generate a package to create provider logs.</p> : (
          <div className="performance-table provider-log-table">
            <div className="performance-head"><span>Provider</span><span>Attempts</span><span>Success</span><span>Failures</span><span>Avg ms</span></div>
            {providerStats.map((provider) => (
              <div className="performance-row" key={provider.provider}>
                <strong>{provider.provider}</strong>
                <span>{provider.attempts}</span>
                <span>{provider.success_rate_pct}%</span>
                <span>{provider.failure_count}</span>
                <span>{provider.avg_duration_ms}</span>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Recent provider attempts</h2><span>{recentLogs.length} logs</span></div>
        {recentLogs.length === 0 ? <p className="muted">No attempts logged yet.</p> : (
          <div className="package-list compact-list">
            {recentLogs.slice(0, 30).map((log) => (
              <div className="package-row static" key={log.id}>
                <div>
                  <h3>Package #{log.package_id}: {log.topic || 'Untitled package'}</h3>
                  <p>{log.provider} • attempt {log.attempt_order} • {log.duration_ms} ms</p>
                  <p>{log.message}</p>
                </div>
                <div className="row-meta"><StatusBadge status={log.success ? 'success' : 'failed'} /></div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Packages that used template fallback</h2><span>{fallbackPackages.length} items</span></div>
        {fallbackPackages.length === 0 ? <p className="muted">No failed-AI-to-template fallback packages detected yet.</p> : (
          <div className="package-list compact-list">
            {fallbackPackages.map((item) => (
              <button className="package-row" key={item.id} onClick={() => navigate(`#/packages/${item.id}`)}>
                <div>
                  <h3>{item.topic}</h3>
                  <p>{item.subject} • final provider: {item.provider_used}</p>
                  <p>{item.provider_notes}</p>
                </div>
                <div className="row-meta"><StatusBadge status="template_fallback" /></div>
              </button>
            ))}
          </div>
        )}
      </div>
    </section>
  )
}


function AiSettings() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchAiSettings().then(setData).catch((err) => setError(err.message))
  }, [])

  if (error) return <ErrorCard title="Could not load AI settings" message={error} />
  if (!data) return <Loading />

  return (
    <section>
      <Header title="AI fallback status" subtitle="Ollama and Transformers are optional. Template fallback keeps the app usable on your laptop." />
      <div className="card provider-grid">
        {data.providers.map((provider) => (
          <div className="provider-card" key={provider.name}>
            <div className="provider-top"><h2>{provider.name}</h2><StatusBadge status={provider.available ? 'available' : 'disabled'} /></div>
            <p>{provider.message}</p>
            <span className="muted">In chain: {provider.in_chain ? 'yes' : 'no'}</span>
          </div>
        ))}
      </div>
      <div className="card stack">
        <h2>Recommended laptop setting</h2>
        <pre>{`AI_PROVIDER_CHAIN=transformers,template\nUSE_OLLAMA=false\nUSE_TRANSFORMERS=false`}</pre>
        <p className="muted">Enable Ollama later on your desktop without changing business logic.</p>
        <button className="secondary" onClick={() => navigate('#/provider-logs')}>Open provider fallback logs</button>
      </div>
    </section>
  )
}


function AudioSettings() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchAudioSettings().then(setData).catch((err) => setError(err.message))
  }, [])

  if (error) return <ErrorCard title="Could not load audio settings" message={error} />
  if (!data) return <Loading />

  return (
    <section>
      <Header
        title="Audio fallback status"
        subtitle="Backend narration can use Windows SAPI or pyttsx3 when available. Manual recording fallback always works."
      />
      <div className="card provider-grid">
        {data.providers.map((provider) => (
          <div className="provider-card" key={provider.name}>
            <div className="provider-top"><h2>{provider.name}</h2><StatusBadge status={provider.available ? 'available' : 'disabled'} /></div>
            <p>{provider.message}</p>
            <span className="muted">Enabled: {provider.enabled ? 'yes' : 'no'} • In chain: {provider.in_chain ? 'yes' : 'no'}</span>
          </div>
        ))}
      </div>
      <div className="card stack">
        <h2>Recommended laptop setting</h2>
        <pre>{`TTS_PROVIDER_CHAIN=windows_sapi,manual_recording
USE_WINDOWS_SAPI_TTS=true
USE_PYTTSX3_TTS=false`}</pre>
        <p className="muted">On Windows, this can use built-in speech. If it fails, the app creates a manual recording guide so publishing does not stop.</p>
      </div>
    </section>
  )
}

function Header({ title, subtitle, action }) {
  return (
    <div className="page-header">
      <div><p className="eyebrow">Edu Content Platform MVP</p><h1>{title}</h1><p>{subtitle}</p></div>
      {action && <div>{action}</div>}
    </div>
  )
}

function StatCard({ label, value }) {
  return <div className="stat-card"><span>{label}</span><strong>{value}</strong></div>
}

function Input({ label, value, onChange, type = 'text', disabled = false }) {
  return <label className="field"><span>{label}</span><input type={type} value={value ?? ''} disabled={disabled} onChange={(event) => onChange(event.target.value)} /></label>
}

function Select({ label, value, options, onChange, disabled = false }) {
  return (
    <label className="field">
      <span>{label}</span>
      <select value={value ?? ''} disabled={disabled} onChange={(event) => onChange(event.target.value)}>
        {options.map((option) => {
          const obj = typeof option === 'string' ? { value: option, label: option } : option
          return <option value={obj.value} key={obj.value}>{obj.label}</option>
        })}
      </select>
    </label>
  )
}

function TextArea({ label, value, onChange, rows = 5, wide = false }) {
  return <label className={`field ${wide ? 'wide' : ''}`}><span>{label}</span><textarea rows={rows} value={value ?? ''} onChange={(event) => onChange(event.target.value)} /></label>
}

function TrustBadge({ score }) {
  const level = score >= 85 ? 'good' : score >= 70 ? 'warn' : 'danger'
  return <span className={`trust-badge ${level}`}>Trust {score}</span>
}

function StatusBadge({ status }) {
  return <span className={`status-badge ${String(status).replaceAll('_', '-')}`}>{status}</span>
}

function InfoBlock({ title, value }) {
  return <div className="info-block"><strong>{title}</strong><p>{value}</p></div>
}

function InfoList({ title, values = [], inline = false }) {
  return (
    <div className="info-block">
      <strong>{title}</strong>
      <div className={inline ? 'pill-list' : 'title-list'}>
        {values.map((value) => inline ? <span key={value}>{value}</span> : <p key={value}>{value}</p>)}
      </div>
    </div>
  )
}

function TextCard({ title, value }) {
  return (
    <div className="card stack">
      <div className="card-header"><h2>{title}</h2><button className="secondary small" onClick={() => copyText(value)}>Copy</button></div>
      <pre>{value}</pre>
    </div>
  )
}

function Loading() {
  return <div className="card loading">Loading...</div>
}

function EmptyState() {
  return <div className="empty-state"><h3>No packages yet</h3><p>Create your first Shorts package using the sample Science topic.</p><button onClick={() => navigate('#/new')}>Create first package</button></div>
}

function ErrorCard({ title, message }) {
  return <div className="card error-card"><h2>{title}</h2><p>{message}</p><p className="muted">Make sure the FastAPI backend is running at http://127.0.0.1:8000.</p></div>
}

async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text)
  } catch (_) {
    // Clipboard may be unavailable on some local/security contexts.
  }
}

function downloadMarkdown(filename, text) {
  const blob = new Blob([text || ''], { type: 'text/markdown;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = filename
  anchor.click()
  URL.revokeObjectURL(url)
}

function speak(text) {
  if (!('speechSynthesis' in window)) return
  window.speechSynthesis.cancel()
  const utterance = new SpeechSynthesisUtterance(text)
  utterance.rate = 1
  window.speechSynthesis.speak(utterance)
}

export default App
