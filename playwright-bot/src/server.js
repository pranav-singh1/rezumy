import http from 'http'
import { prefillAndOptionallySubmit } from './bot.js'

const PORT = Number(process.env.PORT || 4000)

const server = http.createServer(async (req, res) => {
  if (req.method === 'POST' && req.url === '/apply') {
    try {
      let body = ''
      req.on('data', chunk => { body += chunk })
      req.on('end', async () => {
        try {
          const parsed = JSON.parse(body || '{}')
          const applyUrl = parsed.applyUrl
          const payload = parsed.payload || {}
          const actuallySubmit = Boolean(parsed.actuallySubmit)
          if (!applyUrl) {
            res.writeHead(400, { 'Content-Type': 'application/json' })
            res.end(JSON.stringify({ error: 'applyUrl is required' }))
            return
          }
          await prefillAndOptionallySubmit(applyUrl, payload, actuallySubmit)
          res.writeHead(200, { 'Content-Type': 'application/json' })
          res.end(JSON.stringify({ ok: true }))
        } catch (e) {
          res.writeHead(500, { 'Content-Type': 'application/json' })
          res.end(JSON.stringify({ error: e?.message || String(e) }))
        }
      })
    } catch (e) {
      res.writeHead(500, { 'Content-Type': 'application/json' })
      res.end(JSON.stringify({ error: e?.message || String(e) }))
    }
    return
  }

  res.writeHead(404, { 'Content-Type': 'application/json' })
  res.end(JSON.stringify({ error: 'Not found' }))
})

server.listen(PORT, () => {
  // eslint-disable-next-line no-console
  console.log(`Playwright bot server listening on :${PORT}`)
}) 