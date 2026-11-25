import { useEffect, useState } from 'react'
import { SERVICES } from './api.js'

const box = { border: '1px solid #ccc', borderRadius: 8, padding: 16, marginBottom: 16 }

export default function App() {
  const [status, setStatus] = useState({})
  const [message, setMessage] = useState('')
  const [author, setAuthor] = useState('')
  const [rows, setRows] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    Object.entries(SERVICES).forEach(([name, url]) => {
      fetch(`${url}/health`)
        .then(r => r.json())
        .then(() => setStatus(s => ({ ...s, [name]: 'עובד' })))
        .catch(() => setStatus(s => ({ ...s, [name]: 'לא עונה' })))
    })
    load()
  }, [])

  async function load() {
    try {
      const r = await fetch(`${SERVICES.core}/api/core/infra-check`)
      const data = await r.json()
      if (!r.ok) throw new Error(data.detail)
      setRows(data); setError('')
    } catch (e) { setError(String(e.message || e)) }
  }

  async function send(e) {
    e.preventDefault()
    const r = await fetch(`${SERVICES.core}/api/core/infra-check`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, author: author || 'anonymous' }),
    })
    const data = await r.json()
    if (!r.ok) { setError(data.detail); return }
    setMessage(''); load()
  }

  return (
    <main style={{ fontFamily: 'Arial, sans-serif', maxWidth: 720, margin: '40px auto', padding: 16 }}>
      <h1>בדיקת תשתית – Moodle</h1>
      <section style={box}>
        <h2>מצב השירותים</h2>
        <ul>
          {Object.keys(SERVICES).map(n => <li key={n}>backend-{n}: {status[n] || 'בודק…'}</li>)}
        </ul>
      </section>
      <section style={box}>
        <h2>Frontend → Backend → Supabase</h2>
        <form onSubmit={send}>
          <input placeholder="שם" value={author} onChange={e => setAuthor(e.target.value)} />{' '}
          <input placeholder="הודעה" value={message} onChange={e => setMessage(e.target.value)} required />{' '}
          <button>שמירה ב-Supabase</button>
        </form>
        {error && <p style={{ color: 'crimson' }}>שגיאה: {error}</p>}
        <ul>{rows.map(r => <li key={r.id}>{r.author}: {r.message} ({new Date(r.created_at).toLocaleString('he-IL')})</li>)}</ul>
      </section>
      <p>כל קבוצה מוסיפה את המסכים שלה בתיקייה src/features/&lt;תחום&gt;.</p>
    </main>
  )
}
