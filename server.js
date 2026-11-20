const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = process.env.PORT || 3002;
const BASE_DIR = __dirname;

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.txt': 'text/plain; charset=utf-8',
  '.xml': 'application/xml; charset=utf-8'
};

const LOCATIONS = [
  'nainital', 'bhimtal', 'almora', 'ramnagar', 'haldwani',
  'kaladhungi', 'rudrapur', 'kathgodam', 'kashipur', 'bajpur',
  'khatima', 'sitarganj', 'kichha', 'jim-corbett', 'bhowali'
];

function send404(res) {
  const p404 = path.join(BASE_DIR, '404.html');
  if (fs.existsSync(p404)) {
    res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(fs.readFileSync(p404));
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('404 Not Found');
  }
}

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  let pathname = decodeURIComponent(parsedUrl.pathname);

  // Security: Block direct /admin and /admin/
  if (pathname === '/admin' || pathname === '/admin/' || pathname.startsWith('/admin/')) {
    return send404(res);
  }

  // Rewrite /admin! and /admin!/
  if (pathname === '/admin!' || pathname === '/admin!/') {
    const adminPath = path.join(BASE_DIR, 'admin!.html');
    if (fs.existsSync(adminPath)) {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      return res.end(fs.readFileSync(adminPath));
    }
  }

  // API handlers
  if (pathname.startsWith('/api/')) {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      req.body = body;
      try { req.body = JSON.parse(body); } catch(e) {}

      // Mock Express response methods
      res.status = function(code) {
        this.statusCode = code;
        return this;
      };
      res.json = function(data) {
        this.setHeader('Content-Type', 'application/json; charset=utf-8');
        this.end(JSON.stringify(data));
      };

      if (pathname === '/api/config') {
        return require('./api/config.js')(req, res);
      }
      if (pathname === '/api/track') {
        return require('./api/track.js')(req, res);
      }
      if (pathname === '/api/clicks') {
        return require('./api/clicks.js')(req, res);
      }

      return send404(res);
    });
    return;
  }

  // Resolve static files
  let safePath = pathname.replace(/^(\.\.[\/\\])+/, '').replace(/^[\/\\]+/, '');
  if (!safePath) safePath = 'index.html';

  let filePath = path.join(BASE_DIR, safePath);
  let publicPath = path.join(BASE_DIR, 'public', safePath);

  // Check direct file in root
  if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
    const ext = path.extname(filePath).toLowerCase();
    res.writeHead(200, { 'Content-Type': MIME_TYPES[ext] || 'application/octet-stream' });
    return fs.createReadStream(filePath).pipe(res);
  }

  // Check direct file in public
  if (fs.existsSync(publicPath) && fs.statSync(publicPath).isFile()) {
    const ext = path.extname(publicPath).toLowerCase();
    res.writeHead(200, { 'Content-Type': MIME_TYPES[ext] || 'application/octet-stream' });
    return fs.createReadStream(publicPath).pipe(res);
  }

  // Check clean URLs with .html in root
  if (fs.existsSync(filePath + '.html') && fs.statSync(filePath + '.html').isFile()) {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    return fs.createReadStream(filePath + '.html').pipe(res);
  }

  // Check location aliases (e.g. /nainital -> /locations/nainital.html)
  const cleanName = pathname.replace(/^\/+/, '').replace(/\.html$/, '');
  if (LOCATIONS.includes(cleanName)) {
    const locPath = path.join(BASE_DIR, 'locations', cleanName + '.html');
    if (fs.existsSync(locPath)) {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      return fs.createReadStream(locPath).pipe(res);
    }
  }

  // Otherwise 404
  return send404(res);
});

server.listen(PORT, () => {
  console.log(`CityHaldwani.com local server running at http://localhost:${PORT}`);
  console.log(`- Admin Panel: http://localhost:${PORT}/admin!`);
});
