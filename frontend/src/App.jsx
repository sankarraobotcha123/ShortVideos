import { useEffect, useMemo, useState } from 'react'
import {
  addAnalytics,
  exportUrl,
  fetchAiSettings,
  fetchPackage,
  fetchPackages,
  generateContent,
  updateReview
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
  source_name: 'Self-written concept notes',
  source_license_type: 'Self-written / Original',
  page_or_section_reference: '',
  copied_text_used: false,
  source_notes:
    'Leaves contain chlorophyll. Chlorophyll absorbs sunlight and helps plants make food through photosynthesis. Chlorophyll reflects green light, so leaves look green.',
  transformation_notes:
    'Converted source facts into a simple original explanation with analogy, visual scenes, and a student challenge.'
}

const today = () => new Date().toISOString().slice(0, 10)

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
          <a className={route.name === 'settings' ? 'active' : ''} href="#/settings/ai">AI fallback status</a>
          <a href="http://127.0.0.1:8000" target="_blank" rel="noreferrer">Legacy Jinja UI</a>
        </nav>
        <div className="side-note">
          <strong>Current rule</strong>
          <span>Publish useful Shorts first. Add full automation only after the workflow proves value.</span>
        </div>
      </aside>

      <main className="main-area">
        {route.name === 'dashboard' && <Dashboard />}
        {route.name === 'new' && <CreatePackage />}
        {route.name === 'package' && <PackageDetail id={route.id} />}
        {route.name === 'settings' && <AiSettings />}
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
  if (parts[0] === 'settings' && parts[1] === 'ai') return { name: 'settings' }
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
        subtitle="Track generated Shorts packages, review status, and basic production progress."
        action={<button onClick={() => navigate('#/new')}>Create new package</button>}
      />

      <div className="stats-grid">
        <StatCard label="Total packages" value={data.stats.total} />
        <StatCard label="Approved" value={data.stats.approved} />
        <StatCard label="Published" value={data.stats.published} />
        <StatCard label="Avg. trust score" value={data.stats.avg_trust} />
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
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  function update(name, value) {
    setForm((current) => ({ ...current, [name]: value }))
  }

  async function onSubmit(event) {
    event.preventDefault()
    setLoading(true)
    setError('')
    try {
      const result = await generateContent({
        ...form,
        duration_seconds: Number(form.duration_seconds),
        copied_text_used: Boolean(form.copied_text_used)
      })
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
        subtitle="Generate script, storyboard, subtitles, title options, quiz, and review metadata."
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

function PackageDetail({ id }) {
  const [data, setData] = useState(null)
  const [scriptText, setScriptText] = useState('')
  const [reviewStatus, setReviewStatus] = useState('draft')
  const [reviewerNotes, setReviewerNotes] = useState('')
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

  useEffect(() => {
    setData(null)
    fetchPackage(id)
      .then((result) => {
        setData(result)
        setScriptText(result.package.script_text || '')
        setReviewStatus(result.package.review_status || 'draft')
        setReviewerNotes(result.package.reviewer_notes || '')
      })
      .catch((err) => setError(err.message))
  }, [id])

  async function saveReview() {
    setMessage('')
    setError('')
    try {
      const result = await updateReview(id, {
        review_status: reviewStatus,
        script_text: scriptText,
        reviewer_notes: reviewerNotes
      })
      setData((current) => ({ ...current, package: result.package }))
      setMessage('Review saved.')
    } catch (err) {
      setError(err.message)
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
          <div className="card-header">
            <h2>Review</h2>
            <TrustBadge score={pkg.trust_score} />
          </div>
          <Select
            label="Review status"
            value={reviewStatus}
            options={['draft', 'approved', 'edit_required', 'rejected', 'published']}
            onChange={setReviewStatus}
          />
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

      <div className="detail-grid">
        <TextCard title="Storyboard" value={pkg.storyboard_markdown} />
        <TextCard title="Visual prompts" value={pkg.visual_prompts_markdown} />
        <TextCard title="Subtitles (.srt)" value={pkg.subtitle_srt} />
        <div className="card stack">
          <h2>AI provider attempts</h2>
          <p className="muted">The app works without Ollama because the template provider is always available.</p>
          <div className="attempt-list">
            {pkg.provider_attempts_list.length === 0 ? (
              <span className="muted">No provider attempts recorded.</span>
            ) : (
              pkg.provider_attempts_list.map((attempt, index) => (
                <div className="attempt" key={`${attempt.provider}-${index}`}>
                  <strong>{attempt.provider}</strong>
                  <span>{attempt.success ? 'success' : 'skipped/failed'}</span>
                  <p>{attempt.message}</p>
                </div>
              ))
            )}
          </div>
        </div>
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
      <Header
        title="AI fallback status"
        subtitle="Ollama and Transformers are optional. Template fallback keeps the app usable on your laptop."
      />
      <div className="card provider-grid">
        {data.providers.map((provider) => (
          <div className="provider-card" key={provider.name}>
            <div className="provider-top">
              <h2>{provider.name}</h2>
              <StatusBadge status={provider.available ? 'available' : 'disabled'} />
            </div>
            <p>{provider.message}</p>
            <span className="muted">In chain: {provider.in_chain ? 'yes' : 'no'}</span>
          </div>
        ))}
      </div>
      <div className="card stack">
        <h2>Recommended laptop setting</h2>
        <pre>{`AI_PROVIDER_CHAIN=transformers,template\nUSE_OLLAMA=false\nUSE_TRANSFORMERS=false`}</pre>
        <p className="muted">Enable Ollama later on your desktop without changing business logic.</p>
      </div>
    </section>
  )
}

function Header({ title, subtitle, action }) {
  return (
    <div className="page-header">
      <div>
        <p className="eyebrow">Edu Content Platform MVP</p>
        <h1>{title}</h1>
        <p>{subtitle}</p>
      </div>
      {action && <div>{action}</div>}
    </div>
  )
}

function StatCard({ label, value }) {
  return (
    <div className="stat-card">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  )
}

function Input({ label, value, onChange, type = 'text' }) {
  return (
    <label className="field">
      <span>{label}</span>
      <input type={type} value={value} onChange={(event) => onChange(event.target.value)} />
    </label>
  )
}

function Select({ label, value, options, onChange }) {
  return (
    <label className="field">
      <span>{label}</span>
      <select value={value} onChange={(event) => onChange(event.target.value)}>
        {options.map((option) => <option value={option} key={option}>{option}</option>)}
      </select>
    </label>
  )
}

function TextArea({ label, value, onChange, rows = 5, wide = false }) {
  return (
    <label className={`field ${wide ? 'wide' : ''}`}>
      <span>{label}</span>
      <textarea rows={rows} value={value} onChange={(event) => onChange(event.target.value)} />
    </label>
  )
}

function TrustBadge({ score }) {
  const level = score >= 85 ? 'good' : score >= 70 ? 'warn' : 'danger'
  return <span className={`trust-badge ${level}`}>Trust {score}</span>
}

function StatusBadge({ status }) {
  return <span className={`status-badge ${String(status).replaceAll('_', '-')}`}>{status}</span>
}

function InfoBlock({ title, value }) {
  return (
    <div className="info-block">
      <strong>{title}</strong>
      <p>{value}</p>
    </div>
  )
}

function InfoList({ title, values, inline = false }) {
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
      <div className="card-header">
        <h2>{title}</h2>
        <button className="secondary small" onClick={() => copyText(value)}>Copy</button>
      </div>
      <pre>{value}</pre>
    </div>
  )
}

function Loading() {
  return <div className="card loading">Loading...</div>
}

function EmptyState() {
  return (
    <div className="empty-state">
      <h3>No packages yet</h3>
      <p>Create your first Shorts package using the sample Science topic.</p>
      <button onClick={() => navigate('#/new')}>Create first package</button>
    </div>
  )
}

function ErrorCard({ title, message }) {
  return (
    <div className="card error-card">
      <h2>{title}</h2>
      <p>{message}</p>
      <p className="muted">Make sure the FastAPI backend is running at http://127.0.0.1:8000.</p>
    </div>
  )
}

async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text)
  } catch (_) {
    // Clipboard may be unavailable on some local/security contexts.
  }
}

function speak(text) {
  if (!('speechSynthesis' in window)) return
  window.speechSynthesis.cancel()
  const utterance = new SpeechSynthesisUtterance(text)
  utterance.rate = 1
  window.speechSynthesis.speak(utterance)
}

export default App
