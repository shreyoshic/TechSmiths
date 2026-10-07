const RAG_API = window.RAG_API || '';

export async function retrieveMX01Evidence(query, topK = 5) {
  const res = await fetch(`${RAG_API}/api/mx-01/evidence`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({query, top_k: topK})
  });
  if (!res.ok) throw new Error(`RAG request failed: ${res.status}`);
  return res.json();
}

export function renderEvidence(container, payload) {
  container.innerHTML = '';
  const title = document.createElement('h3');
  title.textContent = 'MX-01 Evidence';
  container.appendChild(title);

  if (!payload.evidence?.length) {
    const empty = document.createElement('p');
    empty.textContent = 'No relevant verified evidence was retrieved.';
    container.appendChild(empty);
    return;
  }

  for (const item of payload.evidence) {
    const card = document.createElement('article');
    card.className = 'evidence-card';
    card.innerHTML = `
      <div><strong>${escapeHtml(item.evidence_id || 'MX-01')}</strong>
      <span class="score">similarity ${item.score}</span></div>
      <p>${escapeHtml(item.text)}</p>
      <small>Source: <code>${escapeHtml(item.source_reference)}</code><br>Location: ${escapeHtml(item.location)}</small>
    `;
    container.appendChild(card);
  }
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
}
