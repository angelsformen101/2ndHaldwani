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
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method === 'POST') {
    try {
      let payload = req.body;
      if (typeof payload === 'string') {
        payload = JSON.parse(payload);
      }

      if (!payload || !payload.type) {
        return res.status(400).json({ error: 'Invalid click tracking payload' });
      }

      const logEntry = {
        id: Date.now() + '-' + Math.random().toString(36).substr(2, 6),
        type: payload.type, // 'call' or 'whatsapp'
        label: payload.label || 'Direct Click',
        page: payload.page || 'index.html',
        url: payload.url || '',
        duration: typeof payload.duration === 'number' ? payload.duration : 0,
        timestamp: payload.timestamp || new Date().toISOString()
      };

      const logs = getLogs();
      logs.unshift(logEntry);
      saveLogs(logs);

      return res.status(200).json({ success: true, entry: logEntry });
    } catch (err) {
      return res.status(500).json({ error: err.message });
    }
  }

  return res.status(405).json({ error: 'Method Not Allowed' });
};
