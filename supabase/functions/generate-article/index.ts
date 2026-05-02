import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const ANTHROPIC_KEY = Deno.env.get('ANTHROPIC_API_KEY')!
const UNSPLASH_KEY  = Deno.env.get('UNSPLASH_ACCESS_KEY')
const SUPABASE_URL  = Deno.env.get('SUPABASE_URL')!
const SERVICE_KEY   = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!

// ── Theme rotation — 10 slots, 2 per week, 5-week cycle ──
const THEMES = [
  { week: 0, slot: 0, category: 'brand',       topic: 'Brand Identity',       angle: 'visual identity systems, logo construction, brand strategy for global companies' },
  { week: 0, slot: 1, category: 'brand',       topic: 'Brand Systems',        angle: 'design tokens, scalable brand architecture, brand guidelines that engineers can use' },
  { week: 1, slot: 0, category: 'interface',   topic: 'Interface Design',     angle: 'UI patterns, interaction design, building digital products people actually use' },
  { week: 1, slot: 1, category: 'interface',   topic: 'Digital Products',     angle: 'product strategy, UX research, digital transformation for established brands' },
  { week: 2, slot: 0, category: 'process',     topic: 'Creative Process',     angle: 'how great creative work gets made, briefing, iteration, creative direction' },
  { week: 2, slot: 1, category: 'process',     topic: 'Client Collaboration', angle: 'working with clients, managing creative feedback, building trust in a design relationship' },
  { week: 3, slot: 0, category: 'engineering', topic: 'Frontend Engineering', angle: 'CSS architecture, design-to-code, performance, building what designers design' },
  { week: 3, slot: 1, category: 'engineering', topic: 'Design Systems',       angle: 'building and maintaining design systems at scale, token pipelines, component governance' },
  { week: 4, slot: 0, category: 'opinion',     topic: 'Industry Perspective', angle: 'honest takes on the design industry, what is changing and what matters' },
  { week: 4, slot: 1, category: 'opinion',     topic: 'Future of Design',     angle: 'AI in design, the role of the creative director, where brand design is going' },
]

function getTheme(overrideIndex?: number) {
  if (overrideIndex !== undefined) return THEMES[overrideIndex % THEMES.length]
  const now         = new Date()
  const msPerWeek   = 7 * 24 * 60 * 60 * 1000
  const weekCycle   = Math.floor(now.getTime() / msPerWeek) % 5
  const slot        = now.getDay() === 4 ? 1 : 0  // Thursday = slot 1, Monday = slot 0
  return THEMES.find(t => t.week === weekCycle && t.slot === slot) ?? THEMES[0]
}

async function callClaude(theme: typeof THEMES[0]) {
  const system = `You are a senior writer for Parallax Studio — a premium brand and digital design agency. Parallax has built brand systems for BMW, Biblica, Sportradar, Vestas, Nissan, and Accenture.

Audience: design directors, brand managers, founders, and product leads at mid-to-large organisations. Sophisticated, time-poor, allergic to fluff.

Voice: Direct. Authoritative. Specific. No generic advice. Write like someone who has done this at scale. Think Stripe blog, Figma blog — not generic Medium posts.

Article structure:
- Lead paragraph: strong hook, 2-3 sentences, no throat-clearing
- 4-5 H2 sections with substantive, specific content
- At least one blockquote and one practical numbered or bulleted list
- Tight closing paragraph with a clear point of view
- Length: 800-1500 words

CRITICAL: Respond with a valid JSON object only. No markdown fences, no preamble. Exactly this shape:
{
  "title": "Compelling specific article title",
  "slug": "url-friendly-slug",
  "excerpt": "2-3 sentence summary. Specific, not generic.",
  "category": "brand|interface|engineering|process|opinion",
  "tags": ["Tag 1", "Tag 2", "Tag 3", "Tag 4"],
  "read_time": "X min read",
  "unsplash_search": "2-3 word image search term",
  "body": "Full article body in markdown. Use ## for H2 sections, > for blockquotes, **bold** for emphasis."
}`

  const user = `Topic: ${theme.topic}
Focus: ${theme.angle}

Write an article that gives design directors and brand leaders a specific, valuable insight they can act on. Draw on the expertise Parallax has from building brand systems for global companies. Genuine expertise — not content marketing.`

  const res = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type':    'application/json',
      'x-api-key':       ANTHROPIC_KEY,
      'anthropic-version': '2023-06-01',
    },
    body: JSON.stringify({
      model:      'claude-opus-4-7',
      max_tokens: 4096,
      system,
      messages: [{ role: 'user', content: user }],
    }),
  })

  if (!res.ok) throw new Error(`Claude API ${res.status}: ${await res.text()}`)

  const data = await res.json()
  const text = data.content[0].text.trim()

  try {
    return JSON.parse(text)
  } catch {
    const match = text.match(/\{[\s\S]*\}/)
    if (match) return JSON.parse(match[0])
    throw new Error('Could not parse Claude response as JSON')
  }
}

async function getUnsplashImage(term: string): Promise<{ url: string; credit: string } | null> {
  if (!UNSPLASH_KEY || UNSPLASH_KEY === 'pending') return null
  try {
    const res  = await fetch(
      `https://api.unsplash.com/search/photos?query=${encodeURIComponent(term)}&per_page=1&orientation=landscape`,
      { headers: { Authorization: `Client-ID ${UNSPLASH_KEY}` } }
    )
    const data  = await res.json()
    const photo = data.results?.[0]
    if (!photo) return null
    return {
      url:    photo.urls.regular,
      credit: `Photo by ${photo.user.name} on Unsplash`,
    }
  } catch {
    return null
  }
}

serve(async (req) => {
  const body         = req.method === 'POST' ? await req.json().catch(() => ({})) : {}
  const themeIndex   = body.theme_index  // optional — for manual test triggers

  try {
    const theme   = getTheme(themeIndex)
    const article = await callClaude(theme)
    const image   = await getUnsplashImage(article.unsplash_search ?? theme.topic)

    const db = createClient(SUPABASE_URL, SERVICE_KEY)
    const { data: ws } = await db.from('workspaces').select('id').limit(1).single()

    const { data, error } = await db.from('articles').insert({
      workspace_id:   ws?.id,
      title:          article.title,
      slug:           article.slug,
      excerpt:        article.excerpt,
      category:       article.category,
      tags:           article.tags,
      read_time:      parseInt(String(article.read_time)) || 5,
      body:           article.body,
      author:         'Parallax Studio',
      hero_image_url: image?.url ?? null,
      status:         'draft',
    }).select().single()

    if (error) throw new Error(`DB insert: ${error.message}`)

    return new Response(JSON.stringify({
      ok:         true,
      article_id: data.id,
      title:      article.title,
      category:   article.category,
      theme:      theme.topic,
    }), { headers: { 'Content-Type': 'application/json' } })

  } catch (err) {
    console.error(err)
    return new Response(
      JSON.stringify({ ok: false, error: err.message }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    )
  }
})
