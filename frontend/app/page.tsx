'use client'
import { useState } from 'react'
import axios from 'axios'

const BACKEND = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'

export default function Home() {
  const [file, setFile] = useState<File | null>(null)
  const [query, setQuery] = useState('Software Engineer Intern')
  const [jobs, setJobs] = useState<any[]>([])
  const [ranked, setRanked] = useState<any[]>([])
  const [parsed, setParsed] = useState<any | null>(null)

  async function upload() {
    if (!file) return
    const formData = new FormData()
    formData.append('file', file)
    const res = await axios.post(`${BACKEND}/resumes/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    setParsed(res.data.parsed)
  }

  async function search() {
    const res = await axios.get(`${BACKEND}/jobs/search`, { params: { q: query, num: 20 }})
    setJobs(res.data.results)
  }

  async function match() {
    const resumeText = Object.entries(parsed || {}).map(([k, v]) => String(v)).join(' ')
    const res = await axios.post(`${BACKEND}/applications/match`, { resume_text: resumeText, jobs })
    setRanked(res.data.ranked)
  }

  return (
    <main className="max-w-4xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-semibold">Rezumy</h1>
      <div className="grid gap-3">
        <input type="file" onChange={e => setFile(e.target.files?.[0] || null)} />
        <button className="px-3 py-2 border rounded" onClick={upload}>Upload and parse resume</button>
      </div>
      {parsed && (
        <pre className="bg-gray-100 p-3 rounded text-sm overflow-auto">{JSON.stringify(parsed, null, 2)}</pre>
      )}
      <div className="grid gap-3">
        <input className="border px-3 py-2 rounded" value={query} onChange={e => setQuery(e.target.value)} placeholder="Search query" />
        <button className="px-3 py-2 border rounded" onClick={search}>Search jobs</button>
      </div>
      {!!jobs.length && <button className="px-3 py-2 border rounded" onClick={match}>Match and rank</button>}
      {!!ranked.length && (
        <div className="space-y-2">
          {ranked.map((j, i) => (
            <div key={i} className="border rounded p-3">
              <div className="font-medium">{j.title} • {j.company} • score {j.score.toFixed(3)}</div>
              <div className="text-sm opacity-80">{j.location || 'Location N/A'}</div>
              <a className="text-blue-600 underline" href={j.link || '#'} target="_blank">Apply link</a>
            </div>
          ))}
        </div>
      )}
    </main>
  )
}
