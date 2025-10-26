document.getElementById('load').addEventListener('click', async () => {
  const pre = document.getElementById('json')
  pre.textContent = 'Loading...'
  try {
    const res = await fetch('result.json')
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()
    pre.textContent = JSON.stringify(data, null, 2)
  } catch (err) {
    pre.textContent = 'Could not load result.json: ' + err.message
  }
})
