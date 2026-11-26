const { createHash } = require('node:crypto');
const fs = require('node:fs/promises');
const path = require('node:path');
const sharp = require('sharp');

const root = __dirname;
const review = path.join(root, 'review');
const width = 1020;
const height = 893;
const panelWidth = 315;
const panelHeight = 242;

function blindOrder(id) {
  return createHash('sha256').update(`onestep-2026-11-26/${id}`).digest('hex');
}

async function prepare() {
  const protocol = JSON.parse(await fs.readFile(path.join(root, 'experiment.json'), 'utf8'));
  const available = new Set(await fs.readdir(path.join(root, 'raw')));
  const groups = new Map();
  for (const job of protocol.plan) {
    const name = `${job.case}-${job.repeat}`;
    if (!groups.has(name)) groups.set(name, []);
    groups.get(name).push(job);
  }

  await fs.mkdir(review, { recursive: true });
  const key = {};
  for (const [name, jobs] of groups) {
    if (!jobs.every(job => available.has(`${job.id}.png`))) continue;

    jobs.sort((a, b) => blindOrder(a.id).localeCompare(blindOrder(b.id)));
    const images = [];
    const labels = [];
    key[name] = {};
    for (const [index, job] of jobs.entries()) {
      const label = String.fromCharCode(65 + index);
      const left = 24 + index % 3 * 329;
      const top = 16 + Math.floor(index / 3) * 290;
      const asset = path.join(root, 'raw', `${job.id}.png`);
      const input = await sharp(asset).flatten({ background: '#fbf9f2' })
        .resize(panelWidth, panelHeight, { fit: 'contain', background: '#fbf9f2' })
        .png().toBuffer();
      images.push({ input, left, top });
      labels.push(`<text x="${left + 150}" y="${top + 271}">${label}</text>`);
      key[name][label] = job.id;
    }

    const overlay = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}">
      <g font-family="Arial" font-weight="700" font-size="18" fill="#232226">${labels.join('')}</g></svg>`);
    await sharp({ create: { width, height, channels: 3, background: '#fbf9f2' } })
      .composite([...images, { input: overlay }])
      .jpeg({ quality: 92 }).toFile(path.join(review, `${name}.jpg`));
  }
  await fs.writeFile(path.join(root, 'review-key.json'), `${JSON.stringify(key, null, 2)}\n`, 'utf8');
  process.stdout.write(`Prepared ${Object.keys(key).length} complete blind sheets.\n`);
}

prepare().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
