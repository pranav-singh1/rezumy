import { chromium } from 'playwright'

export async function prefillAndOptionallySubmit(applyUrl, payload, actuallySubmit = false) {
  const browser = await chromium.launch({ headless: true })
  const page = await browser.newPage()
  await page.goto(applyUrl, { waitUntil: 'domcontentloaded' })

  try { if (payload.fullName) await page.fill('input[name="name"], input[name="full_name"]', payload.fullName) } catch {}
  try { if (payload.email) await page.fill('input[type="email"]', payload.email) } catch {}
  try { if (payload.phone) await page.fill('input[type="tel"]', payload.phone) } catch {}

  if (payload.resumePath) {
    const [fileChooser] = await Promise.all([
      page.waitForEvent('filechooser'),
      page.click('input[type="file"]')
    ])
    await fileChooser.setFiles(payload.resumePath)
  }

  if (payload.coverLetter) {
    const area = await page.$('textarea, [contenteditable="true"]')
    if (area) await area.fill(payload.coverLetter)
  }

  if (actuallySubmit) {
    const submit = await page.$('button[type="submit"], button:has-text("Submit")')
    if (submit) await submit.click()
  }

  await browser.close()
} 