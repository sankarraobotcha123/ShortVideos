import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import {
  addAnalytics,
  bulkScheduleCalendar,
  batchHandoffDownloadUrl,
  batchHandoffReportDownloadUrl,
  calendarBulkReportDownloadUrl,
  changeAuthPassword,
  contentIdeasDownloadUrl,
  convertContentIdea,
  createContentIdea,
  createContentSeries,
  createMultilingualPlan,
  createSeriesItem,
  cleanupAuthSessions,
  clearAuthToken,
  createAuthUser,
  audioDownloadUrl,
  assemblyDownloadUrl,
  assignPackageBatch,
  createBatch,
  createBatchHandoff,
  createCalendarEntry,
  deleteCalendarEntry,
  deleteVisualAsset,
  deploymentGuideDownloadUrl,
  finalPolishReportDownloadUrl,
  fetchAuthStatus,
  fetchAuthUsers,
  fetchAuthPermissions,
  fetchAuthHardening,
  exportUrl,
  fetchAiSettings,
  fetchAnalyticsInsights,
  fetchAudioSettings,
  fetchBatch,
  fetchBatches,
  fetchBatchHandoffs,
  fetchCalendar,
  fetchCalendarBulkRuns,
  fetchPackage,
  fetchPackages,
  fetchContentIdeas,
  fetchContentSeries,
  fetchContentSeriesDetail,
  fetchDeploymentGuide,
  fetchFinalPolishReport,
  fetchMultilingualPlans,
  fetchCurrentUser,
  fetchProviderLogs,
  fetchProviderSetupGuide,
  fetchProductionBoard,
  fetchReleaseChecklist,
  fetchSetupGuide,
  fetchSystemReadiness,
  fetchVisualAssets,
  fetchYoutubePublishingChecklist,
  getStoredAuthUser,
  generateAssembly,
  generateAudio,
  generateContent,
  generateSourceSafetyReview,
  generateThumbnailGuide,
  generateTrustReview,
  generateLearningOutput,
  generatePublishingApproval,
  generateVideoDraft,
  loginUser,
  logoutUser,
  thumbnailGuideDownloadUrl,
  sourceSafetyDownloadUrl,
  updatePublishingApproval,
  trustReviewDownloadUrl,
  learningOutputDownloadUrl,
  createPromptTemplate,
  deleteContentIdea,
  deleteContentSeries,
  deleteMultilingualPlan,
  deletePromptTemplate,
  deleteSeriesItem,
  fetchPromptTemplates,
  previewPromptTemplate,
  publishingApprovalDownloadUrl,
  providerSetupGuideDownloadUrl,
  releaseChecklistDownloadUrl,
  setupGuideDownloadUrl,
  productionBoardDownloadUrl,
  contentSeriesDownloadUrl,
  multilingualPlansDownloadUrl,
  youtubePublishingChecklistDownloadUrl,
  seedDemoData,
  seedPromptTemplates,
  updatePromptTemplate,
  updateAuthUser,
  updateContentIdea,
  updateContentSeries,
  updateMultilingualPlan,
  updateSeriesItem,
  updateBatch,
  uploadVisualAsset,
  updateCalendarEntry,
  updateProductionCard,
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

const initialBulkCalendar = {
  start_date: today(),
  batch_id: '',
  limit: 20,
  videos_per_day: 1,
  days_between: 0,
  platform: 'YouTube Shorts',
  playlist_name: 'Science Curiosity Shorts',
  status: 'planned',
  order_by: 'created_at',
  created_by: '',
  apply: false
}

const initialBatchHandoff = {
  handoff_name: 'Science Shorts Production Handoff',
  batch_id: '',
  ready_only: true,
  limit_count: 50,
  created_by: '',
  notes: 'Export ready packages for CapCut/Canva editing and publisher handoff.'
}

const initialVisualAsset = {
  title: 'Leaf chlorophyll diagram',
  tags: 'leaf, chlorophyll, photosynthesis, science',
  description: 'Simple reusable visual for explaining why leaves look green.',
  source_type: 'self_created',
  license_type: 'Self-created / Original',
  notes: 'Use for Class 6-8 science Shorts about plants.'
}

const initialPromptTemplate = {
  name: 'Custom Curiosity Short Script',
  task_type: 'script',
  style_key: 'custom_curiosity',
  active: true,
  notes: 'Use this for a 30-60 second educational Short with a strong hook and simple explanation.',
  template_text: `{hook}

{simple_meaning}

Example: {analogy}

Remember: {memory_line}

Quick challenge: explain {topic_lower} in one sentence.`
}


const initialContentIdea = {
  title: 'Why do we see lightning before thunder?',
  subject: 'Science',
  class_level: 'Class 7',
  target_audience: 'School students and curious learners',
  language: 'English',
  idea_type: 'curiosity',
  hook_angle: 'Most students think lightning and thunder happen at different times, but the real reason is speed.',
  source_hint: 'Light travels much faster than sound, so lightning reaches our eyes before thunder reaches our ears.',
  batch_id: '',
  status: 'backlog',
  notes: 'Good visual idea with sky, flash, and sound wave timing.',
  curiosity_score: 9,
  evergreen_score: 8,
  visual_potential_score: 9,
  student_value_score: 8,
  production_effort_score: 4,
  monetization_potential_score: 6
}


const initialMultilingualPlan = {
  package_id: '',
  source_language: 'English',
  target_language: 'Hindi',
  status: 'planning',
  priority: 'medium',
  translation_goal: 'Make this Short understandable for local-language students without changing the meaning.',
  cultural_notes: 'Use simple local examples and avoid word-for-word textbook translation.',
  glossary_terms: 'photosynthesis = process plants use to make food; chlorophyll = green pigment in leaves',
  voice_strategy: 'manual_voice',
  subtitle_strategy: 'manual_review',
  reviewer_name: '',
  notes: 'Plan translation first. Publish only after human language review.',
  needs_human_translation_review: true
}

const initialContentSeries = {
  title: 'Why does nature work like this?',
  niche: 'Class 6-8 Science curiosity Shorts',
  target_audience: 'School students and curious learners',
  subject: 'Science',
  class_level: 'Class 7',
  language: 'English',
  series_goal: 'Create a connected set of curiosity Shorts that makes students watch the next episode.',
  status: 'planning',
  planned_count: 10,
  episode_style: 'Curiosity hook → simple explanation → next-video question',
  cta_strategy: 'End each Short with a question that naturally leads to the next episode.',
  notes: 'Use this to group related Shorts instead of posting random one-off videos.'
}

const initialSeriesItem = {
  idea_id: '',
  package_id: '',
  order_index: 1,
  episode_title: 'Why are leaves green?',
  hook_angle: 'Start with a simple thing students see every day and reveal the hidden science behind it.',
  target_status: 'planned',
  notes: 'Keep episode connected to the series goal.'
}

const initialPublishingApprovalDecision = {
  reviewer_decision: 'pending',
  reviewer_name: '',
  reviewer_notes: ''
}

const ACTION_LABELS = {
  'content:view': 'view content packages',
  'content:create': 'create packages and batches',
  'content:edit': 'edit packages and batches',
  'content:review': 'review and approve scripts',
  'content:publish': 'export publish packages',
  'assets:manage': 'manage visual assets',
  'templates:manage': 'manage prompt templates',
  'analytics:view': 'view analytics',
  'analytics:manage': 'enter analytics',
  'calendar:manage': 'manage publishing calendar',
  'calendar:bulk_schedule': 'bulk schedule publishing calendar',
  'source_safety:review': 'run source safety reviews',
  'trust_score:review': 'run teacher trust reviews',
  'thumbnail:generate': 'generate thumbnail guides',
  'video:generate': 'generate assembly plans and video drafts',
  'audio:generate': 'generate narration audio',
  'learning_outputs:generate': 'generate notes, quizzes, and worksheets',
  'ideas:manage': 'manage content ideas and topic scoring',
  'series:manage': 'manage content series plans',
  'multilingual:manage': 'manage multilingual planning',
  'publish:approve': 'approve publishing gates'
}

const ROUTE_ACCESS = {
  dashboard: { permission: 'content:view' },
  new: { permission: 'content:create' },
  package: { permission: 'content:view' },
  batches: { permission: 'content:view' },
  batch: { permission: 'content:view' },
  calendar: { permission: 'content:view' },
  bulkCalendar: { permission: 'content:view' },
  handoff: { permission: 'content:view' },
  productionBoard: { permission: 'content:view' },
  ideas: { permission: 'content:view' },
  series: { permission: 'content:view' },
  seriesDetail: { permission: 'content:view' },
  multilingual: { permission: 'content:view' },
  assets: { permission: 'content:view' },
  templates: { permission: 'templates:manage' },
  analytics: { permission: 'analytics:view' },
  providerLogs: { permission: 'analytics:view' },
  providerSetup: { permission: 'content:view' },
  youtubePublishing: { permission: 'content:view' },
  deployment: { permission: 'content:view' },
  finalPolish: { permission: 'content:view' },
  demo: { permission: 'content:create' },
  users: { role: 'super_admin' },
  authHardening: { role: 'super_admin' }
}

const AuthContext = createContext({ user: null, status: null })

function useAuthContext() {
  return useContext(AuthContext)
}

function canUsePermission(user, status, permission) {
  if (!permission) return true
  if (status && status.auth_required === false) return true
  if (!user) return false
  const permissions = user.permissions || []
  return permissions.includes('*') || permissions.includes(permission)
}

function useCan(permission) {
  const { user, status } = useAuthContext()
  return canUsePermission(user, status, permission)
}

function permissionLabel(permission) {
  return ACTION_LABELS[permission] || permission
}

function PermissionNotice({ permission, compact = false }) {
  const { user, status } = useAuthContext()
  const allowed = canUsePermission(user, status, permission)
  if (allowed) return null
  return (
    <div className={`permission-banner ${compact ? 'compact' : ''}`}>
      <strong>Permission needed</strong>
      <span>This action requires permission to {permissionLabel(permission)}.</span>
      {!user && <span>Login with a role that has this permission, or keep AUTH_REQUIRED=false during local solo development.</span>}
      {user && <span>Your current role is <strong>{user.role.replaceAll('_', ' ')}</strong>.</span>}
    </div>
  )
}

function GuardedButton({ permission, children, disabled = false, className = '', ...props }) {
  const allowed = useCan(permission)
  const locked = !allowed
  return (
    <button
      {...props}
      className={`${className} ${locked ? 'locked-action' : ''}`.trim()}
      disabled={disabled || locked}
      title={locked ? `Requires permission to ${permissionLabel(permission)}` : props.title}
    >
      {locked ? '🔒 ' : ''}{children}
    </button>
  )
}

function GuardedLink({ permission, children, className = '', href, ...props }) {
  const allowed = useCan(permission)
  if (!allowed) {
    return <span className={`${className} locked-link`.trim()} title={`Requires permission to ${permissionLabel(permission)}`}>🔒 {children}</span>
  }
  return <a className={className} href={href} {...props}>{children}</a>
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


function routeDisplayName(route) {
  const labels = {
    dashboard: 'Dashboard',
    new: 'Create package',
    package: 'Package detail',
    batches: 'Batches',
    batch: 'Batch detail',
    calendar: 'Calendar',
    bulkCalendar: 'Bulk schedule',
    handoff: 'Batch handoff',
    productionBoard: 'Production board',
    ideas: 'Idea backlog',
    series: 'Series planner',
    seriesDetail: 'Series detail',
    multilingual: 'Multilingual plans',
    assets: 'Visual assets',
    templates: 'Prompt templates',
    analytics: 'Analytics insights',
    providerLogs: 'Provider logs',
    providerSetup: 'Provider setup guide',
    youtubePublishing: 'YouTube publishing',
    deployment: 'Deployment guide',
    finalPolish: 'Final MVP polish',
    demo: 'MVP demo setup',
    release: 'Release checklist',
    setup: 'Fresh clone setup',
    permissions: 'Permissions',
    authHardening: 'Auth hardening',
    users: 'Users & roles',
    login: 'Account / Login',
    settings: 'AI fallback status',
    audioSettings: 'Audio fallback status'
  }
  return labels[route.name] || 'Dashboard'
}

function NavItem({ route, active, href, children }) {
  return <a className={active ? 'active' : ''} aria-current={active ? 'page' : undefined} href={href}><span>{children}</span>{active && <em>Current</em>}</a>
}

function App() {
  const hash = useHashRoute()
  const route = useMemo(() => parseRoute(hash), [hash])
  const [authUser, setAuthUser] = useState(getStoredAuthUser())
  const [authStatus, setAuthStatus] = useState(null)
  const authValue = useMemo(() => ({ user: authUser, status: authStatus }), [authUser, authStatus])
  const navCan = (permission) => canUsePermission(authUser, authStatus, permission)

  useEffect(() => {
    fetchAuthStatus().then(setAuthStatus).catch(() => setAuthStatus(null))
    fetchCurrentUser().then((data) => setAuthUser(data.user || null)).catch(() => setAuthUser(null))
    const onExpired = () => {
      setAuthUser(null)
      if (window.location.hash !== '#/login') navigate('#/login')
    }
    window.addEventListener('auth:expired', onExpired)
    return () => window.removeEventListener('auth:expired', onExpired)
  }, [])

  async function handleLogout() {
    try {
      await logoutUser()
    } catch (_) {
      clearAuthToken()
    }
    setAuthUser(null)
    navigate('#/login')
  }

  return (
    <AuthContext.Provider value={authValue}>
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-block">
          <div className="brand-mark">Edu</div>
          <div>
            <h1>Shorts Creator</h1>
            <p>React frontend + FastAPI backend</p>
          </div>
        </div>
        <div className="current-page-chip"><span>Current page</span><strong>{routeDisplayName(route)}</strong></div>
        <nav className="side-nav" aria-label="Primary navigation">
          <div className="nav-section-title">Create</div>
          <NavItem route={route} active={route.name === 'dashboard'} href="#/">Dashboard</NavItem>
          {navCan('content:create') && <NavItem route={route} active={route.name === 'new'} href="#/new">Create package</NavItem>}
          {navCan('content:view') && <NavItem route={route} active={route.name === 'batches' || route.name === 'batch'} href="#/batches">Batches</NavItem>}
          {navCan('content:view') && <NavItem route={route} active={route.name === 'calendar'} href="#/calendar">Calendar</NavItem>}
          {navCan('content:view') && <NavItem route={route} active={route.name === 'bulkCalendar'} href="#/calendar/bulk">Bulk schedule</NavItem>}
          {navCan('content:view') && <NavItem route={route} active={route.name === 'handoff'} href="#/handoff">Batch handoff</NavItem>}
          {navCan('content:view') && <NavItem route={route} active={route.name === 'productionBoard'} href="#/production-board">Production board</NavItem>}
          {navCan('content:view') && <NavItem route={route} active={route.name === 'ideas'} href="#/ideas">Idea backlog</NavItem>}
          {navCan('content:view') && <NavItem route={route} active={route.name === 'series' || route.name === 'seriesDetail'} href="#/series">Series planner</NavItem>}
          {navCan('content:view') && <NavItem route={route} active={route.name === 'multilingual'} href="#/multilingual">Multilingual plans</NavItem>}
          {navCan('content:view') && <NavItem route={route} active={route.name === 'assets'} href="#/assets">Visual assets</NavItem>}
          {navCan('templates:manage') && <NavItem route={route} active={route.name === 'templates'} href="#/templates">Prompt templates</NavItem>}

          <div className="nav-section-title">Review</div>
          {navCan('analytics:view') && <NavItem route={route} active={route.name === 'analytics'} href="#/analytics">Analytics insights</NavItem>}
          {navCan('analytics:view') && <NavItem route={route} active={route.name === 'providerLogs'} href="#/provider-logs">Provider logs</NavItem>}
          {navCan('content:view') && <NavItem route={route} active={route.name === 'providerSetup'} href="#/provider-setup">Provider setup guide</NavItem>}
          {navCan('content:view') && <NavItem route={route} active={route.name === 'youtubePublishing'} href="#/youtube-publishing">YouTube publishing</NavItem>}
          <NavItem route={route} active={route.name === 'settings'} href="#/settings/ai">AI fallback status</NavItem>
          <NavItem route={route} active={route.name === 'audioSettings'} href="#/settings/audio">Audio fallback status</NavItem>

          <div className="nav-section-title">System</div>
          {navCan('content:create') && <NavItem route={route} active={route.name === 'demo'} href="#/demo">MVP demo setup</NavItem>}
          {navCan('content:view') && <NavItem route={route} active={route.name === 'deployment'} href="#/deployment">Deployment guide</NavItem>}
          {navCan('content:view') && <NavItem route={route} active={route.name === 'finalPolish'} href="#/final-polish">Final MVP polish</NavItem>}
          <NavItem route={route} active={route.name === 'release'} href="#/release">Release checklist</NavItem>
          <NavItem route={route} active={route.name === 'setup'} href="#/setup">Fresh clone setup</NavItem>
          <NavItem route={route} active={route.name === 'permissions'} href="#/permissions">Permissions</NavItem>
          {authUser?.role === 'super_admin' && <NavItem route={route} active={route.name === 'authHardening'} href="#/auth-hardening">Auth hardening</NavItem>}
          {authUser?.role === 'super_admin' && <NavItem route={route} active={route.name === 'users'} href="#/users">Users & roles</NavItem>}
          <NavItem route={route} active={route.name === 'login'} href="#/login">{authUser ? 'Account' : 'Login'}</NavItem>
          <a href="http://127.0.0.1:8000" target="_blank" rel="noreferrer">Legacy Jinja UI</a>
        </nav>
        <div className="side-note">
          <strong>{authUser ? `Signed in: ${authUser.name}` : 'Local MVP mode'}</strong>
          <span>{authUser ? `${authUser.role.replaceAll('_', ' ')}` : 'Login is available, but local auth enforcement can stay disabled while building.'}</span>
          {authUser && <button className="secondary small full-width" onClick={handleLogout}>Logout</button>}
          <strong>Current rule</strong>
          <span>Plan 20-30 Shorts as batches. Publish consistently. Automate only after the workflow proves value.</span>
        </div>
      </aside>

      <main className="main-area">
        <RouteGate route={route}>
          {route.name === 'dashboard' && <Dashboard />}
          {route.name === 'new' && <CreatePackage />}
          {route.name === 'package' && <PackageDetail id={route.id} />}
          {route.name === 'batches' && <BatchesPage />}
          {route.name === 'batch' && <BatchDetail id={route.id} />}
          {route.name === 'calendar' && <CalendarPage />}
          {route.name === 'bulkCalendar' && <BulkScheduleCalendarPage />}
          {route.name === 'handoff' && <BatchHandoffPage />}
          {route.name === 'productionBoard' && <ProductionBoardPage />}
          {route.name === 'ideas' && <ContentIdeaBacklogPage />}
          {route.name === 'series' && <ContentSeriesPlannerPage />}
          {route.name === 'seriesDetail' && <ContentSeriesDetailPage id={route.id} />}
          {route.name === 'multilingual' && <MultilingualPlansPage />}
          {route.name === 'assets' && <VisualAssetsPage />}
          {route.name === 'templates' && <PromptTemplatesPage />}
          {route.name === 'analytics' && <AnalyticsInsightsPage />}
          {route.name === 'providerLogs' && <ProviderLogsPage />}
          {route.name === 'providerSetup' && <ProviderSetupGuidePage />}
          {route.name === 'youtubePublishing' && <YoutubePublishingChecklistPage />}
          {route.name === 'demo' && <DemoSetupPage />}
          {route.name === 'deployment' && <DeploymentGuidePage />}
          {route.name === 'finalPolish' && <FinalPolishPage />}
          {route.name === 'release' && <ReleaseChecklistPage />}
          {route.name === 'setup' && <FreshCloneSetupPage />}
          {route.name === 'login' && <LoginPage authUser={authUser} authStatus={authStatus} onLogin={setAuthUser} onLogout={handleLogout} />}
          {route.name === 'users' && <UserManagementPage currentUser={authUser} />}
          {route.name === 'authHardening' && <AuthHardeningPage />}
          {route.name === 'permissions' && <PermissionMatrixPage authStatus={authStatus} authUser={authUser} />}
          {route.name === 'settings' && <AiSettings />}
          {route.name === 'audioSettings' && <AudioSettings />}
        </RouteGate>
      </main>
    </div>
    </AuthContext.Provider>
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
  if (parts[0] === 'calendar' && parts[1] === 'bulk') return { name: 'bulkCalendar' }
  if (parts[0] === 'calendar') return { name: 'calendar' }
  if (parts[0] === 'handoff') return { name: 'handoff' }
  if (parts[0] === 'production-board') return { name: 'productionBoard' }
  if (parts[0] === 'ideas') return { name: 'ideas' }
  if (parts[0] === 'series' && parts[1]) return { name: 'seriesDetail', id: parts[1] }
  if (parts[0] === 'series') return { name: 'series' }
  if (parts[0] === 'multilingual') return { name: 'multilingual' }
  if (parts[0] === 'assets') return { name: 'assets' }
  if (parts[0] === 'templates') return { name: 'templates' }
  if (parts[0] === 'analytics') return { name: 'analytics' }
  if (parts[0] === 'provider-logs') return { name: 'providerLogs' }
  if (parts[0] === 'provider-setup') return { name: 'providerSetup' }
  if (parts[0] === 'youtube-publishing') return { name: 'youtubePublishing' }
  if (parts[0] === 'demo') return { name: 'demo' }
  if (parts[0] === 'deployment') return { name: 'deployment' }
  if (parts[0] === 'final-polish') return { name: 'finalPolish' }
  if (parts[0] === 'release') return { name: 'release' }
  if (parts[0] === 'setup') return { name: 'setup' }
  if (parts[0] === 'login') return { name: 'login' }
  if (parts[0] === 'users') return { name: 'users' }
  if (parts[0] === 'auth-hardening') return { name: 'authHardening' }
  if (parts[0] === 'permissions') return { name: 'permissions' }
  if (parts[0] === 'settings' && parts[1] === 'ai') return { name: 'settings' }
  if (parts[0] === 'settings' && parts[1] === 'audio') return { name: 'audioSettings' }
  return { name: 'dashboard' }
}

function routeAccessRule(route) {
  return ROUTE_ACCESS[route.name] || null
}

function RouteGate({ route, children }) {
  const { user, status } = useAuthContext()
  const rule = routeAccessRule(route)

  if (!rule || route.name === 'login') return children
  if (status === null) return <Loading />
  if (status && status.auth_required === false) return children

  if (!user) {
    return (
      <ErrorCard
        title="Login required"
        message="This page is protected when AUTH_REQUIRED=true. Login with a role that has access to continue."
        action={<button onClick={() => navigate('#/login')}>Go to login</button>}
      />
    )
  }

  if (rule.role && user.role !== rule.role) {
    return (
      <ErrorCard
        title="Role required"
        message={`This page requires the ${rule.role.replaceAll('_', ' ')} role. Your current role is ${user.role.replaceAll('_', ' ')}.`}
        action={<button className="secondary" onClick={() => navigate('#/permissions')}>View permissions</button>}
      />
    )
  }

  if (rule.permission && !canUsePermission(user, status, rule.permission)) {
    return (
      <ErrorCard
        title="Permission required"
        message={`This page requires permission to ${permissionLabel(rule.permission)}.`}
        action={<button className="secondary" onClick={() => navigate('#/permissions')}>View permissions</button>}
      />
    )
  }

  return children
}

function LoginPage({ authUser, authStatus, onLogin, onLogout }) {
  const [form, setForm] = useState({ email: authStatus?.default_admin_email || 'admin@example.com', password: '' })
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (authStatus?.default_admin_email && !authUser) {
      setForm((current) => ({ ...current, email: authStatus.default_admin_email }))
    }
  }, [authStatus, authUser])

  async function submit(event) {
    event.preventDefault()
    setBusy(true)
    setError('')
    try {
      const data = await loginUser(form)
      onLogin(data.user)
      navigate('#/')
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  if (authUser) {
    return (
      <section>
        <Header
          title="Account"
          subtitle="You are signed in to the local role-based MVP foundation. Use this to test reviewer/admin workflows before enabling strict auth."
        />
        <div className="card stack">
          <InfoBlock title="Name" value={authUser.name} />
          <InfoBlock title="Email" value={authUser.email} />
          <InfoBlock title="Role" value={authUser.role.replaceAll('_', ' ')} />
          <InfoList title="Permissions" values={authUser.permissions || []} inline />
          <div className="button-row">
            {authUser.role === 'super_admin' && <button onClick={() => navigate('#/users')}>Manage users</button>}
            <button className="secondary" onClick={onLogout}>Logout</button>
          </div>
        </div>
      </section>
    )
  }

  return (
    <section>
      <Header
        title="Login"
        subtitle="Default local admin is created when the database has no users. Change the default password in your local .env before using this outside local testing."
      />
      <form className="card form-grid" onSubmit={submit}>
        <Input label="Email" value={form.email} onChange={(value) => setForm({ ...form, email: value })} />
        <Input label="Password" type="password" value={form.password} onChange={(value) => setForm({ ...form, password: value })} />
        {error && <p className="error-text wide">{error}</p>}
        <div className="wide button-row">
          <button disabled={busy}>{busy ? 'Logging in...' : 'Login'}</button>
          <button type="button" className="secondary" onClick={() => setForm({ email: authStatus?.default_admin_email || 'admin@example.com', password: 'ChangeMe123!' })}>Fill local sample password</button>
        </div>
      </form>
      <div className="card stack">
        <h2>Auth foundation status</h2>
        <InfoBlock title="Auth required" value={String(Boolean(authStatus?.auth_required))} />
        <InfoBlock title="Default admin email" value={authStatus?.default_admin_email || 'admin@example.com'} />
        <p className="muted">For now, AUTH_REQUIRED can stay false while you build. Before strict testing, change the sample password and review the Auth hardening page.</p>
      </div>
    </section>
  )
}


function PermissionMatrixPage({ authStatus, authUser }) {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchAuthPermissions().then(setData).catch((err) => setError(err.message))
  }, [])

  if (error) return <ErrorCard title="Could not load permissions" message={error} />
  if (!data) return <Loading />

  return (
    <section>
      <Header
        title="Role permissions"
        subtitle="This shows which roles can use sensitive creator workflows. AUTH_REQUIRED=false keeps local development permissive; AUTH_REQUIRED=true enforces these permissions on protected API actions."
      />
      <div className="card stack">
        <InfoBlock title="Auth enforcement" value={data.auth_required ? 'Strict mode enabled' : 'Local MVP permissive mode'} />
        <InfoBlock title="Current user" value={authUser ? `${authUser.name} (${authUser.role})` : 'Not signed in'} />
        {!data.auth_required && <p className="muted">Local MVP mode allows protected creator actions without blocking development. Login still works, and strict enforcement can be enabled later through AUTH_REQUIRED=true.</p>}
        <div className="current-permission-grid">
          {Object.entries(ACTION_LABELS).map(([permission, label]) => {
            const allowed = canUsePermission(authUser, data, permission)
            return (
              <div className={`permission-card ${allowed ? 'allowed' : 'blocked'}`} key={permission}>
                <strong>{allowed ? 'Allowed' : 'Blocked'}: {label}</strong>
                <span>{permission}</span>
              </div>
            )
          })}
        </div>
      </div>
      <div className="card">
        <div className="card-header"><h2>Permission matrix</h2><span>{data.roles.length} roles</span></div>
        <div className="table-wrap">
          <table>
            <thead><tr><th>Role</th><th>Permissions</th></tr></thead>
            <tbody>
              {data.roles.map((role) => (
                <tr key={role.role}>
                  <td><strong>{role.role.replaceAll('_', ' ')}</strong></td>
                  <td><div className="pill-list">{role.permissions.map((permission) => <span key={permission}>{permission}</span>)}</div></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <div className="card stack">
        <h2>Strict mode test</h2>
        <p className="muted">When you are ready to test real permissions, set this in your local .env and restart FastAPI:</p>
        <pre>{`AUTH_REQUIRED=true`}</pre>
        <p className="muted">Then login as different roles and confirm create/review/publish actions are blocked or allowed correctly.</p>
      </div>
    </section>
  )
}

function AuthHardeningPage() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const [passwordForm, setPasswordForm] = useState({ current_password: '', new_password: '' })
  const [message, setMessage] = useState('')

  function load() {
    setError('')
    fetchAuthHardening().then(setData).catch((err) => setError(err.message))
  }

  useEffect(() => {
    load()
  }, [])

  async function cleanupSessions() {
    setBusy(true)
    setMessage('')
    setError('')
    try {
      const result = await cleanupAuthSessions()
      setMessage(`Revoked ${result.revoked_expired_sessions || 0} expired sessions.`)
      load()
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  async function submitPassword(event) {
    event.preventDefault()
    setBusy(true)
    setMessage('')
    setError('')
    try {
      await changeAuthPassword(passwordForm)
      clearAuthToken()
      setMessage('Password changed. Sessions were revoked. Please login again with the new password.')
      setPasswordForm({ current_password: '', new_password: '' })
      setTimeout(() => navigate('#/login'), 600)
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  if (error && !data) return <ErrorCard title="Could not load auth hardening" message={error} />
  if (!data) return <Loading />

  return (
    <section>
      <Header
        title="Auth hardening"
        subtitle="Check production-style login settings, clean expired sessions, and rotate the local admin password before stricter testing."
      />
      <div className="metric-grid">
        <Metric label="Auth required" value={data.auth_required ? 'Strict' : 'Permissive'} />
        <Metric label="Active sessions" value={data.active_sessions} />
        <Metric label="Users" value={data.users_total} />
        <Metric label="Token TTL" value={`${data.token_ttl_hours}h`} />
      </div>

      <div className="card stack">
        <div className="card-header">
          <h2>Hardening checklist</h2>
          <button className="secondary small" onClick={load}>Refresh</button>
        </div>
        <div className="current-permission-grid">
          {(data.checklist || []).map((item) => (
            <div className={`permission-card ${item.passed ? 'allowed' : 'blocked'}`} key={item.item}>
              <strong>{item.passed ? 'Passed' : 'Needs attention'}</strong>
              <span>{item.item}</span>
            </div>
          ))}
        </div>
        {data.warnings?.length > 0 && (
          <div className="warning-list">
            <h3>Warnings</h3>
            <ul>{data.warnings.map((warning) => <li key={warning}>{warning}</li>)}</ul>
          </div>
        )}
        {data.recommendations?.length > 0 && (
          <div className="warning-list">
            <h3>Recommended fixes</h3>
            <ul>{data.recommendations.map((recommendation) => <li key={recommendation}>{recommendation}</li>)}</ul>
          </div>
        )}
        {message && <p className="success-text">{message}</p>}
        {error && <p className="error-text">{error}</p>}
        <div className="button-row">
          <button className="secondary" disabled={busy} onClick={cleanupSessions}>Clean expired sessions</button>
          <button className="secondary" onClick={() => navigate('#/permissions')}>View permission matrix</button>
        </div>
      </div>

      <form className="card form-grid" onSubmit={submitPassword}>
        <div className="wide">
          <h2>Change current password</h2>
          <p className="muted">After password change, all sessions for this account are revoked. You will need to login again.</p>
        </div>
        <Input label="Current password" type="password" value={passwordForm.current_password} onChange={(value) => setPasswordForm({ ...passwordForm, current_password: value })} />
        <Input label="New password" type="password" value={passwordForm.new_password} onChange={(value) => setPasswordForm({ ...passwordForm, new_password: value })} />
        <div className="wide button-row"><button disabled={busy}>Change password and revoke sessions</button></div>
      </form>

      <div className="card stack">
        <h2>Suggested strict testing settings</h2>
        <pre>{`AUTH_REQUIRED=true\nAUTH_COOKIE_SECURE=false\nAUTH_COOKIE_SAMESITE=lax\nAUTH_TOKEN_TTL_HOURS=24\nAUTH_MAX_ACTIVE_SESSIONS_PER_USER=4`}</pre>
        <p className="muted">Use AUTH_COOKIE_SECURE=true only when serving through HTTPS.</p>
      </div>
    </section>
  )
}

function UserManagementPage({ currentUser }) {
  const [data, setData] = useState(null)
  const [form, setForm] = useState({ name: 'Content Reviewer', email: 'reviewer@example.com', password: 'ChangeMe123!', role: 'script_reviewer', active: true })
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  function load() {
    fetchAuthUsers().then(setData).catch((err) => setError(err.message))
  }

  useEffect(() => {
    load()
  }, [])

  if (!currentUser) {
    return <ErrorCard title="Login required" message="Please login as the local admin before opening user management." />
  }
  if (currentUser.role !== 'super_admin') {
    return <ErrorCard title="Super admin required" message="Only the super admin can create or update users." />
  }

  async function submit(event) {
    event.preventDefault()
    setBusy(true)
    setError('')
    try {
      await createAuthUser(form)
      setForm({ name: '', email: '', password: '', role: 'content_admin', active: true })
      load()
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  async function toggleUser(user) {
    setError('')
    try {
      await updateAuthUser(user.id, { active: !user.active })
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <section>
      <Header title="Users & roles" subtitle="Create reviewers, editors, publishers, and admins for the Shorts workflow." />
      <form className="card form-grid" onSubmit={submit}>
        <Input label="Name" value={form.name} onChange={(value) => setForm({ ...form, name: value })} />
        <Input label="Email" value={form.email} onChange={(value) => setForm({ ...form, email: value })} />
        <Input label="Temporary password" type="password" value={form.password} onChange={(value) => setForm({ ...form, password: value })} />
        <Select label="Role" value={form.role} onChange={(value) => setForm({ ...form, role: value })} options={[
          'super_admin',
          'content_admin',
          'script_reviewer',
          'video_editor',
          'publisher',
          'viewer'
        ]} />
        {error && <p className="error-text wide">{error}</p>}
        <div className="wide button-row"><button disabled={busy}>{busy ? 'Creating...' : 'Create user'}</button></div>
      </form>

      <div className="card">
        <div className="card-header"><h2>Existing users</h2><button className="secondary small" onClick={load}>Refresh</button></div>
        {!data ? <Loading /> : (
          <div className="table-wrap">
            <table>
              <thead><tr><th>Name</th><th>Email</th><th>Role</th><th>Status</th><th>Last login</th><th>Action</th></tr></thead>
              <tbody>
                {data.users.map((user) => (
                  <tr key={user.id}>
                    <td>{user.name}</td>
                    <td>{user.email}</td>
                    <td>{user.role}</td>
                    <td>{user.active ? 'Active' : 'Inactive'}</td>
                    <td>{user.last_login_at || '-'}</td>
                    <td><button className="secondary small" onClick={() => toggleUser(user)}>{user.active ? 'Deactivate' : 'Activate'}</button></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </section>
  )
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
        action={<GuardedButton permission="content:create" onClick={() => navigate('#/new')}>Create new package</GuardedButton>}
      />

      <div className="stats-grid">
        <StatCard label="Total packages" value={data.stats.total} />
        <StatCard label="Published" value={data.stats.published} />
        <StatCard label="Active batches" value={data.stats.active_batches} />
        <StatCard label="Scheduled items" value={data.stats.scheduled_items} />
        <StatCard label="Visual assets" value={data.stats.visual_assets || 0} />
        <StatCard label="Idea backlog" value={data.stats.content_ideas || 0} />
      </div>

      <div className="quick-actions card">
        <GuardedButton permission="content:create" onClick={() => navigate('#/batches')}>Plan a 20-Short batch</GuardedButton>
        <GuardedButton permission="content:view" className="secondary" onClick={() => navigate('#/calendar')}>Open publishing calendar</GuardedButton>
        <GuardedButton permission="content:view" className="secondary" onClick={() => navigate('#/calendar/bulk')}>Bulk schedule calendar</GuardedButton>
        <GuardedButton permission="content:view" className="secondary" onClick={() => navigate('#/handoff')}>Batch export handoff</GuardedButton>
        <GuardedButton permission="content:view" className="secondary" onClick={() => navigate('#/production-board')}>Open production board</GuardedButton>
        <GuardedButton permission="content:view" className="secondary" onClick={() => navigate('#/ideas')}>Open idea backlog</GuardedButton>
        <GuardedButton permission="assets:manage" className="secondary" onClick={() => navigate('#/assets')}>Upload visual assets</GuardedButton>
        <GuardedButton permission="templates:manage" className="secondary" onClick={() => navigate('#/templates')}>Manage prompt templates</GuardedButton>
        <GuardedButton permission="analytics:view" className="secondary" onClick={() => navigate('#/analytics')}>View analytics insights</GuardedButton>
        <GuardedButton permission="analytics:view" className="secondary" onClick={() => navigate('#/provider-logs')}>Review provider logs</GuardedButton>
        <GuardedButton permission="content:create" className="secondary" onClick={() => navigate('#/demo')}>Run MVP demo setup</GuardedButton>
        <button className="secondary" onClick={() => navigate('#/setup')}>Fresh clone setup</button>
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
  const canCreate = useCan('content:create')
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
    if (!canCreate) {
      setError('You do not have permission to create content packages.')
      return
    }
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
        <PermissionNotice permission="content:create" />
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
          <GuardedButton permission="content:create" type="submit" disabled={loading}>{loading ? 'Generating...' : 'Generate package'}</GuardedButton>
        </div>
      </form>
    </section>
  )
}

function BatchesPage() {
  const canCreate = useCan('content:create')
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
    if (!canCreate) {
      setError('You do not have permission to create content batches.')
      return
    }
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
        action={<GuardedButton permission="content:create" onClick={() => navigate('#/new')}>Create package</GuardedButton>}
      />

      {message && <div className="success-banner">{message}</div>}
      {error && <div className="form-error">{error}</div>}

      <form className="card form-grid" onSubmit={submit}>
        <PermissionNotice permission="content:create" />
        <Input label="Batch name" value={form.name} onChange={(v) => update('name', v)} />
        <Input label="Niche" value={form.niche} onChange={(v) => update('niche', v)} />
        <Input label="Target audience" value={form.target_audience} onChange={(v) => update('target_audience', v)} />
        <Input type="date" label="Start date" value={form.start_date} onChange={(v) => update('start_date', v)} />
        <Input type="date" label="End date" value={form.end_date} onChange={(v) => update('end_date', v)} />
        <Input type="number" label="Planned count" value={form.planned_count} onChange={(v) => update('planned_count', v)} />
        <Select label="Status" value={form.status} options={['planning', 'active', 'completed', 'paused']} onChange={(v) => update('status', v)} />
        <TextArea label="Notes" value={form.notes} onChange={(v) => update('notes', v)} rows={4} wide />
        <div className="form-actions wide"><GuardedButton permission="content:create" type="submit">Create batch</GuardedButton></div>
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
  const canEdit = useCan('content:edit')
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
    if (!canEdit) {
      setError('You do not have permission to edit content batches.')
      return
    }
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
        action={<GuardedButton permission="content:create" onClick={() => navigate('#/new')}>Create package for batch</GuardedButton>}
      />
      {message && <div className="success-banner">{message}</div>}
      {error && <div className="form-error">{error}</div>}

      <form className="card form-grid" onSubmit={submit}>
        <PermissionNotice permission="content:edit" />
        <Input label="Batch name" value={form.name} onChange={(v) => update('name', v)} />
        <Input label="Niche" value={form.niche} onChange={(v) => update('niche', v)} />
        <Input label="Target audience" value={form.target_audience} onChange={(v) => update('target_audience', v)} />
        <Input type="date" label="Start date" value={form.start_date || ''} onChange={(v) => update('start_date', v)} />
        <Input type="date" label="End date" value={form.end_date || ''} onChange={(v) => update('end_date', v)} />
        <Input type="number" label="Planned count" value={form.planned_count} onChange={(v) => update('planned_count', v)} />
        <Select label="Status" value={form.status} options={['planning', 'active', 'completed', 'paused']} onChange={(v) => update('status', v)} />
        <TextArea label="Notes" value={form.notes || ''} onChange={(v) => update('notes', v)} rows={4} wide />
        <div className="form-actions wide"><GuardedButton permission="content:edit" type="submit">Save batch</GuardedButton></div>
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
  const canManageCalendar = useCan('calendar:manage')
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
    if (!canManageCalendar) {
      setError('You do not have permission to manage the publishing calendar.')
      return
    }
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
    if (!canManageCalendar) {
      setError('You do not have permission to manage the publishing calendar.')
      return
    }
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
        action={<GuardedButton permission="content:create" onClick={() => navigate('#/new')}>Create package</GuardedButton>}
      />
      {message && <div className="success-banner">{message}</div>}
      {error && <div className="form-error">{error}</div>}

      <form className="card form-grid" onSubmit={submit}>
        <PermissionNotice permission="calendar:manage" />
        <Select label="Package" value={form.package_id} options={packageOptions} onChange={(v) => update('package_id', v)} disabled={Boolean(editing)} />
        <Input type="date" label="Planned publish date" value={form.planned_publish_date} onChange={(v) => update('planned_publish_date', v)} />
        <Input type="date" label="Actual publish date" value={form.actual_publish_date} onChange={(v) => update('actual_publish_date', v)} />
        <Input label="Platform" value={form.platform} onChange={(v) => update('platform', v)} />
        <Select label="Status" value={form.status} options={['planned', 'scheduled', 'published', 'skipped']} onChange={(v) => update('status', v)} />
        <Input label="Playlist name" value={form.playlist_name} onChange={(v) => update('playlist_name', v)} />
        <TextArea label="Notes" value={form.notes} onChange={(v) => update('notes', v)} rows={3} wide />
        <div className="form-actions wide">
          {editing && <button type="button" className="secondary" onClick={resetForm}>Cancel edit</button>}
          <GuardedButton permission="calendar:manage" type="submit">{editing ? 'Save calendar entry' : 'Schedule package'}</GuardedButton>
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
                  <GuardedButton permission="calendar:manage" className="secondary small" onClick={() => startEdit(entry)}>Edit</GuardedButton>
                  <GuardedButton permission="calendar:manage" className="secondary small" onClick={() => remove(entry.id)}>Remove</GuardedButton>
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



function BatchHandoffPage() {
  const canPublish = useCan('content:publish')
  const [batches, setBatches] = useState([])
  const [runs, setRuns] = useState([])
  const [form, setForm] = useState(initialBatchHandoff)
  const [latest, setLatest] = useState(null)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  function load() {
    setError('')
    Promise.all([fetchBatches(), fetchBatchHandoffs()])
      .then(([batchPayload, runPayload]) => {
        setBatches(batchPayload.batches || [])
        setRuns(runPayload.handoff_runs || [])
      })
      .catch((err) => setError(err.message))
  }

  useEffect(load, [])

  function update(name, value) {
    setForm((current) => ({ ...current, [name]: value }))
  }

  async function submit(event) {
    event.preventDefault()
    setError('')
    setMessage('')
    if (!canPublish) {
      setError('You do not have permission to create production handoff exports.')
      return
    }
    setBusy(true)
    try {
      const payload = {
        ...form,
        batch_id: form.batch_id ? Number(form.batch_id) : null,
        limit_count: Number(form.limit_count || 50),
        ready_only: Boolean(form.ready_only)
      }
      const result = await createBatchHandoff(payload)
      setLatest(result.handoff_run)
      setRuns(result.handoff_runs || [])
      setMessage(`Handoff ready: ${result.handoff_run.package_count} package(s) included, ${result.handoff_run.skipped_count} skipped.`)
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  const batchOptions = [{ value: '', label: 'All packages' }, ...batches.map((b) => ({ value: String(b.id), label: b.name }))]

  return (
    <section>
      <Header
        title="Batch export and production handoff"
        subtitle="Export many ready Shorts together with manifests, per-package ZIPs, editor README, and skipped-item notes."
        action={<a className="button secondary" href={batchHandoffReportDownloadUrl()} target="_blank" rel="noreferrer">Download handoff report</a>}
      />
      {message && <div className="success-banner">{message}</div>}
      {error && <div className="form-error">{error}</div>}

      <form className="card form-grid" onSubmit={submit}>
        <PermissionNotice permission="content:publish" />
        <Input label="Handoff name" value={form.handoff_name} onChange={(v) => update('handoff_name', v)} />
        <Select label="Batch/source" value={form.batch_id} options={batchOptions} onChange={(v) => update('batch_id', v)} />
        <Input type="number" label="Maximum packages" value={form.limit_count} onChange={(v) => update('limit_count', v)} />
        <Input label="Created by" value={form.created_by} onChange={(v) => update('created_by', v)} />
        <label className="checkbox-field wide"><input type="checkbox" checked={form.ready_only} onChange={(event) => update('ready_only', event.target.checked)} /> Include only review-ready packages</label>
        <TextArea wide rows={3} label="Handoff notes" value={form.notes} onChange={(v) => update('notes', v)} />
        <div className="form-actions wide">
          <GuardedButton permission="content:publish" disabled={busy}>{busy ? 'Creating handoff...' : 'Create handoff ZIP'}</GuardedButton>
        </div>
      </form>

      {latest && (
        <div className="card stack">
          <div className="card-header"><h2>Latest handoff</h2><a className="button" href={batchHandoffDownloadUrl(latest.id)} target="_blank" rel="noreferrer">Download ZIP</a></div>
          <div className="stats-grid compact-stats">
            <StatCard label="Included" value={latest.package_count} />
            <StatCard label="Skipped" value={latest.skipped_count} />
            <StatCard label="Ready-only" value={latest.ready_only ? 'Yes' : 'No'} />
          </div>
          <p className="muted">Open the ZIP and start with <strong>README_HANDOFF.md</strong> and <strong>manifest.csv</strong>.</p>
        </div>
      )}

      <div className="card">
        <div className="card-header"><h2>Recent handoff exports</h2><span>{runs.length}</span></div>
        {runs.length === 0 ? <p className="muted">No handoff exports yet.</p> : (
          <div className="package-list compact">
            {runs.map((run) => (
              <div className="package-row static" key={run.id}>
                <div>
                  <h3>#{run.id} — {run.handoff_name}</h3>
                  <p>{run.batch_name || 'All packages'} • {run.package_count} included • {run.skipped_count} skipped</p>
                  <p>{run.created_at}</p>
                </div>
                <div className="row-meta">
                  <StatusBadge status={run.ready_only ? 'ready_only' : 'all'} />
                  <a className="button secondary small" href={batchHandoffDownloadUrl(run.id)} target="_blank" rel="noreferrer">Download</a>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  )
}

function BulkScheduleCalendarPage() {
  const canManageCalendar = useCan('calendar:manage')
  const [data, setData] = useState(null)
  const [batches, setBatches] = useState([])
  const [runs, setRuns] = useState([])
  const [form, setForm] = useState(initialBulkCalendar)
  const [preview, setPreview] = useState(null)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  function load() {
    setError('')
    Promise.all([fetchCalendar(), fetchBatches(), fetchCalendarBulkRuns()])
      .then(([calendarPayload, batchPayload, runPayload]) => {
        setData(calendarPayload)
        setBatches(batchPayload.batches || [])
        setRuns(runPayload.bulk_runs || [])
      })
      .catch((err) => setError(err.message))
  }

  useEffect(load, [])

  function update(name, value) {
    setForm((current) => ({ ...current, [name]: value }))
  }

  function buildPayload(apply) {
    return {
      ...form,
      batch_id: form.batch_id ? Number(form.batch_id) : null,
      limit: Number(form.limit || 20),
      videos_per_day: Number(form.videos_per_day || 1),
      days_between: Number(form.days_between || 0),
      apply
    }
  }

  async function previewSchedule(event) {
    event.preventDefault()
    setMessage('')
    setError('')
    try {
      const result = await bulkScheduleCalendar(buildPayload(false))
      setPreview(result.bulk_schedule)
      setRuns(result.bulk_runs || [])
      setMessage(`Preview ready: ${result.bulk_schedule.scheduled_count} package(s) can be scheduled.`)
    } catch (err) {
      setError(err.message)
    }
  }

  async function applySchedule() {
    setMessage('')
    setError('')
    if (!canManageCalendar) {
      setError('You do not have permission to bulk schedule calendar entries.')
      return
    }
    try {
      const result = await bulkScheduleCalendar(buildPayload(true))
      setPreview(result.bulk_schedule)
      setData(result.calendar_payload)
      setRuns(result.bulk_runs || [])
      setMessage(`Bulk schedule applied: ${result.bulk_schedule.inserted_count} added, ${result.bulk_schedule.skipped_count} skipped.`)
    } catch (err) {
      setError(err.message)
    }
  }

  if (error && !data) return <ErrorCard title="Could not load bulk scheduler" message={error} />
  if (!data) return <Loading />

  const batchOptions = [{ value: '', label: 'All unscheduled packages' }, ...batches.map((b) => ({ value: String(b.id), label: b.name }))]

  return (
    <section>
      <Header
        title="Content calendar bulk scheduling"
        subtitle="Schedule a batch of Shorts in one step, then fine-tune dates from the publishing calendar."
        action={<a className="button secondary" href={calendarBulkReportDownloadUrl()} target="_blank" rel="noreferrer">Download bulk report</a>}
      />
      {message && <div className="success-banner">{message}</div>}
      {error && <div className="form-error">{error}</div>}

      <form className="card form-grid" onSubmit={previewSchedule}>
        <PermissionNotice permission="calendar:manage" />
        <Select label="Package source" value={form.batch_id} options={batchOptions} onChange={(v) => update('batch_id', v)} />
        <Input type="date" label="Start date" value={form.start_date} onChange={(v) => update('start_date', v)} />
        <Input type="number" label="Max packages" value={form.limit} onChange={(v) => update('limit', v)} />
        <Input type="number" label="Videos per day" value={form.videos_per_day} onChange={(v) => update('videos_per_day', v)} />
        <Input type="number" label="Gap days after each publishing day" value={form.days_between} onChange={(v) => update('days_between', v)} />
        <Select label="Order by" value={form.order_by} options={['created_at', 'trust_score', 'topic']} onChange={(v) => update('order_by', v)} />
        <Input label="Platform" value={form.platform} onChange={(v) => update('platform', v)} />
        <Input label="Playlist name" value={form.playlist_name} onChange={(v) => update('playlist_name', v)} />
        <Select label="Initial status" value={form.status} options={['planned', 'scheduled']} onChange={(v) => update('status', v)} />
        <Input label="Created by" value={form.created_by} onChange={(v) => update('created_by', v)} />
        <div className="form-actions wide">
          <button className="secondary" type="submit">Preview schedule</button>
          <GuardedButton permission="calendar:manage" type="button" onClick={applySchedule}>Apply bulk schedule</GuardedButton>
        </div>
      </form>

      <div className="grid two-cols">
        <div className="card">
          <div className="card-header"><h2>Preview</h2><span>{preview?.items?.length || 0} items</span></div>
          {!preview ? <p className="muted">Preview a schedule before applying it.</p> : preview.items.length === 0 ? <p className="muted">No unscheduled packages match this filter.</p> : (
            <div className="calendar-list">
              {preview.items.map((item) => (
                <div className="calendar-entry" key={item.id}>
                  <div>
                    <strong>{item.planned_publish_date} • {item.topic}</strong>
                    <p>{item.subject} • {item.class_level} • {item.batch_name || 'No batch'} • trust {item.trust_score}</p>
                  </div>
                  <StatusBadge status={item.status} />
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="card">
          <div className="card-header"><h2>Recent bulk runs</h2><span>{runs.length}</span></div>
          {runs.length === 0 ? <p className="muted">No bulk runs yet.</p> : (
            <div className="package-list compact">
              {runs.slice(0, 8).map((run) => (
                <div className="package-row static" key={run.id}>
                  <div>
                    <h3>Run #{run.id}: {run.batch_name || 'All unscheduled packages'}</h3>
                    <p>{run.start_date} • {run.platform} • {run.playlist_name || 'No playlist'}</p>
                  </div>
                  <div className="row-meta"><span>{run.scheduled_count} scheduled</span><span>{run.skipped_count} skipped</span></div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <div className="card">
        <div className="card-header"><h2>Still unscheduled</h2><span>{data.unscheduled_packages.length}</span></div>
        {data.unscheduled_packages.length === 0 ? <p className="muted">All packages are scheduled.</p> : (
          <div className="package-list compact">
            {data.unscheduled_packages.slice(0, 12).map((item) => (
              <button key={item.id} className="package-row" onClick={() => navigate(`#/packages/${item.id}`)}>
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
  const canManageAssets = useCan('assets:manage')
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
    if (!canManageAssets) {
      setError('You do not have permission to manage visual assets.')
      return
    }
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
    if (!canManageAssets) {
      setError('You do not have permission to manage visual assets.')
      return
    }
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
        action={<GuardedButton permission="content:create" onClick={() => navigate('#/new')}>Create package</GuardedButton>}
      />
      {message && <div className="success-banner">{message}</div>}
      {error && <div className="form-error">{error}</div>}

      <div className="detail-grid">
        <form className="card stack" onSubmit={submit}>
          <h2>Upload asset</h2>
          <PermissionNotice permission="assets:manage" compact />
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
          <GuardedButton permission="assets:manage" type="submit">Upload visual asset</GuardedButton>
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
                    <GuardedButton permission="assets:manage" className="danger small" onClick={() => remove(asset.id)}>Delete</GuardedButton>
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
  const canManageTemplates = useCan('templates:manage')
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
    if (!canManageTemplates) {
      setError('You do not have permission to manage prompt templates.')
      return
    }
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
    if (!canManageTemplates) {
      setError('You do not have permission to manage prompt templates.')
      return
    }
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
    if (!canManageTemplates) {
      setError('You do not have permission to manage prompt templates.')
      return
    }
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
        action={<GuardedButton permission="templates:manage" onClick={seedDefaults}>Seed default templates</GuardedButton>}
      />
      {message && <div className="success-banner">{message}</div>}
      {error && <div className="form-error">{error}</div>}

      <div className="detail-grid">
        <form className="card stack" onSubmit={save}>
          <h2>{editingId ? 'Edit prompt template' : 'Create prompt template'}</h2>
          <PermissionNotice permission="templates:manage" compact />
          <Input label="Name" value={form.name} onChange={(v) => update('name', v)} />
          <Input label="Task type" value={form.task_type} onChange={(v) => update('task_type', v)} />
          <Input label="Style key" value={form.style_key} onChange={(v) => update('style_key', v)} />
          <Select label="Active" value={form.active ? 'true' : 'false'} options={[{ value: 'true', label: 'Active' }, { value: 'false', label: 'Inactive' }]} onChange={(v) => update('active', v === 'true')} />
          <TextArea label="Template text" value={form.template_text} onChange={(v) => update('template_text', v)} rows={12} />
          <TextArea label="Notes" value={form.notes} onChange={(v) => update('notes', v)} rows={3} />
          <div className="button-row">
            <GuardedButton permission="templates:manage" type="submit">{editingId ? 'Save template' : 'Create template'}</GuardedButton>
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
                  <GuardedButton permission="templates:manage" className="secondary small" onClick={() => previewTemplate(template)}>Preview</GuardedButton>
                  <GuardedButton permission="templates:manage" className="secondary small" onClick={() => edit(template)}>Edit</GuardedButton>
                  <GuardedButton permission="templates:manage" className="danger small" onClick={() => remove(template.id)}>Delete</GuardedButton>
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
  const canReview = useCan('content:review')
  const canEdit = useCan('content:edit')
  const canPublish = useCan('content:publish')
  const canManageAnalytics = useCan('analytics:manage')
  const canGenerateThumbnail = useCan('thumbnail:generate')
  const canReviewSourceSafety = useCan('source_safety:review')
  const canReviewTrust = useCan('trust_score:review')
  const canGenerateLearningOutputs = useCan('learning_outputs:generate')
  const canGenerateAudio = useCan('audio:generate')
  const canGenerateVideo = useCan('video:generate')
  const canManageAssets = useCan('assets:manage')
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
  const [publishingApprovalGenerating, setPublishingApprovalGenerating] = useState(false)
  const [publishingApprovalSaving, setPublishingApprovalSaving] = useState(false)
  const [publishingApprovalDecision, setPublishingApprovalDecision] = useState(initialPublishingApprovalDecision)
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
    if (!canReview) {
      setError('You do not have permission to review scripts.')
      return
    }
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
    if (!canEdit) {
      setError('You do not have permission to edit package batch assignment.')
      return
    }
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
    if (!canGenerateAudio) {
      setError('You do not have permission to generate narration audio.')
      return
    }
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
    if (!canGenerateVideo) {
      setError('You do not have permission to generate assembly plans.')
      return
    }
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
    if (!canGenerateThumbnail) {
      setError('You do not have permission to generate thumbnail helpers.')
      return
    }
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
    if (!canReviewSourceSafety) {
      setError('You do not have permission to generate source safety reviews.')
      return
    }
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
    if (!canReviewTrust) {
      setError('You do not have permission to generate teacher trust reviews.')
      return
    }
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
    if (!canReviewTrust) {
      setError('You do not have permission to edit teacher trust reviews.')
      return
    }
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
    if (!canGenerateLearningOutputs) {
      setError('You do not have permission to generate learning outputs.')
      return
    }
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


  async function createPublishingApprovalGate() {
    setMessage('')
    setError('')
    if (!canPublish) {
      setError('You do not have permission to create publishing approval gates.')
      return
    }
    setPublishingApprovalGenerating(true)
    try {
      const result = await generatePublishingApproval(id)
      setData((current) => ({
        ...current,
        publishing_approvals: [result.publishing_approval, ...(current.publishing_approvals || [])]
      }))
      setPublishingApprovalDecision({
        ...initialPublishingApprovalDecision,
        reviewer_decision: result.publishing_approval.gate_status === 'approved' ? 'approved' : 'changes_required'
      })
      setMessage(`Publishing gate generated: ${result.publishing_approval.status}.`)
    } catch (err) {
      setError(err.message)
    } finally {
      setPublishingApprovalGenerating(false)
    }
  }

  async function savePublishingApprovalDecision(approvalId) {
    setMessage('')
    setError('')
    if (!canPublish) {
      setError('You do not have permission to approve publishing gates.')
      return
    }
    setPublishingApprovalSaving(true)
    try {
      const result = await updatePublishingApproval(id, approvalId, publishingApprovalDecision)
      setData((current) => ({
        ...current,
        publishing_approvals: (current.publishing_approvals || []).map((item) => item.id === result.publishing_approval.id ? result.publishing_approval : item)
      }))
      setMessage(`Publishing decision saved: ${result.publishing_approval.status}.`)
    } catch (err) {
      setError(err.message)
    } finally {
      setPublishingApprovalSaving(false)
    }
  }

  async function createVideoDraft() {
    setMessage('')
    setError('')
    if (!canGenerateVideo) {
      setError('You do not have permission to generate video drafts.')
      return
    }
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
    if (!canManageAnalytics) {
      setError('You do not have permission to save analytics.')
      return
    }
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
  const latestPublishingApproval = (data.publishing_approvals || [])[0]
  const publishingGateApproved = latestPublishingApproval?.status === 'approved' && latestPublishingApproval?.reviewer_decision === 'approved'

  return (
    <section>
      <Header
        title={pkg.topic}
        subtitle={`${pkg.class_level} • ${pkg.subject} • ${pkg.duration_seconds}s • ${pkg.provider_used}`}
        action={publishingGateApproved
          ? <GuardedLink permission="content:publish" className="button-link" href={exportUrl(id)}>Export publish ZIP</GuardedLink>
          : <button className="secondary locked-action" disabled title="Generate and approve the publishing gate before final export">Publish gate required</button>
        }
      />
      {message && <div className="success-banner">{message}</div>}
      {error && <div className="form-error">{error}</div>}

      <div className="detail-grid">
        <div className="card stack">
          <div className="card-header"><h2>Review</h2><TrustBadge score={pkg.trust_score} /></div>
          <PermissionNotice permission="content:review" compact />
          <Select label="Review status" value={reviewStatus} options={['draft', 'approved', 'edit_required', 'rejected', 'published']} onChange={setReviewStatus} />
          <TextArea label="Script editor" value={scriptText} onChange={setScriptText} rows={12} />
          <TextArea label="Reviewer notes" value={reviewerNotes} onChange={setReviewerNotes} rows={4} />
          <div className="button-row">
            <GuardedButton permission="content:review" onClick={saveReview}>Save review</GuardedButton>
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
          <GuardedButton permission="thumbnail:generate" onClick={createThumbnailGuide} disabled={thumbnailGenerating}>
            {thumbnailGenerating ? 'Generating...' : 'Generate thumbnail helper'}
          </GuardedButton>
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
          <GuardedButton permission="source_safety:review" onClick={createSourceSafetyReview} disabled={sourceSafetyGenerating}>
            {sourceSafetyGenerating ? 'Checking...' : 'Generate source safety review'}
          </GuardedButton>
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
          <GuardedButton permission="trust_score:review" onClick={createTrustReview} disabled={trustReviewGenerating}>
            {trustReviewGenerating ? 'Generating...' : 'Generate trust review'}
          </GuardedButton>
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
                  <GuardedButton permission="trust_score:review" className="secondary small" onClick={() => setEditingTrustReview(review)}>Edit scores</GuardedButton>
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
                <GuardedButton permission="trust_score:review" onClick={saveTrustReview} disabled={trustReviewSaving}>{trustReviewSaving ? 'Saving...' : 'Save trust review'}</GuardedButton>
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
          <GuardedButton permission="learning_outputs:generate" onClick={createLearningOutput} disabled={learningOutputGenerating}>
            {learningOutputGenerating ? 'Generating...' : 'Generate learning outputs'}
          </GuardedButton>
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
          <GuardedButton permission="content:edit" onClick={saveBatch}>Save batch assignment</GuardedButton>
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
            <h2>Publishing approval gate</h2>
            <p className="muted">Final publisher checkpoint before marking this Short as published. Required checks include script approval, source safety, and Teacher Trust Score readiness.</p>
          </div>
          <GuardedButton permission="content:publish" onClick={createPublishingApprovalGate} disabled={publishingApprovalGenerating}>
            {publishingApprovalGenerating ? 'Checking...' : 'Generate publishing gate'}
          </GuardedButton>
        </div>
        {!data.publishing_approvals || data.publishing_approvals.length === 0 ? (
          <p className="muted">No publishing gate yet. Generate this after source safety and Teacher Trust Score reviews are complete.</p>
        ) : (
          <div className="review-list">
            {data.publishing_approvals.map((approval, index) => (
              <div className="review-entry" key={approval.id}>
                <div>
                  <strong>Gate #{approval.id}</strong>
                  <p>{approval.status} • gate: {approval.gate_status} • required failures: {approval.required_failures_count} • optional warnings: {approval.optional_warnings_count}</p>
                  {index === 0 && <p className="muted">Latest gate controls the publish ZIP button above.</p>}
                  <div className="checklist-mini">
                    {(approval.checklist || []).slice(0, 6).map((item) => (
                      <span key={item.key} className={item.passed ? 'passed-check' : 'failed-check'}>{item.passed ? '✓' : '×'} {item.label}</span>
                    ))}
                  </div>
                </div>
                <div className="row-meta">
                  <StatusBadge status={approval.status} />
                  <a className="button-link small" href={publishingApprovalDownloadUrl(id, approval.id)}>Download gate</a>
                </div>
              </div>
            ))}
          </div>
        )}
        {latestPublishingApproval && (
          <div className="approval-editor">
            <h3>Publisher decision for latest gate</h3>
            <PermissionNotice permission="content:publish" compact />
            <Select label="Decision" value={publishingApprovalDecision.reviewer_decision} options={[
              { value: 'pending', label: 'Pending' },
              { value: 'approved', label: 'Approved' },
              { value: 'changes_required', label: 'Changes required' },
              { value: 'rejected', label: 'Rejected' }
            ]} onChange={(v) => setPublishingApprovalDecision({ ...publishingApprovalDecision, reviewer_decision: v })} />
            <Input label="Publisher/reviewer name" value={publishingApprovalDecision.reviewer_name} onChange={(v) => setPublishingApprovalDecision({ ...publishingApprovalDecision, reviewer_name: v })} />
            <TextArea label="Publisher notes" value={publishingApprovalDecision.reviewer_notes} onChange={(v) => setPublishingApprovalDecision({ ...publishingApprovalDecision, reviewer_notes: v })} rows={3} />
            <GuardedButton permission="content:publish" onClick={() => savePublishingApprovalDecision(latestPublishingApproval.id)} disabled={publishingApprovalSaving}>
              {publishingApprovalSaving ? 'Saving...' : 'Save publisher decision'}
            </GuardedButton>
          </div>
        )}
      </div>

      <div className="card stack">
        <div className="card-header">
          <div>
            <h2>Narration audio</h2>
            <p className="muted">Generate offline narration when possible. If no local TTS is ready, the system creates a manual recording guide.</p>
          </div>
          <GuardedButton permission="audio:generate" onClick={createNarrationAudio} disabled={audioGenerating}>
            {audioGenerating ? 'Generating...' : 'Generate narration'}
          </GuardedButton>
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
          <GuardedButton permission="video:generate" onClick={createAssemblyPlan} disabled={assemblyGenerating}>
            {assemblyGenerating ? 'Generating...' : 'Generate assembly plan'}
          </GuardedButton>
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
          <GuardedButton permission="assets:manage" className="secondary" onClick={() => navigate('#/assets')}>Manage assets</GuardedButton>
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
          <GuardedButton permission="video:generate" onClick={createVideoDraft} disabled={videoDraftGenerating}>
            {videoDraftGenerating ? 'Generating...' : 'Generate video draft'}
          </GuardedButton>
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
          <PermissionNotice permission="analytics:manage" compact />
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
          <div className="wide"><GuardedButton permission="analytics:manage" type="submit">Save analytics</GuardedButton></div>
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




function ContentIdeaBacklogPage() {
  const canCreate = useCan('content:create')
  const canEdit = useCan('content:edit')
  const [data, setData] = useState(null)
  const [batches, setBatches] = useState([])
  const [form, setForm] = useState(initialContentIdea)
  const [editingId, setEditingId] = useState(null)
  const [statusFilter, setStatusFilter] = useState('')
  const [search, setSearch] = useState('')
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const [busy, setBusy] = useState(false)

  function load() {
    setError('')
    fetchContentIdeas({ status: statusFilter, search })
      .then(setData)
      .catch((err) => setError(err.message))
    fetchBatches().then((result) => setBatches(result.batches || [])).catch(() => setBatches([]))
  }

  useEffect(load, [statusFilter])

  function update(name, value) {
    setForm((current) => ({ ...current, [name]: value }))
  }

  function payloadFromForm() {
    return {
      ...form,
      batch_id: form.batch_id ? Number(form.batch_id) : null,
      curiosity_score: Number(form.curiosity_score),
      evergreen_score: Number(form.evergreen_score),
      visual_potential_score: Number(form.visual_potential_score),
      student_value_score: Number(form.student_value_score),
      production_effort_score: Number(form.production_effort_score),
      monetization_potential_score: Number(form.monetization_potential_score)
    }
  }

  async function submit(event) {
    event.preventDefault()
    setBusy(true)
    setError('')
    setMessage('')
    try {
      if (editingId) {
        await updateContentIdea(editingId, payloadFromForm())
        setMessage('Idea updated and score recalculated.')
      } else {
        await createContentIdea(payloadFromForm())
        setMessage('Idea added to backlog with topic score.')
      }
      resetForm()
      load()
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  function editIdea(idea) {
    setEditingId(idea.id)
    setForm({
      title: idea.title || '',
      subject: idea.subject || 'Science',
      class_level: idea.class_level || 'Class 7',
      target_audience: idea.target_audience || 'School students',
      language: idea.language || 'English',
      idea_type: idea.idea_type || 'curiosity',
      hook_angle: idea.hook_angle || '',
      source_hint: idea.source_hint || '',
      batch_id: idea.batch_id ? String(idea.batch_id) : '',
      status: idea.status || 'backlog',
      notes: idea.notes || '',
      curiosity_score: idea.curiosity_score || 7,
      evergreen_score: idea.evergreen_score || 7,
      visual_potential_score: idea.visual_potential_score || 7,
      student_value_score: idea.student_value_score || 7,
      production_effort_score: idea.production_effort_score || 4,
      monetization_potential_score: idea.monetization_potential_score || 5
    })
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  function resetForm() {
    setEditingId(null)
    setForm(initialContentIdea)
  }

  async function removeIdea(id) {
    if (!window.confirm('Delete this idea from the backlog?')) return
    setError('')
    setMessage('')
    try {
      await deleteContentIdea(id)
      setMessage('Idea deleted.')
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  async function convertIdea(idea) {
    setBusy(true)
    setError('')
    setMessage('')
    try {
      const result = await convertContentIdea(idea.id, {
        output_type: 'Short',
        tone: idea.idea_type === 'exam_friendly' ? 'Exam-focused' : idea.idea_type === 'mistake_correction' ? 'Mistake correction' : 'Curious',
        duration_seconds: 60,
        board_source: 'NCERT / Self-written',
        source_name: 'Idea backlog notes',
        source_license_type: 'Self-written / Original',
        page_or_section_reference: 'Idea backlog',
        transformation_notes: 'Converted from scored backlog idea into a Shorts package.'
      })
      navigate(`#/packages/${result.package.id}`)
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  if (error && !data) return <ErrorCard title="Could not load idea backlog" message={error} />
  if (!data) return <Loading />

  const backlog = data.idea_backlog || { ideas: [], summary: {} }
  const summary = backlog.summary || {}
  const ideas = backlog.ideas || []
  const statuses = data.statuses || ['backlog', 'shortlisted', 'ready', 'converted', 'archived']
  const ideaTypes = data.idea_types || ['curiosity', 'textbook_doubt', 'exam_friendly', 'myth_vs_fact', 'mistake_correction', 'series']

  return (
    <section>
      <Header
        title="Content idea backlog"
        subtitle="Capture Shorts ideas first, score them, shortlist the best ones, and convert only strong ideas into content packages."
        action={<a className="button-link secondary" href={contentIdeasDownloadUrl()} target="_blank" rel="noreferrer">Download backlog</a>}
      />

      <div className="stats-grid">
        <StatCard label="Total ideas" value={summary.total || 0} />
        <StatCard label="Ready/shortlisted" value={summary.ready_or_shortlisted || 0} />
        <StatCard label="Average score" value={summary.average_score || 0} />
        <StatCard label="Backlog" value={(summary.by_status || {}).backlog || 0} />
      </div>

      {message && <div className="success-banner">{message}</div>}
      {error && <div className="form-error">{error}</div>}

      <form className="card form-grid" onSubmit={submit}>
        <PermissionNotice permission={editingId ? 'content:edit' : 'content:create'} />
        <Input label="Idea title" value={form.title} onChange={(v) => update('title', v)} />
        <Input label="Subject" value={form.subject} onChange={(v) => update('subject', v)} />
        <Input label="Class / Level" value={form.class_level} onChange={(v) => update('class_level', v)} />
        <Input label="Target audience" value={form.target_audience} onChange={(v) => update('target_audience', v)} />
        <Input label="Language" value={form.language} onChange={(v) => update('language', v)} />
        <Select label="Idea type" value={form.idea_type} options={ideaTypes} onChange={(v) => update('idea_type', v)} />
        <Select label="Status" value={form.status} options={statuses} onChange={(v) => update('status', v)} />
        <Select label="Target batch" value={form.batch_id} options={[{ value: '', label: 'No batch yet' }, ...batches.map((b) => ({ value: String(b.id), label: b.name }))]} onChange={(v) => update('batch_id', v)} />
        <TextArea label="Hook angle" value={form.hook_angle} onChange={(v) => update('hook_angle', v)} rows={3} wide />
        <TextArea label="Source hint / fact notes" value={form.source_hint} onChange={(v) => update('source_hint', v)} rows={4} wide />
        <TextArea label="Planning notes" value={form.notes} onChange={(v) => update('notes', v)} rows={3} wide />

        <Input type="number" label="Curiosity score (1-10)" value={form.curiosity_score} onChange={(v) => update('curiosity_score', v)} />
        <Input type="number" label="Evergreen score (1-10)" value={form.evergreen_score} onChange={(v) => update('evergreen_score', v)} />
        <Input type="number" label="Visual potential (1-10)" value={form.visual_potential_score} onChange={(v) => update('visual_potential_score', v)} />
        <Input type="number" label="Student value (1-10)" value={form.student_value_score} onChange={(v) => update('student_value_score', v)} />
        <Input type="number" label="Production effort (1 easy - 10 hard)" value={form.production_effort_score} onChange={(v) => update('production_effort_score', v)} />
        <Input type="number" label="Monetization potential (1-10)" value={form.monetization_potential_score} onChange={(v) => update('monetization_potential_score', v)} />

        <div className="form-actions wide">
          <button type="button" className="secondary" onClick={resetForm}>Reset</button>
          <GuardedButton permission={editingId ? 'content:edit' : 'content:create'} type="submit" disabled={busy}>{busy ? 'Saving...' : editingId ? 'Update idea' : 'Add idea'}</GuardedButton>
        </div>
      </form>

      <div className="card form-grid compact-form">
        <Select label="Status filter" value={statusFilter} options={[{ value: '', label: 'All statuses' }, ...statuses.map((status) => ({ value: status, label: status }))]} onChange={setStatusFilter} />
        <Input label="Search ideas" value={search} onChange={setSearch} />
        <div className="form-actions"><button className="secondary" onClick={load}>Search</button></div>
      </div>

      <div className="card">
        <div className="card-header"><h2>Scored ideas</h2><span>{ideas.length} items</span></div>
        {ideas.length === 0 ? <p className="muted">No ideas yet. Add the first one above.</p> : (
          <div className="package-list">
            {ideas.map((idea) => (
              <div className="package-row idea-row" key={idea.id}>
                <div>
                  <h3>{idea.title}</h3>
                  <p>{idea.subject} • {idea.class_level} • {idea.idea_type} • {idea.status}</p>
                  <p>{idea.hook_angle || 'No hook angle yet.'}</p>
                  <p><strong>Recommendation:</strong> {idea.recommendation}</p>
                  {idea.batch_name && <p>Batch: {idea.batch_name}</p>}
                  {idea.converted_package_id && <p>Converted package: #{idea.converted_package_id} {idea.converted_package_topic || ''}</p>}
                </div>
                <div className="row-meta wide-actions">
                  <TrustBadge score={Math.round(idea.total_score || 0)} />
                  <StatusBadge status={idea.priority || 'medium'} />
                  <GuardedButton permission="content:edit" className="secondary small" onClick={() => editIdea(idea)}>Edit</GuardedButton>
                  <GuardedButton permission="content:create" className="small" disabled={busy || idea.status === 'converted'} onClick={() => convertIdea(idea)}>Convert to package</GuardedButton>
                  <GuardedButton permission="content:edit" className="secondary small" onClick={() => removeIdea(idea.id)}>Delete</GuardedButton>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  )
}


function ContentSeriesPlannerPage() {
  const canCreate = useCan('content:create')
  const canEdit = useCan('content:edit')
  const [data, setData] = useState(null)
  const [form, setForm] = useState(initialContentSeries)
  const [editingId, setEditingId] = useState(null)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const [busy, setBusy] = useState(false)

  function load() {
    setError('')
    fetchContentSeries().then(setData).catch((err) => setError(err.message))
  }

  useEffect(load, [])

  function update(name, value) {
    setForm((current) => ({ ...current, [name]: value }))
  }

  async function submit(event) {
    event.preventDefault()
    setBusy(true)
    setError('')
    setMessage('')
    try {
      const payload = { ...form, planned_count: Number(form.planned_count || 10) }
      if (editingId) {
        await updateContentSeries(editingId, payload)
        setMessage('Series updated.')
      } else {
        await createContentSeries(payload)
        setMessage('Series plan created.')
      }
      setEditingId(null)
      setForm(initialContentSeries)
      load()
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  function editSeries(series) {
    setEditingId(series.id)
    setForm({
      title: series.title || '',
      niche: series.niche || '',
      target_audience: series.target_audience || '',
      subject: series.subject || 'Science',
      class_level: series.class_level || 'Class 7',
      language: series.language || 'English',
      series_goal: series.series_goal || '',
      status: series.status || 'planning',
      planned_count: series.planned_count || 10,
      episode_style: series.episode_style || '',
      cta_strategy: series.cta_strategy || '',
      notes: series.notes || ''
    })
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  async function removeSeries(id) {
    if (!window.confirm('Delete this series plan and its episode rows?')) return
    setError('')
    setMessage('')
    try {
      await deleteContentSeries(id)
      setMessage('Series deleted.')
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  if (error && !data) return <ErrorCard title="Could not load content series" message={error} />
  if (!data) return <Loading />

  const payload = data.content_series || { series: [], summary: {} }
  const series = payload.series || []
  const summary = payload.summary || {}
  const statuses = data.series_statuses || ['planning', 'active', 'completed', 'paused', 'archived']

  return (
    <section>
      <Header
        title="Content series planner"
        subtitle="Plan connected Shorts as episodes, not random one-off videos. Use series to improve returning viewers and playlist flow."
        action={<a className="button-link secondary" href={contentSeriesDownloadUrl()} target="_blank" rel="noreferrer">Download series report</a>}
      />

      <div className="stats-grid">
        <StatCard label="Total series" value={summary.total_series || 0} />
        <StatCard label="Active/planning" value={summary.active_or_planning || 0} />
        <StatCard label="Total episodes" value={summary.total_episodes || 0} />
        <StatCard label="Published episodes" value={summary.total_published || 0} />
      </div>

      {message && <div className="success-banner">{message}</div>}
      {error && <div className="form-error">{error}</div>}

      <form className="card form-grid" onSubmit={submit}>
        <PermissionNotice permission={editingId ? 'content:edit' : 'content:create'} />
        <Input label="Series title" value={form.title} onChange={(v) => update('title', v)} />
        <Input label="Niche" value={form.niche} onChange={(v) => update('niche', v)} />
        <Input label="Target audience" value={form.target_audience} onChange={(v) => update('target_audience', v)} />
        <Input label="Subject" value={form.subject} onChange={(v) => update('subject', v)} />
        <Input label="Class / Level" value={form.class_level} onChange={(v) => update('class_level', v)} />
        <Input label="Language" value={form.language} onChange={(v) => update('language', v)} />
        <Select label="Status" value={form.status} options={statuses} onChange={(v) => update('status', v)} />
        <Input type="number" label="Planned episodes" value={form.planned_count} onChange={(v) => update('planned_count', v)} />
        <TextArea label="Series goal" value={form.series_goal} onChange={(v) => update('series_goal', v)} rows={3} wide />
        <TextArea label="Episode style" value={form.episode_style} onChange={(v) => update('episode_style', v)} rows={3} wide />
        <TextArea label="CTA strategy" value={form.cta_strategy} onChange={(v) => update('cta_strategy', v)} rows={3} wide />
        <TextArea label="Notes" value={form.notes} onChange={(v) => update('notes', v)} rows={3} wide />
        <div className="form-actions wide">
          <button type="button" className="secondary" onClick={() => { setEditingId(null); setForm(initialContentSeries) }}>Reset</button>
          <GuardedButton permission={editingId ? 'content:edit' : 'content:create'} type="submit" disabled={busy}>{busy ? 'Saving...' : editingId ? 'Update series' : 'Create series'}</GuardedButton>
        </div>
      </form>

      <div className="card">
        <div className="card-header"><h2>Series plans</h2><span>{series.length} series</span></div>
        {series.length === 0 ? <p className="muted">No series yet. Create one above.</p> : (
          <div className="package-list">
            {series.map((item) => (
              <div className="package-row" key={item.id}>
                <div>
                  <h3>{item.title}</h3>
                  <p>{item.subject} • {item.class_level} • {item.status}</p>
                  <p>{item.series_goal || 'No series goal yet.'}</p>
                  <p>{item.episode_count || 0}/{item.planned_count || 0} episodes planned • {item.published_count || 0} published</p>
                </div>
                <div className="row-meta wide-actions">
                  <StatusBadge status={item.status || 'planning'} />
                  <a className="button-link small" href={`#/series/${item.id}`}>Open</a>
                  <GuardedButton permission="content:edit" className="secondary small" onClick={() => editSeries(item)}>Edit</GuardedButton>
                  <GuardedButton permission="content:edit" className="secondary small" onClick={() => removeSeries(item.id)}>Delete</GuardedButton>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  )
}

function ContentSeriesDetailPage({ id }) {
  const [data, setData] = useState(null)
  const [itemForm, setItemForm] = useState(initialSeriesItem)
  const [editingItemId, setEditingItemId] = useState(null)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const [busy, setBusy] = useState(false)

  function load() {
    setError('')
    fetchContentSeriesDetail(id).then(setData).catch((err) => setError(err.message))
  }

  useEffect(load, [id])

  function updateItem(name, value) {
    setItemForm((current) => ({ ...current, [name]: value }))
  }

  async function submitItem(event) {
    event.preventDefault()
    setBusy(true)
    setError('')
    setMessage('')
    try {
      const payload = {
        ...itemForm,
        idea_id: itemForm.idea_id ? Number(itemForm.idea_id) : null,
        package_id: itemForm.package_id ? Number(itemForm.package_id) : null,
        order_index: Number(itemForm.order_index || 1)
      }
      if (editingItemId) {
        await updateSeriesItem(id, editingItemId, payload)
        setMessage('Episode updated.')
      } else {
        await createSeriesItem(id, payload)
        setMessage('Episode added to series.')
      }
      setEditingItemId(null)
      setItemForm(initialSeriesItem)
      load()
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  function editItem(item) {
    setEditingItemId(item.id)
    setItemForm({
      idea_id: item.idea_id ? String(item.idea_id) : '',
      package_id: item.package_id ? String(item.package_id) : '',
      order_index: item.order_index || 1,
      episode_title: item.episode_title || '',
      hook_angle: item.hook_angle || '',
      target_status: item.target_status || 'planned',
      notes: item.notes || ''
    })
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  async function removeItem(itemId) {
    if (!window.confirm('Remove this episode from the series?')) return
    setError('')
    setMessage('')
    try {
      await deleteSeriesItem(id, itemId)
      setMessage('Episode removed.')
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  if (error && !data) return <ErrorCard title="Could not load series" message={error} />
  if (!data) return <Loading />

  const series = data.series
  const items = data.items || []
  const ideaOptions = [{ value: '', label: 'No idea link' }, ...(data.idea_options || []).map((idea) => ({ value: String(idea.id), label: `#${idea.id} ${idea.title}` }))]
  const packageOptions = [{ value: '', label: 'No package link' }, ...(data.package_options || []).map((pkg) => ({ value: String(pkg.id), label: `#${pkg.id} ${pkg.topic}` }))]
  const episodeStatuses = data.episode_statuses || ['planned', 'idea_ready', 'package_created', 'scheduled', 'published', 'skipped']

  return (
    <section>
      <Header
        title={series.title}
        subtitle={`${series.subject} • ${series.class_level} • ${series.status}. Plan episode order, linked ideas, and linked packages.`}
        action={<a className="button-link secondary" href={contentSeriesDownloadUrl(series.id)} target="_blank" rel="noreferrer">Download this series</a>}
      />

      <div className="stats-grid">
        <StatCard label="Episodes" value={series.episode_count || 0} />
        <StatCard label="Planned count" value={series.planned_count || 0} />
        <StatCard label="Packages linked" value={series.package_count || 0} />
        <StatCard label="Published" value={series.published_count || 0} />
      </div>

      {message && <div className="success-banner">{message}</div>}
      {error && <div className="form-error">{error}</div>}

      <div className="card stack">
        <h2>Series strategy</h2>
        <InfoBlock title="Goal" value={series.series_goal || '-'} />
        <InfoBlock title="Episode style" value={series.episode_style || '-'} />
        <InfoBlock title="CTA strategy" value={series.cta_strategy || '-'} />
      </div>

      <form className="card form-grid" onSubmit={submitItem}>
        <PermissionNotice permission="content:edit" />
        <Input type="number" label="Episode order" value={itemForm.order_index} onChange={(v) => updateItem('order_index', v)} />
        <Select label="Status" value={itemForm.target_status} options={episodeStatuses} onChange={(v) => updateItem('target_status', v)} />
        <Select label="Linked idea" value={itemForm.idea_id} options={ideaOptions} onChange={(v) => updateItem('idea_id', v)} />
        <Select label="Linked package" value={itemForm.package_id} options={packageOptions} onChange={(v) => updateItem('package_id', v)} />
        <Input label="Episode title" value={itemForm.episode_title} onChange={(v) => updateItem('episode_title', v)} />
        <TextArea label="Hook angle" value={itemForm.hook_angle} onChange={(v) => updateItem('hook_angle', v)} rows={3} wide />
        <TextArea label="Episode notes" value={itemForm.notes} onChange={(v) => updateItem('notes', v)} rows={3} wide />
        <div className="form-actions wide">
          <button type="button" className="secondary" onClick={() => { setEditingItemId(null); setItemForm(initialSeriesItem) }}>Reset</button>
          <GuardedButton permission="content:edit" type="submit" disabled={busy}>{busy ? 'Saving...' : editingItemId ? 'Update episode' : 'Add episode'}</GuardedButton>
        </div>
      </form>

      <div className="card">
        <div className="card-header"><h2>Series episodes</h2><span>{items.length} items</span></div>
        {items.length === 0 ? <p className="muted">No episodes yet. Add the first episode above.</p> : (
          <div className="package-list">
            {items.map((item) => {
              const linked = item.package_topic || item.idea_title || 'Not linked yet'
              return (
                <div className="package-row" key={item.id}>
                  <div>
                    <h3>Episode {item.order_index}: {item.episode_title || linked}</h3>
                    <p>{item.target_status} • {linked}</p>
                    <p>{item.hook_angle || 'No hook angle yet.'}</p>
                    {item.package_id && <p><a href={`#/packages/${item.package_id}`}>Open linked package #{item.package_id}</a></p>}
                  </div>
                  <div className="row-meta wide-actions">
                    <StatusBadge status={item.target_status || 'planned'} />
                    {item.idea_score && <TrustBadge score={Math.round(Number(item.idea_score))} />}
                    <GuardedButton permission="content:edit" className="secondary small" onClick={() => editItem(item)}>Edit</GuardedButton>
                    <GuardedButton permission="content:edit" className="secondary small" onClick={() => removeItem(item.id)}>Remove</GuardedButton>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </section>
  )
}


function MultilingualPlansPage() {
  const [data, setData] = useState(null)
  const [form, setForm] = useState(initialMultilingualPlan)
  const [editingId, setEditingId] = useState(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  async function load() {
    const payload = await fetchMultilingualPlans()
    setData(payload)
  }

  useEffect(() => { load().catch((err) => setError(err.message)) }, [])

  function resetForm() {
    setEditingId(null)
    setForm(initialMultilingualPlan)
  }

  function edit(plan) {
    setEditingId(plan.id)
    setForm({
      package_id: plan.package_id || '',
      source_language: plan.source_language || 'English',
      target_language: plan.target_language || 'Hindi',
      status: plan.status || 'planning',
      priority: plan.priority || 'medium',
      translation_goal: plan.translation_goal || '',
      cultural_notes: plan.cultural_notes || '',
      glossary_terms: plan.glossary_terms || '',
      voice_strategy: plan.voice_strategy || 'manual_voice',
      subtitle_strategy: plan.subtitle_strategy || 'manual_review',
      reviewer_name: plan.reviewer_name || '',
      notes: plan.notes || '',
      needs_human_translation_review: Boolean(plan.needs_human_translation_review)
    })
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  async function submit(event) {
    event.preventDefault()
    setBusy(true)
    setError('')
    const payload = { ...form, package_id: form.package_id ? Number(form.package_id) : null }
    try {
      if (editingId) await updateMultilingualPlan(editingId, payload)
      else await createMultilingualPlan(payload)
      resetForm()
      await load()
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  async function remove(id) {
    if (!window.confirm('Delete this multilingual plan?')) return
    setBusy(true)
    try {
      await deleteMultilingualPlan(id)
      await load()
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  if (!data) return <Loading />
  const summary = data.summary || {}
  const languageOptions = data.supported_languages || ['English', 'Hindi', 'Telugu']
  const packageOptions = data.package_options || []

  return (
    <section>
      <Header
        title="Multilingual planning"
        subtitle="Plan Hindi/Telugu/Tamil/Kannada versions without building full translation automation too early. Use this to prepare glossary, voice, subtitles, and human review before publishing local-language Shorts."
        action={<a className="button-link secondary" href={multilingualPlansDownloadUrl()}>Download report</a>}
      />

      <div className="stats-grid">
        <StatCard label="Plans" value={summary.total || 0} />
        <StatCard label="Ready" value={summary.ready_count || 0} />
        <StatCard label="Needs review" value={summary.needs_review_count || 0} />
        <StatCard label="Languages" value={Object.keys(summary.by_language || {}).length} />
      </div>

      <form className="card form-grid" onSubmit={submit}>
        <h2 className="wide">{editingId ? 'Edit multilingual plan' : 'Create multilingual plan'}</h2>
        <Select label="Package" value={form.package_id} onChange={(value) => setForm({ ...form, package_id: value })} options={[{ value: '', label: 'Standalone plan / no package yet' }, ...packageOptions.map((pkg) => ({ value: String(pkg.id), label: `#${pkg.id} — ${pkg.topic}` }))]} />
        <Select label="Source language" value={form.source_language} onChange={(value) => setForm({ ...form, source_language: value })} options={languageOptions} />
        <Select label="Target language" value={form.target_language} onChange={(value) => setForm({ ...form, target_language: value })} options={languageOptions.filter((language) => language !== form.source_language)} />
        <Select label="Status" value={form.status} onChange={(value) => setForm({ ...form, status: value })} options={data.statuses || []} />
        <Select label="Priority" value={form.priority} onChange={(value) => setForm({ ...form, priority: value })} options={['high', 'medium', 'low']} />
        <Select label="Voice strategy" value={form.voice_strategy} onChange={(value) => setForm({ ...form, voice_strategy: value })} options={data.voice_strategies || []} />
        <Select label="Subtitle strategy" value={form.subtitle_strategy} onChange={(value) => setForm({ ...form, subtitle_strategy: value })} options={data.subtitle_strategies || []} />
        <Input label="Reviewer name" value={form.reviewer_name} onChange={(value) => setForm({ ...form, reviewer_name: value })} />
        <TextArea wide label="Translation goal" rows={3} value={form.translation_goal} onChange={(value) => setForm({ ...form, translation_goal: value })} />
        <TextArea wide label="Cultural/localization notes" rows={4} value={form.cultural_notes} onChange={(value) => setForm({ ...form, cultural_notes: value })} />
        <TextArea wide label="Glossary terms" rows={4} value={form.glossary_terms} onChange={(value) => setForm({ ...form, glossary_terms: value })} />
        <TextArea wide label="Notes" rows={3} value={form.notes} onChange={(value) => setForm({ ...form, notes: value })} />
        <label className="field checkbox-field wide"><input type="checkbox" checked={form.needs_human_translation_review} onChange={(event) => setForm({ ...form, needs_human_translation_review: event.target.checked })} /><span>Require human translation review before publishing</span></label>
        {error && <p className="error-text wide">{error}</p>}
        <PermissionNotice permission="content:edit" compact />
        <div className="wide button-row">
          <GuardedButton permission="content:edit" disabled={busy}>{editingId ? 'Update plan' : 'Create plan'}</GuardedButton>
          {editingId && <button type="button" className="secondary" onClick={resetForm}>Cancel edit</button>}
        </div>
      </form>

      <div className="card stack">
        <div className="card-header"><h2>Language summary</h2><span className="muted">Use this to decide which language to test first.</span></div>
        <div className="mini-grid">
          {Object.entries(summary.by_language || {}).map(([language, count]) => <InfoBlock key={language} title={language} value={`${count} plan(s)`} />)}
          {Object.keys(summary.by_language || {}).length === 0 && <p className="muted">No language plans yet.</p>}
        </div>
      </div>

      <div className="card stack">
        <h2>Plans</h2>
        {(data.plans || []).length === 0 && <p className="muted">No multilingual plans yet. Create one for Hindi/Telugu/Tamil/Kannada before translating your best Shorts.</p>}
        {(data.plans || []).map((plan) => (
          <div className="list-item" key={plan.id}>
            <div>
              <strong>#{plan.id} {plan.target_language}</strong>
              <p>{plan.package_topic ? `Package: ${plan.package_topic}` : 'Standalone language plan'}</p>
              <div className="pill-list">
                <StatusBadge status={plan.status} />
                <span>{plan.priority} priority</span>
                <span>Readiness {plan.readiness_score}</span>
                <span>{plan.voice_strategy}</span>
                <span>{plan.subtitle_strategy}</span>
              </div>
              <p className="muted">{plan.recommendation}</p>
              <details><summary>Checklist</summary><ul>{(plan.checklist || []).map((item) => <li key={item.label}>{item.passed ? '✅' : '⚠️'} {item.label} — {item.fix}</li>)}</ul></details>
            </div>
            <div className="button-row compact-actions">
              <button className="secondary small" onClick={() => edit(plan)}>Edit</button>
              <GuardedButton permission="content:edit" className="secondary small" onClick={() => remove(plan.id)}>Delete</GuardedButton>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}


function ProductionBoardPage() {
  const canEdit = useCan('content:edit')
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [savingId, setSavingId] = useState(null)
  const [editing, setEditing] = useState({})

  function load() {
    setError('')
    fetchProductionBoard()
      .then((result) => {
        const board = result.production_board
        setData(board)
        const nextEditing = {}
        ;(board.cards || []).forEach((card) => {
          nextEditing[card.id] = {
            stage: card.stage || card.derived_stage || 'script_review',
            priority: card.priority || 'normal',
            owner: card.owner || '',
            due_date: card.due_date || '',
            notes: card.board_notes || ''
          }
        })
        setEditing(nextEditing)
      })
      .catch((err) => setError(err.message))
  }

  useEffect(load, [])

  function editCard(packageId, name, value) {
    setEditing((current) => ({
      ...current,
      [packageId]: { ...(current[packageId] || {}), [name]: value }
    }))
  }

  async function saveCard(packageId) {
    if (!canEdit) {
      setError('You do not have permission to update production board cards.')
      return
    }
    setSavingId(packageId)
    setError('')
    try {
      const payload = editing[packageId]
      const result = await updateProductionCard(packageId, payload)
      setData(result.production_board)
    } catch (err) {
      setError(err.message)
    } finally {
      setSavingId(null)
    }
  }

  if (error && !data) return <ErrorCard title="Could not load production board" message={error} />
  if (!data) return <Loading />

  const stageOptions = data.stages.map((stage) => ({ value: stage.key, label: stage.label }))
  const priorityOptions = ['urgent', 'high', 'normal', 'low']

  return (
    <section>
      <Header
        title="Content production board"
        subtitle="Track every Short from script review to publishing and analytics. Use this board to avoid losing work between generation, review, editing, and upload."
        action={<a className="button-link" href={productionBoardDownloadUrl()}>Download board report</a>}
      />
      {error && <div className="form-error">{error}</div>}

      <div className="stats-grid">
        <StatCard label="Total cards" value={data.summary.total_cards} />
        <StatCard label="Blocked/revision" value={data.summary.blocked_or_revision} />
        <StatCard label="Ready/scheduled" value={data.summary.ready_or_scheduled} />
        <StatCard label="Published" value={data.summary.published} />
      </div>

      <div className="card stack">
        <div className="card-header">
          <h2>Next actions</h2>
          <button className="secondary small" onClick={load}>Refresh</button>
        </div>
        <ul className="recommendation-list">
          {(data.recommendations || []).map((item) => <li key={item}>{item}</li>)}
        </ul>
      </div>

      <div className="production-board">
        {data.stages.map((stage) => (
          <div className="production-column" key={stage.key}>
            <div className="production-column-head">
              <div>
                <h2>{stage.label}</h2>
                <p>{stage.count} cards • avg {stage.avg_progress}%</p>
              </div>
            </div>
            <p className="stage-description">{stage.description}</p>
            {stage.cards.length === 0 ? (
              <p className="muted small-text">No Shorts here.</p>
            ) : (
              <div className="production-card-list">
                {stage.cards.map((card) => {
                  const form = editing[card.id] || {}
                  return (
                    <div className={`production-card priority-${card.priority}`} key={card.id}>
                      <div className="production-card-top">
                        <button className="link-button" onClick={() => navigate(`#/packages/${card.id}`)}>
                          #{card.id} {card.topic}
                        </button>
                        <span className={`priority-pill ${card.priority}`}>{card.priority}</span>
                      </div>
                      <p>{card.class_level} • {card.subject} • {card.tone}</p>
                      {card.batch_name && <p className="muted">Batch: {card.batch_name}</p>}
                      <div className="board-progress"><span style={{ width: `${card.progress_score}%` }} /></div>
                      <div className="board-card-meta">
                        <span>Progress {card.progress_score}%</span>
                        <span>Trust {card.overall_trust_score || card.trust_score}</span>
                        {card.planned_publish_date && <span>Plan {card.planned_publish_date}</span>}
                        {card.latest_views > 0 && <span>{card.latest_views} views</span>}
                      </div>
                      <details>
                        <summary>Update card</summary>
                        <div className="board-edit-grid">
                          <Select label="Stage" value={form.stage || card.stage} options={stageOptions} onChange={(value) => editCard(card.id, 'stage', value)} />
                          <Select label="Priority" value={form.priority || card.priority} options={priorityOptions} onChange={(value) => editCard(card.id, 'priority', value)} />
                          <Input label="Owner" value={form.owner || ''} onChange={(value) => editCard(card.id, 'owner', value)} />
                          <Input type="date" label="Due date" value={form.due_date || ''} onChange={(value) => editCard(card.id, 'due_date', value)} />
                          <TextArea label="Board notes" value={form.notes || ''} onChange={(value) => editCard(card.id, 'notes', value)} rows={3} wide />
                          <div className="wide button-row">
                            <GuardedButton permission="content:edit" className="secondary small" onClick={() => saveCard(card.id)} disabled={savingId === card.id}>
                              {savingId === card.id ? 'Saving...' : 'Save board card'}
                            </GuardedButton>
                          </div>
                        </div>
                      </details>
                    </div>
                  )
                })}
              </div>
            )}
          </div>
        ))}
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


function DemoSetupPage() {
  const canSeedDemo = useCan('content:create')
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const [message, setMessage] = useState('')

  const load = () => {
    setError('')
    fetchSystemReadiness().then(setData).catch((err) => setError(err.message))
  }

  useEffect(() => {
    load()
  }, [])

  const runSeed = async (resetDemo = false) => {
    if (!canSeedDemo) {
      setError('You do not have permission to seed demo content.')
      return
    }
    setBusy(true)
    setError('')
    setMessage('')
    try {
      const result = await seedDemoData(resetDemo)
      setData({ readiness: result.readiness })
      setMessage(result.demo?.message || 'Demo seed completed.')
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  if (error) return <ErrorCard title="Could not load demo setup" message={error} />
  if (!data) return <Loading />

  const readiness = data.readiness || {}
  const counts = readiness.counts || {}
  const readyItems = readiness.ready_items || []
  const directories = readiness.directory_checks || []
  const providers = readiness.provider_checks || []
  const recommendations = readiness.recommendations || []

  return (
    <section>
      <Header
        title="MVP demo setup"
        subtitle="Seed demo content, verify local storage, and confirm the fallback workflow before daily Shorts production."
        action={<GuardedButton permission="content:create" onClick={() => runSeed(false)} disabled={busy}>{busy ? 'Working...' : 'Seed demo data'}</GuardedButton>}
      />

      {message && <div className="card success-card"><strong>{message}</strong><p className="muted">Open Dashboard, Analytics insights, Provider logs, or a demo package to test the full workflow.</p></div>}

      <div className="stats-grid">
        <StatCard label="Packages" value={counts.packages || 0} />
        <StatCard label="Batches" value={counts.batches || 0} />
        <StatCard label="Calendar items" value={counts.calendar_items || 0} />
        <StatCard label="Analytics entries" value={counts.manual_analytics || 0} />
        <StatCard label="Prompt templates" value={counts.prompt_templates || 0} />
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Readiness checklist</h2><StatusBadge status={readiness.overall_ready ? 'ready' : 'needs_setup'} /></div>
        <ul className="check-list">
          {readyItems.map((item) => <li key={item.label}>[{item.passed ? 'x' : ' '}] {item.label}</li>)}
        </ul>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Recommended actions</h2><span>{recommendations.length} items</span></div>
        <ul className="check-list">
          {recommendations.map((item) => <li key={item}>{item}</li>)}
        </ul>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Storage folder checks</h2><span>{directories.length} folders</span></div>
        <div className="performance-table">
          <div className="performance-head"><span>Folder</span><span>Exists</span><span>Writable</span></div>
          {directories.map((item) => (
            <div className="performance-row" key={item.path}>
              <strong>{item.path}</strong>
              <span>{item.exists ? 'yes' : 'no'}</span>
              <span>{item.writable ? 'yes' : 'no'}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Provider checks</h2><span>{providers.length} providers</span></div>
        <div className="provider-grid">
          {providers.map((provider) => (
            <div className="provider-card" key={provider.name}>
              <div className="provider-top"><h2>{provider.name}</h2><StatusBadge status={provider.available ? 'available' : 'disabled'} /></div>
              <p>{provider.message}</p>
              <span className="muted">In chain: {provider.in_chain ? 'yes' : 'no'}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="card stack">
        <h2>Demo controls</h2>
        <p className="muted">Normal seed is safe and will not duplicate demo rows. Reset only deletes rows tagged as demo seed data.</p>
        <div className="quick-actions">
          <GuardedButton permission="content:create" onClick={() => runSeed(false)} disabled={busy}>Seed demo data</GuardedButton>
          <GuardedButton permission="content:create" className="secondary" onClick={() => runSeed(true)} disabled={busy}>Reset demo data</GuardedButton>
          <button className="secondary" onClick={() => navigate('#/')}>Open dashboard</button>
          <button className="secondary" onClick={() => navigate('#/analytics')}>Open analytics insights</button>
        </div>
      </div>
    </section>
  )
}



function DeploymentGuidePage() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchDeploymentGuide().then(setData).catch((err) => setError(err.message))
  }, [])

  if (error) return <ErrorCard title="Could not load deployment guide" message={error} />
  if (!data) return <Loading />

  const deployment = data.deployment || {}
  const summary = deployment.summary || {}
  const envChecks = deployment.production_env_checks || []
  const fileChecks = deployment.required_file_checks || []
  const gitignoreChecks = deployment.gitignore_checks || []
  const deploymentSteps = deployment.deployment_steps || []

  return (
    <section>
      <Header
        title="Deployment packaging and production configuration"
        subtitle="Use this before sharing a ZIP, pushing to GitHub, or deploying the MVP to a server. It focuses on secrets, storage, auth, CORS, and release packaging."
        action={<a className="button-link" href={deploymentGuideDownloadUrl()} target="_blank" rel="noreferrer">Download guide</a>}
      />

      <div className="stats-grid">
        <StatCard label="Passed" value={summary.pass_count || 0} />
        <StatCard label="Warnings" value={summary.warn_count || 0} />
        <StatCard label="Failures" value={summary.fail_count || 0} />
        <StatCard label="Ready" value={summary.ready_for_package ? 'Yes' : 'Check'} />
      </div>

      <div className="card stack success-card">
        <div className="card-header"><h2>Recommended production overrides</h2><StatusBadge status="production" /></div>
        <p>Keep local development easy, but use stricter settings before any public demo or production deployment.</p>
        <pre>{`ENVIRONMENT=production\nAUTH_REQUIRED=true\nDEFAULT_ADMIN_PASSWORD=replace-with-a-strong-password\nAUTH_COOKIE_SECURE=true\nCORS_ORIGINS=https://your-frontend-domain.example\nDATABASE_PATH=/persistent-storage/app.db\nYOUTUBE_API_ENABLED=false\nYOUTUBE_DRY_RUN=true`}</pre>
        <button className="secondary" onClick={() => copyText(`ENVIRONMENT=production\nAUTH_REQUIRED=true\nDEFAULT_ADMIN_PASSWORD=replace-with-a-strong-password\nAUTH_COOKIE_SECURE=true\nCORS_ORIGINS=https://your-frontend-domain.example\nDATABASE_PATH=/persistent-storage/app.db\nYOUTUBE_API_ENABLED=false\nYOUTUBE_DRY_RUN=true`)}>Copy production env sample</button>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Deployment phases</h2><span>{deploymentSteps.length} phases</span></div>
        <div className="detail-grid">
          {deploymentSteps.map((phase) => (
            <div className="card nested-card stack" key={phase.phase}>
              <h3>{phase.phase}. {phase.title}</h3>
              <ul className="check-list">
                {(phase.items || []).map((item) => <li key={item}>{item}</li>)}
              </ul>
            </div>
          ))}
        </div>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Production environment checks</h2><span>{envChecks.length} keys</span></div>
        <div className="performance-table release-table">
          <div className="performance-head"><span>Status</span><span>Key</span><span>Recommended</span><span>Reason</span></div>
          {envChecks.map((item) => (
            <div className="performance-row" key={item.key}>
              <StatusBadge status={item.status} />
              <strong>{item.key}</strong>
              <span>{item.recommended}</span>
              <span>{item.reason}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Required deployment files</h2><span>{fileChecks.length} files</span></div>
        <div className="performance-table release-table">
          <div className="performance-head"><span>Status</span><span>Path</span><span>Detail</span></div>
          {fileChecks.map((item) => (
            <div className="performance-row" key={item.path}>
              <StatusBadge status={item.status} />
              <strong>{item.path}</strong>
              <span>{item.detail}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="card stack warning-card">
        <div className="card-header"><h2>Protected paths</h2><span>{(deployment.protected_paths || []).length} protected</span></div>
        <p>These should stay out of Git and out of shared source ZIPs unless they are only `.gitkeep` placeholders.</p>
        <div className="performance-table release-table">
          <div className="performance-head"><span>Status</span><span>Pattern</span><span>Detail</span></div>
          {gitignoreChecks.map((item) => (
            <div className="performance-row" key={item.path}>
              <StatusBadge status={item.status} />
              <strong>{item.path}</strong>
              <span>{item.detail}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Packaging commands</h2><StatusBadge status="package" /></div>
        <pre>{(deployment.packaging_commands || []).join('\n')}</pre>
        <button className="secondary" onClick={() => copyText((deployment.packaging_commands || []).join('\n'))}>Copy package commands</button>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Git commands for this step</h2><StatusBadge status="git" /></div>
        <pre>{(deployment.git_commands || []).join('\n')}</pre>
        <button className="secondary" onClick={() => copyText((deployment.git_commands || []).join('\n'))}>Copy Git commands</button>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Recommendations</h2><span>{(deployment.recommendations || []).length} items</span></div>
        <ul className="check-list">
          {(deployment.recommendations || []).map((item) => <li key={item}>{item}</li>)}
        </ul>
      </div>

      <TextCard title="Deployment guide markdown" value={deployment.guide_markdown || ''} />
      <div className="quick-actions">
        <button onClick={() => downloadMarkdown('deployment_production_guide.md', deployment.guide_markdown || '')}>Download markdown from browser</button>
        <button className="secondary" onClick={() => navigate('#/release')}>Open release checklist</button>
        <button className="secondary" onClick={() => navigate('#/setup')}>Open fresh clone setup</button>
      </div>
    </section>
  )
}



function FinalPolishPage() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchFinalPolishReport().then(setData).catch((err) => setError(err.message))
  }, [])

  if (error) return <ErrorCard title="Could not load final MVP polish report" message={error} />
  if (!data) return <Loading />

  const report = data.final_polish || {}
  const summary = report.summary || {}
  const snapshot = report.db_snapshot || {}
  const completed = report.completed_items || []
  const checks = report.project_checks || []
  const qaSteps = report.manual_qa_steps || []

  return (
    <section>
      <Header
        title="Final MVP bug-fix and UI polish"
        subtitle="Use this as the final browser and release pass after v32. It records the production cookie fix, UI polish, manual QA steps, and final Git commands."
        action={<a className="button-link" href={finalPolishReportDownloadUrl()} target="_blank" rel="noreferrer">Download report</a>}
      />

      <div className="stats-grid">
        <StatCard label="Passed" value={summary.pass_count || 0} />
        <StatCard label="Warnings" value={summary.warn_count || 0} />
        <StatCard label="Failures" value={summary.fail_count || 0} />
        <StatCard label="Final ready" value={summary.mvp_final_ready ? 'Yes' : 'Check'} />
      </div>

      <div className="card stack success-card">
        <div className="card-header"><h2>Completed final polish items</h2><span>{completed.length} items</span></div>
        <div className="detail-grid">
          {completed.map((item) => (
            <div className="card nested-card stack" key={item.key}>
              <div className="card-header"><h3>{item.title}</h3><StatusBadge status={item.status} /></div>
              <p>{item.detail}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Project checks</h2><span>{checks.length} checks</span></div>
        <div className="performance-table release-table">
          <div className="performance-head"><span>Status</span><span>Item</span><span>Detail</span><span>Fix</span></div>
          {checks.map((item) => (
            <div className="performance-row" key={item.label}>
              <StatusBadge status={item.status} />
              <strong>{item.label}</strong>
              <span>{item.detail}</span>
              <span>{item.fix || '-'}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Current MVP data snapshot</h2><span>local database</span></div>
        <div className="stats-grid compact-stats">
          {Object.entries(snapshot).map(([key, value]) => (
            <StatCard key={key} label={key.replaceAll('_', ' ')} value={value} />
          ))}
        </div>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Manual QA before final push</h2><span>{qaSteps.length} areas</span></div>
        <div className="detail-grid">
          {qaSteps.map((group) => (
            <div className="card nested-card stack" key={group.area}>
              <h3>{group.area}</h3>
              <ul className="check-list">
                {(group.steps || []).map((step) => <li key={step}>{step}</li>)}
              </ul>
            </div>
          ))}
        </div>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Final Git commands</h2><StatusBadge status="git" /></div>
        <pre>{(report.git_commands || []).join('\n')}</pre>
        <button className="secondary" onClick={() => copyText((report.git_commands || []).join('\n'))}>Copy final commands</button>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Commit message</h2><StatusBadge status="commit" /></div>
        <pre>{`git commit -m "${report.commit_message || 'Finalize MVP bug fixes and UI polish'}"`}</pre>
        <button className="secondary" onClick={() => copyText(`git commit -m "${report.commit_message || 'Finalize MVP bug fixes and UI polish'}"`)}>Copy commit command</button>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Recommendations</h2><span>{(report.recommendations || []).length} items</span></div>
        <ul className="check-list">
          {(report.recommendations || []).map((item) => <li key={item}>{item}</li>)}
        </ul>
      </div>

      <TextCard title="Final MVP polish report markdown" value={report.report_markdown || ''} />
      <div className="quick-actions">
        <button onClick={() => downloadMarkdown('final_mvp_polish_report.md', report.report_markdown || '')}>Download markdown from browser</button>
        <button className="secondary" onClick={() => navigate('#/release')}>Open release checklist</button>
        <button className="secondary" onClick={() => navigate('#/deployment')}>Open deployment guide</button>
      </div>
    </section>
  )
}

function ReleaseChecklistPage() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchReleaseChecklist().then(setData).catch((err) => setError(err.message))
  }, [])

  if (error) return <ErrorCard title="Could not load release checklist" message={error} />
  if (!data) return <Loading />

  const release = data.release || {}
  const summary = release.summary || {}
  const checks = [
    ['Required files', release.file_checks || []],
    ['Required folders', release.directory_checks || []],
    ['.gitignore checks', release.gitignore_checks || []],
    ['.env.example checks', release.env_example_checks || []],
    ['Manual commands', release.manual_command_checks || []]
  ]

  return (
    <section>
      <Header
        title="Production cleanup and release checklist"
        subtitle="Use this page before every GitHub push or shared zip release. It protects local data, generated media, and environment secrets."
        action={<a className="button-link" href={releaseChecklistDownloadUrl()} target="_blank" rel="noreferrer">Download report</a>}
      />

      <div className="stats-grid">
        <StatCard label="Passed" value={summary.pass_count || 0} />
        <StatCard label="Warnings" value={summary.warn_count || 0} />
        <StatCard label="Failures" value={summary.fail_count || 0} />
        <StatCard label="Ready for push" value={summary.ready_for_push ? 'Yes' : 'No'} />
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Recommended Git commands</h2><StatusBadge status="git" /></div>
        <pre>{(release.git_commands || []).join('\n')}</pre>
        <button className="secondary" onClick={() => copyText((release.git_commands || []).join('\n'))}>Copy commands</button>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Commit message for this step</h2><StatusBadge status="commit" /></div>
        <pre>{`git commit -m "${release.commit_message || 'Add fresh clone setup automation'}"`}</pre>
        <button className="secondary" onClick={() => copyText(`git commit -m "${release.commit_message || 'Add fresh clone setup automation'}"`)}>Copy commit command</button>
      </div>

      <div className="card stack warning-card">
        <div className="card-header"><h2>Do not commit these paths</h2><span>{(release.protected_paths || []).length} protected</span></div>
        <ul className="check-list two-column">
          {(release.protected_paths || []).map((item) => <li key={item}><code>{item}</code></li>)}
        </ul>
      </div>

      {checks.map(([title, items]) => (
        <div className="card stack" key={title}>
          <div className="card-header"><h2>{title}</h2><span>{items.length} checks</span></div>
          <div className="performance-table release-table">
            <div className="performance-head"><span>Status</span><span>Item</span><span>Detail</span><span>Fix</span></div>
            {items.map((item) => (
              <div className="performance-row" key={`${title}-${item.label}`}>
                <StatusBadge status={item.status} />
                <strong>{item.label}</strong>
                <span>{item.detail}</span>
                <span>{item.fix || '-'}</span>
              </div>
            ))}
          </div>
        </div>
      ))}

      <div className="card stack">
        <div className="card-header"><h2>Recommendations</h2><span>{(release.recommendations || []).length} items</span></div>
        <ul className="check-list">
          {(release.recommendations || []).map((item) => <li key={item}>{item}</li>)}
        </ul>
      </div>

      <TextCard title="Release report markdown" value={release.report_markdown || ''} />
      <div className="quick-actions">
        <button onClick={() => downloadMarkdown('production_release_checklist.md', release.report_markdown || '')}>Download markdown from browser</button>
        <button className="secondary" onClick={() => navigate('#/demo')}>Open MVP demo setup</button>
        <button className="secondary" onClick={() => navigate('#/provider-logs')}>Open provider logs</button>
      </div>
    </section>
  )
}



function FreshCloneSetupPage() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchSetupGuide().then(setData).catch((err) => setError(err.message))
  }, [])

  if (error) return <ErrorCard title="Could not load fresh clone setup guide" message={error} />
  if (!data) return <Loading />

  const setup = data.setup || {}
  const summary = setup.summary || {}

  return (
    <section>
      <Header
        title="Fresh clone setup automation"
        subtitle="Use this after cloning the GitHub repo on a new laptop or desktop. It keeps setup repeatable and avoids missing env, database, or frontend steps."
        action={<a className="button-link" href={setupGuideDownloadUrl()} target="_blank" rel="noreferrer">Download guide</a>}
      />

      <div className="stats-grid">
        <StatCard label="Passed" value={summary.pass_count || 0} />
        <StatCard label="Warnings" value={summary.warn_count || 0} />
        <StatCard label="Failures" value={summary.fail_count || 0} />
        <StatCard label="Fresh-clone ready" value={summary.fresh_clone_ready ? 'Yes' : 'No'} />
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Fast Windows setup</h2><StatusBadge status="recommended" /></div>
        <pre>{'setup_windows.bat'}</pre>
        <button className="secondary" onClick={() => copyText('setup_windows.bat')}>Copy command</button>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Manual Windows setup commands</h2><span>{(setup.windows_setup_commands || []).length} commands</span></div>
        <pre>{(setup.windows_setup_commands || []).join('\n')}</pre>
        <button className="secondary" onClick={() => copyText((setup.windows_setup_commands || []).join('\n'))}>Copy commands</button>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Step-by-step setup</h2><span>{(setup.setup_steps || []).length} steps</span></div>
        <div className="timeline-list">
          {(setup.setup_steps || []).map((item) => (
            <div className="timeline-item" key={item.step}>
              <strong>{item.step}. {item.title}</strong>
              <p>{item.description}</p>
              <code>{item.command}</code>
            </div>
          ))}
        </div>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Git commands for this step</h2><StatusBadge status="git" /></div>
        <pre>{(setup.git_commands || []).join('\n')}</pre>
        <button className="secondary" onClick={() => copyText((setup.git_commands || []).join('\n'))}>Copy Git commands</button>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Commit message</h2><StatusBadge status="commit" /></div>
        <pre>{`git commit -m "${setup.commit_message || 'Add fresh clone setup automation'}"`}</pre>
        <button className="secondary" onClick={() => copyText(`git commit -m "${setup.commit_message || 'Add fresh clone setup automation'}"`)}>Copy commit command</button>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Required setup files</h2><span>{(setup.required_setup_files || []).length} files</span></div>
        <div className="performance-table release-table">
          <div className="performance-head"><span>Status</span><span>File</span><span>Detail</span><span>Fix</span></div>
          {(setup.required_setup_files || []).map((item) => (
            <div className="performance-row" key={item.label}>
              <StatusBadge status={item.status} />
              <strong>{item.label}</strong>
              <span>{item.detail}</span>
              <span>{item.fix || '-'}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Local machine status</h2><span>{(setup.local_status || []).length} checks</span></div>
        <div className="performance-table release-table">
          <div className="performance-head"><span>Status</span><span>Item</span><span>Detail</span><span>Fix</span></div>
          {(setup.local_status || []).map((item) => (
            <div className="performance-row" key={item.label}>
              <StatusBadge status={item.status} />
              <strong>{item.label}</strong>
              <span>{item.detail}</span>
              <span>{item.fix || '-'}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Recommendations</h2><span>{(setup.recommendations || []).length} items</span></div>
        <ul className="check-list">
          {(setup.recommendations || []).map((item) => <li key={item}>{item}</li>)}
        </ul>
      </div>

      <TextCard title="Fresh clone setup guide markdown" value={setup.guide_markdown || ''} />
      <div className="quick-actions">
        <button onClick={() => downloadMarkdown('fresh_clone_setup_guide.md', setup.guide_markdown || '')}>Download markdown from browser</button>
        <button className="secondary" onClick={() => navigate('#/release')}>Open release checklist</button>
        <button className="secondary" onClick={() => navigate('#/demo')}>Open MVP demo setup</button>
      </div>
    </section>
  )
}



function ProviderSetupGuidePage() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchProviderSetupGuide().then(setData).catch((err) => setError(err.message))
  }, [])

  if (error) return <ErrorCard title="Could not load provider setup guide" message={error} />
  if (!data) return <Loading />

  const guide = data.provider_setup || {}
  const summary = guide.summary || {}
  const currentStatus = guide.current_status || []
  const profiles = guide.provider_profiles || []
  const envProfiles = guide.env_profiles || []
  const envChecks = guide.env_checks || []

  return (
    <section>
      <Header
        title="Real provider adapter setup guide"
        subtitle="Keep this laptop safe with template fallback now, then test Ollama/Transformers/hosted APIs later without breaking the Shorts workflow."
        action={<a className="button-link" href={providerSetupGuideDownloadUrl()} target="_blank" rel="noreferrer">Download guide</a>}
      />

      <div className="stats-grid">
        <StatCard label="Recommended mode" value={summary.recommended_current_mode || 'Laptop-safe'} />
        <StatCard label="Env checks passed" value={summary.env_checks_passed || 0} />
        <StatCard label="Warnings" value={summary.env_checks_warnings || 0} />
        <StatCard label="Provider steps left" value={summary.remaining_provider_steps || 0} />
      </div>

      <div className="card stack success-card">
        <div className="card-header"><h2>Current recommendation</h2><StatusBadge status="safe" /></div>
        <p>For your current laptop, keep Ollama and Transformers disabled and let the template provider generate content packages reliably.</p>
        <pre>{`AI_PROVIDER_CHAIN=transformers,template\nUSE_OLLAMA=false\nUSE_TRANSFORMERS=false\nUSE_HOSTED_LLM=false`}</pre>
        <div className="quick-actions">
          <button className="secondary" onClick={() => navigate('#/settings/ai')}>Open AI fallback status</button>
          <button className="secondary" onClick={() => navigate('#/provider-logs')}>Open provider logs</button>
        </div>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Current provider status</h2><span>{currentStatus.length} providers</span></div>
        <div className="provider-grid">
          {currentStatus.map((provider) => (
            <div className="provider-card" key={provider.name}>
              <div className="provider-top"><h2>{provider.name}</h2><StatusBadge status={provider.available ? 'available' : 'disabled'} /></div>
              <p>{provider.message}</p>
              <span className="muted">In chain: {provider.in_chain ? 'yes' : 'no'}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="detail-grid">
        {profiles.map((profile) => (
          <div className="card stack" key={profile.key}>
            <div className="card-header"><h2>{profile.name}</h2><StatusBadge status={profile.recommended_now ? 'recommended' : 'later'} /></div>
            <p><strong>Best for:</strong> {profile.best_for}</p>
            <p><strong>Install difficulty:</strong> {profile.install_difficulty}</p>
            <p><strong>Risk:</strong> {profile.risk}</p>
            <p className="muted">{profile.notes}</p>
          </div>
        ))}
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Environment profiles</h2><span>{envProfiles.length} profiles</span></div>
        <div className="detail-grid">
          {envProfiles.map((profile) => (
            <div className="card nested-card stack" key={profile.key}>
              <h3>{profile.title}</h3>
              <p>{profile.when_to_use}</p>
              <pre>{profile.env}</pre>
              <button className="secondary" onClick={() => copyText(profile.env)}>Copy env profile</button>
            </div>
          ))}
        </div>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>.env.example provider keys</h2><span>{envChecks.length} checks</span></div>
        <div className="performance-table release-table">
          <div className="performance-head"><span>Status</span><span>Key</span><span>Detail</span></div>
          {envChecks.map((item) => (
            <div className="performance-row" key={item.key}>
              <StatusBadge status={item.status} />
              <strong>{item.key}</strong>
              <span>{item.detail}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Provider test commands</h2><StatusBadge status="test" /></div>
        <pre>{(guide.test_commands || []).join('\n')}</pre>
        <button className="secondary" onClick={() => copyText((guide.test_commands || []).join('\n'))}>Copy test commands</button>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Git commands for this step</h2><StatusBadge status="git" /></div>
        <pre>{(guide.git_commands || []).join('\n')}</pre>
        <button className="secondary" onClick={() => copyText((guide.git_commands || []).join('\n'))}>Copy Git commands</button>
      </div>

      <TextCard title="Provider adapter setup guide markdown" value={guide.guide_markdown || ''} />
      <div className="quick-actions">
        <button onClick={() => downloadMarkdown('real_provider_adapter_setup_guide.md', guide.guide_markdown || '')}>Download markdown from browser</button>
        <button className="secondary" onClick={() => navigate('#/provider-logs')}>Open provider logs</button>
        <button className="secondary" onClick={() => navigate('#/settings/ai')}>Open AI fallback status</button>
      </div>
    </section>
  )
}


function YoutubePublishingChecklistPage() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchYoutubePublishingChecklist().then(setData).catch((err) => setError(err.message))
  }, [])

  if (error) return <ErrorCard title="Could not load YouTube publishing checklist" message={error} />
  if (!data) return <Loading />

  const checklist = data.youtube_publishing || {}
  const summary = checklist.summary || {}
  const phases = checklist.manual_publishing_phases || []
  const packages = checklist.package_readiness || []
  const apiSteps = checklist.api_prep_steps || []
  const envProfiles = checklist.env_profiles || []
  const envChecks = checklist.env_checks || []

  return (
    <section>
      <Header
        title="YouTube manual publishing checklist"
        subtitle="Publish manually from YouTube Studio now, while keeping safe dry-run API placeholders ready for a future integration."
        action={<a className="button-link" href={youtubePublishingChecklistDownloadUrl()} target="_blank" rel="noreferrer">Download checklist</a>}
      />

      <div className="stats-grid">
        <StatCard label="Ready to upload" value={summary.ready_to_upload_count || 0} />
        <StatCard label="Needs gate" value={summary.needs_gate_count || 0} />
        <StatCard label="Scheduled" value={summary.scheduled_count || 0} />
        <StatCard label="Published" value={summary.published_count || 0} />
      </div>

      <div className="card stack success-card">
        <div className="card-header"><h2>Current recommendation</h2><StatusBadge status="manual-first" /></div>
        <p>Use manual YouTube Studio publishing for this MVP. API upload is only prepared as a future dry-run path, so no accidental upload or secret leak is introduced.</p>
        <pre>{`YOUTUBE_API_ENABLED=false\nYOUTUBE_DRY_RUN=true\nYOUTUBE_DEFAULT_PRIVACY_STATUS=private`}</pre>
        <div className="quick-actions">
          <button className="secondary" onClick={() => navigate('#/calendar')}>Open calendar</button>
          <button className="secondary" onClick={() => navigate('#/handoff')}>Open batch handoff</button>
          <button className="secondary" onClick={() => navigate('#/release')}>Open release checklist</button>
        </div>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Manual publishing phases</h2><span>{phases.length} phases</span></div>
        <div className="detail-grid">
          {phases.map((phase) => (
            <div className="card nested-card stack" key={phase.key}>
              <h3>{phase.title}</h3>
              <p>{phase.goal}</p>
              <ul className="check-list">
                {(phase.items || []).map((item) => <li key={item}>{item}</li>)}
              </ul>
            </div>
          ))}
        </div>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Package readiness for YouTube</h2><span>{packages.length} packages checked</span></div>
        {packages.length === 0 && <p className="muted">Create and approve at least one package to see upload readiness here.</p>}
        {packages.length > 0 && (
          <div className="performance-table youtube-table">
            <div className="performance-head"><span>Package</span><span>Trust</span><span>Gate</span><span>Calendar</span><span>Next action</span></div>
            {packages.map((item) => (
              <div className="performance-row" key={item.id}>
                <strong>#{item.id} {item.best_title}</strong>
                <span>{item.trust_score}</span>
                <StatusBadge status={item.gate_status} />
                <span>{item.calendar_status}{item.planned_publish_date ? ` • ${item.planned_publish_date}` : ''}</span>
                <span>{item.next_action}</span>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="card stack warning-card">
        <div className="card-header"><h2>Optional API integration preparation</h2><StatusBadge status="future" /></div>
        <div className="timeline-list">
          {apiSteps.map((item) => (
            <div className="timeline-item" key={item.step}>
              <strong>{item.step}. {item.title}</strong>
              <p>{item.description}</p>
              <code>{item.owner_action}</code>
            </div>
          ))}
        </div>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>YouTube environment profiles</h2><span>{envProfiles.length} profiles</span></div>
        <div className="detail-grid">
          {envProfiles.map((profile) => (
            <div className="card nested-card stack" key={profile.key}>
              <h3>{profile.title}</h3>
              <p>{profile.when_to_use}</p>
              <pre>{profile.env}</pre>
              <button className="secondary" onClick={() => copyText(profile.env)}>Copy env profile</button>
            </div>
          ))}
        </div>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>.env.example YouTube keys</h2><span>{envChecks.length} checks</span></div>
        <div className="performance-table release-table">
          <div className="performance-head"><span>Status</span><span>Key</span><span>Detail</span><span>Fix</span></div>
          {envChecks.map((item) => (
            <div className="performance-row" key={item.key}>
              <StatusBadge status={item.status} />
              <strong>{item.key}</strong>
              <span>{item.detail}</span>
              <span>{item.status === 'pass' ? '-' : 'Add this key to .env.example'}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="card stack">
        <div className="card-header"><h2>Git commands for this step</h2><StatusBadge status="git" /></div>
        <pre>{(checklist.git_commands || []).join('\n')}</pre>
        <button className="secondary" onClick={() => copyText((checklist.git_commands || []).join('\n'))}>Copy Git commands</button>
      </div>

      <TextCard title="YouTube publishing checklist markdown" value={checklist.guide_markdown || ''} />
      <div className="quick-actions">
        <button onClick={() => downloadMarkdown('youtube_manual_publishing_checklist.md', checklist.guide_markdown || '')}>Download markdown from browser</button>
        <button className="secondary" onClick={() => navigate('#/calendar')}>Open calendar</button>
        <button className="secondary" onClick={() => navigate('#/analytics')}>Open analytics</button>
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
  return <div className="empty-state"><h3>No packages yet</h3><p>Create your first Shorts package using the sample Science topic.</p><GuardedButton permission="content:create" onClick={() => navigate('#/new')}>Create first package</GuardedButton></div>
}

function ErrorCard({ title, message, action = null }) {
  return (
    <div className="card error-card">
      <h2>{title}</h2>
      <p>{message}</p>
      {action && <div className="button-row">{action}</div>}
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
