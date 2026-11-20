const fs = require('fs');
const path = require('path');

const CONFIG_PATH = path.join(process.cwd(), 'js', 'contacts-config.js');

function readConfig() {
  try {
    if (fs.existsSync(CONFIG_PATH)) {
      const content = fs.readFileSync(CONFIG_PATH, 'utf8');
      const jsonMatch = content.match(/window\.SITE_CONTACTS_CONFIG\s*=\s*(\{[\s\S]*?\});/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[1]);
      }
    }
  } catch (err) {
    console.error('Error reading contacts-config.js:', err);
  }
  return {
    master: { call: '+919876543210', whatsapp: '919876543210' },
    pages: {}
  };
}

function writeConfig(data) {
  try {
    const formatted = `// Master Contacts Configuration for CityHaldwani.com\n// Managed dynamically via CityHaldwani.com Admin Panel\nwindow.SITE_CONTACTS_CONFIG = ${JSON.stringify(data, null, 2)};\n`;
    fs.writeFileSync(CONFIG_PATH, formatted, 'utf8');
    return true;
  } catch (err) {
    console.error('Error writing contacts-config.js:', err);
    return false;
  }
}

module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method === 'GET') {
    const config = readConfig();
    return res.status(200).json(config);
  }

  if (req.method === 'POST') {
    try {
      const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
      if (!body) {
        return res.status(400).json({ error: 'Missing request body' });
      }

      const current = readConfig();

      if (body.master) {
        current.master = {
          call: body.master.call || current.master.call,
          whatsapp: body.master.whatsapp || current.master.whatsapp
        };
      }

      if (body.pages) {
        current.pages = { ...current.pages, ...body.pages };
      }

      const success = writeConfig(current);
      return res.status(200).json({ success: success, config: current });
    } catch (e) {
      return res.status(500).json({ error: e.message });
    }
  }

  return res.status(405).json({ error: 'Method Not Allowed' });
};
