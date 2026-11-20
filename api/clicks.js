const fs = require('fs');
const path = require('path');

const LOGS_FILE = path.join(process.cwd(), 'data_clicks.json');

function getLogs() {
  try {
    if (fs.existsSync(LOGS_FILE)) {
      return JSON.parse(fs.readFileSync(LOGS_FILE, 'utf8'));
    }
  } catch (e) {}
  return [];
}

function saveLogs(logs) {
  try {
    fs.writeFileSync(LOGS_FILE, JSON.stringify(logs.slice(0, 2000), null, 2), 'utf8');
  } catch (e) {}
}

module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // GET: Fetch logs and page breakdown
  if (req.method === 'GET') {
    const logs = getLogs();
    
    // Group statistics by page
    const byPage = {};
    let totalCall = 0;
    let totalWa = 0;

    logs.forEach(log => {
      const p = log.page || 'Unknown';
      if (!byPage[p]) {
        byPage[p] = { page: p, call: 0, whatsapp: 0, total: 0, avgDuration: 0, totalDuration: 0 };
      }
      if (log.type === 'call') {
        byPage[p].call++;
        totalCall++;
      } else if (log.type === 'whatsapp') {
        byPage[p].whatsapp++;
        totalWa++;
      }
      byPage[p].total++;
      byPage[p].totalDuration += (log.duration || 0);
    });

    Object.keys(byPage).forEach(k => {
      byPage[k].avgDuration = byPage[k].total > 0 ? Math.round(byPage[k].totalDuration / byPage[k].total) : 0;
    });

    return res.status(200).json({
      summary: {
        totalClicks: logs.length,
        totalCalls: totalCall,
        totalWhatsApp: totalWa,
        activePagesCount: Object.keys(byPage).length
      },
      pageBreakdown: Object.values(byPage),
      logs: logs
    });
  }

  // POST or DELETE: Purge/Clear history (selective: single page, array of pages, or all)
  if (req.method === 'POST' || req.method === 'DELETE') {
    try {
      let body = req.body;
      if (typeof body === 'string') {
        try { body = JSON.parse(body); } catch(e) { body = {}; }
      }
      body = body || {};

      let logs = getLogs();
      const initialCount = logs.length;

      // Case 1: Clear all history
      if (body.all === true || body.action === 'clear_all') {
        logs = [];
        saveLogs(logs);
        return res.status(200).json({ success: true, message: 'All click analytics cleared', cleared: initialCount });
      }

      // Case 2: Clear specific single page
      if (body.page) {
        logs = logs.filter(l => l.page !== body.page);
        saveLogs(logs);
        return res.status(200).json({ success: true, message: `Cleared history for page ${body.page}`, cleared: initialCount - logs.length });
      }

      // Case 3: Clear multiple selected pages
      if (Array.isArray(body.pages) && body.pages.length > 0) {
        const pagesToClear = new Set(body.pages);
        logs = logs.filter(l => !pagesToClear.has(l.page));
        saveLogs(logs);
        return res.status(200).json({ success: true, message: `Cleared history for ${body.pages.length} selected pages`, cleared: initialCount - logs.length });
      }

      return res.status(400).json({ error: 'Please specify "page", "pages" array, or "all: true" to clear history.' });
    } catch (e) {
      return res.status(500).json({ error: e.message });
    }
  }

  return res.status(405).json({ error: 'Method Not Allowed' });
};
