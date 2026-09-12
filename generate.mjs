#!/usr/bin/env node
/**
 * GitHub Jet Heatmap Generator
 * 
 * Generates an animated "jet over contribution grid" SVG using a GitHub
 * user's REAL contribution calendar (last 34 weeks, 34 columns x 7 rows).
 * 
 * Works both:
 * 1. With GH_TOKEN / GITHUB_TOKEN via GitHub GraphQL API (in GitHub Actions)
 * 2. Without any token by parsing public contribution data directly!
 */

import fs from "node:fs";
import path from "node:path";

const USERNAME = process.env.GH_USERNAME || "khushboocodes";
const TOKEN = process.env.GH_TOKEN || process.env.GITHUB_TOKEN;
const OUTPUT = process.env.OUTPUT_PATH || "dist/github-jet.svg";

const COLS = 34; // 34 weeks
const ROWS = 7;  // 7 days per week
const CELL = 11;
const STEP = 14; // cell + gap
const GRID_X = 20;
const GRID_Y = 15;
const WIDTH = 513;
const HEIGHT = 170;
const JET_X_START = 35;
const JET_X_END = 478;
const LOOP_DUR = 20; // seconds per pass
const MAX_TARGETS = 12; // top busy days to shoot
const FLASH_COLOR = "#39d353";
const BULLET_COLOR = "#7ee787";
const BLAST_COLOR = "#56d364";
const PAD_Y = 128; // bullet launch line

const GITHUB_COLORS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"];

const GRAPHQL_QUERY = `
  query($login: String!) {
    user(login: $login) {
      contributionsCollection {
        contributionCalendar {
          weeks {
            contributionDays {
              date
              contributionCount
              color
            }
          }
        }
      }
    }
  }
`;

async function fetchWeeksGraphQL(token) {
  const res = await fetch("https://api.github.com/graphql", {
    method: "POST",
    headers: {
      Authorization: `bearer ${token}`,
      "Content-Type": "application/json",
      "User-Agent": "GitHub-Jet-Heatmap",
    },
    body: JSON.stringify({ query: GRAPHQL_QUERY, variables: { login: USERNAME } }),
  });
  if (!res.ok) {
    throw new Error(`GraphQL API error ${res.status}: ${await res.text()}`);
  }
  const json = await res.json();
  if (json.errors) throw new Error(JSON.stringify(json.errors));
  return json.data.user.contributionsCollection.contributionCalendar.weeks;
}

async function fetchWeeksScrape() {
  const url = `https://github.com/users/${USERNAME}/contributions`;
  const res = await fetch(url, {
    headers: {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
      Accept: "text/html",
    },
  });
  if (!res.ok) {
    throw new Error(`Failed to fetch public contributions from ${url}: ${res.status}`);
  }
  const html = await res.text();
  
  // Extract all contribution day cells
  const dayRegex = /<td[^>]+data-date="([^"]+)"[^>]+data-level="([^"]+)"[^>]*>/g;
  const days = [];
  let match;
  while ((match = dayRegex.exec(html)) !== null) {
    const date = match[1];
    const level = Math.min(4, Math.max(0, parseInt(match[2], 10) || 0));
    // Estimate or map count from level
    const count = level === 0 ? 0 : level === 1 ? 1 : level === 2 ? 4 : level === 3 ? 8 : 15;
    days.push({
      date,
      contributionCount: count,
      color: GITHUB_COLORS[level],
    });
  }

  if (days.length === 0) {
    throw new Error("Could not parse contribution days from HTML page.");
  }

  // Chunk days into weeks (7 days each)
  const weeks = [];
  for (let i = 0; i < days.length; i += 7) {
    const chunk = days.slice(i, i + 7);
    weeks.push({ contributionDays: chunk });
  }

  return weeks;
}

async function getWeeks() {
  if (TOKEN) {
    try {
      console.log(`Fetching contributions for ${USERNAME} via GraphQL API...`);
      return await fetchWeeksGraphQL(TOKEN);
    } catch (err) {
      console.warn(`GraphQL fetch failed: ${err.message}. Falling back to public scraper...`);
    }
  }
  console.log(`Fetching public contributions for ${USERNAME}...`);
  return await fetchWeeksScrape();
}

function buildCells(weeks) {
  const recent = weeks.slice(-COLS);
  const padCount = COLS - recent.length;
  const padded = Array.from({ length: Math.max(0, padCount) }, () => ({
    contributionDays: Array.from({ length: ROWS }, () => ({
      contributionCount: 0,
      color: "#161b22",
      date: null,
    })),
  })).concat(recent);

  const cells = [];
  padded.forEach((week, col) => {
    week.contributionDays.forEach((day, row) => {
      cells.push({
        col,
        row,
        x: GRID_X + col * STEP,
        y: GRID_Y + row * STEP,
        color: day.color || "#161b22",
        count: day.contributionCount || 0,
        date: day.date,
      });
    });
  });
  return cells;
}

function pickTargets(cells) {
  const active = cells.filter((c) => c.count > 0);
  // If not enough active days, pick any non-empty cells or top days
  const pool = active.length >= 4 ? active : cells.slice(-28).filter(c => c.color !== "#161b22" || c.count > 0);
  
  return [...(pool.length > 0 ? pool : cells.slice(-12))]
    .sort((a, b) => b.count - a.count)
    .slice(0, MAX_TARGETS)
    .sort((a, b) => a.col - b.col || a.row - b.row);
}

function keyTimeForCol(col, direction) {
  const span = 0.46;
  const t = 0.02 + (col / (COLS - 1)) * span;
  return direction === "forward" ? t : 1 - t;
}

function fmt(n) {
  return Number(n.toFixed(4));
}

function buildGrid(cells, targets) {
  const targetKey = new Set(targets.map((t) => `${t.col}-${t.row}`));
  let svg = "";
  for (const c of cells) {
    const isTarget = targetKey.has(`${c.col}-${c.row}`);
    if (!isTarget) {
      svg += `  <rect x="${c.x.toFixed(2)}" y="${c.y.toFixed(2)}" width="${CELL}" height="${CELL}" rx="2" ry="2" fill="${c.color}"/>\n`;
      continue;
    }
    const tFwd = keyTimeForCol(c.col, "forward");
    const tBack = keyTimeForCol(c.col, "backward");
    const [t1, t2] = [Math.min(tFwd, tBack), Math.max(tFwd, tBack)];
    const dur = 0.006;
    svg += `  <rect x="${c.x.toFixed(2)}" y="${c.y.toFixed(2)}" width="${CELL}" height="${CELL}" rx="2" ry="2" fill="${c.color}">` +
      `<animate attributeName="fill" dur="${LOOP_DUR}s" repeatCount="indefinite" ` +
      `keyTimes="0;${fmt(t1)};${fmt(t1 + dur)};${fmt(t2)};${fmt(t2 + dur)};1" ` +
      `values="${c.color};${c.color};${FLASH_COLOR};${c.color};${FLASH_COLOR};${c.color}"/>` +
      `</rect>\n`;
  }
  return svg;
}

function buildBulletsAndBlasts(targets) {
  let bullets = "";
  let blasts = "";
  const dur = 0.006;

  for (const dir of ["forward", "backward"]) {
    const ordered = dir === "forward" ? targets : [...targets].reverse();
    for (const c of ordered) {
      const t = keyTimeForCol(c.col, dir);
      const rise = Math.max(0, t - dur * 3);
      const arrive = t;
      const fadeEnd = Math.min(1, t + dur);
      const cx = fmt(c.x + CELL / 2);
      const targetY = fmt(c.y + CELL / 2);

      bullets += `  <circle cx="${cx}" cy="${PAD_Y}" r="2.4" fill="${BULLET_COLOR}">` +
        `<animate attributeName="cy" dur="${LOOP_DUR}s" repeatCount="indefinite" ` +
        `keyTimes="0;${fmt(rise)};${fmt(arrive)};1" values="${PAD_Y};${PAD_Y};${targetY};${targetY}"/>` +
        `<animate attributeName="opacity" dur="${LOOP_DUR}s" repeatCount="indefinite" ` +
        `keyTimes="0;${fmt(rise)};${fmt(arrive)};${fmt(fadeEnd)};1" values="0;1;1;0;0"/>` +
        `</circle>\n`;

      blasts += `  <circle cx="${cx}" cy="${targetY}" r="0" fill="none" stroke="${BLAST_COLOR}" stroke-width="1.6" opacity="0">` +
        `<animate attributeName="r" dur="${LOOP_DUR}s" repeatCount="indefinite" ` +
        `keyTimes="0;${fmt(arrive)};${fmt(arrive + dur * 3)};1" values="0;1;9;9"/>` +
        `<animate attributeName="opacity" dur="${LOOP_DUR}s" repeatCount="indefinite" ` +
        `keyTimes="0;${fmt(arrive)};${fmt(arrive + dur * 3)};1" values="0;1;1;0"/>` +
        `</circle>\n`;
    }
  }
  return { bullets, blasts };
}

function buildStars() {
  const pts = [
    [8, 20, 1.2], [8, 60, 1.6], [8, 100, 2.0],
    [505, 25, 1.2], [505, 70, 1.6], [505, 110, 2.0],
    [30, 164, 1.2], [483, 164, 1.6],
  ];
  return pts.map(([x, y, dur]) =>
    `  <circle cx="${x}" cy="${y}" r="1.1" fill="#8b949e"><animate attributeName="opacity" values="0.2;1;0.2" dur="${dur}s" repeatCount="indefinite"/></circle>`
  ).join("\n");
}

function buildJet() {
  return `<g id="jet">
  <g transform="translate(0,0)">
    <polygon points="0,-16 8,6 4,3 -4,3 -8,6" fill="#58a6ff" stroke="#1f6feb" stroke-width="1"/>
    <polygon points="-8,6 -14,12 -4,7" fill="#388bfd"/>
    <polygon points="8,6 14,12 4,7" fill="#388bfd"/>
    <circle cx="0" cy="-6" r="2.2" fill="#c9e6ff"/>
    <polygon points="-3,7 3,7 0,15" fill="#f0883e">
      <animate attributeName="opacity" values="0.5;1;0.6;1" dur="0.18s" repeatCount="indefinite"/>
    </polygon>
  </g>
  <animateTransform attributeName="transform" attributeType="XML" type="translate"
    dur="${LOOP_DUR}s" repeatCount="indefinite"
    keyTimes="0;0.5;1"
    values="${JET_X_START}.00,140.00;${JET_X_END}.00,140.00;${JET_X_START}.00,140.00"/>
</g>`;
}

function buildSvg(weeks) {
  const cells = buildCells(weeks);
  const targets = pickTargets(cells);
  const { bullets, blasts } = buildBulletsAndBlasts(targets);

  return `<svg viewBox="0 0 ${WIDTH} ${HEIGHT}" xmlns="http://www.w3.org/2000/svg">
<rect x="0" y="0" width="${WIDTH}" height="${HEIGHT}" fill="#0d1117"/>
${buildStars()}
<g id="grid">
${buildGrid(cells, targets)}</g>
<g id="bullets">
${bullets}</g>
<g id="blasts">
${blasts}</g>
${buildJet()}
</svg>`;
}

async function main() {
  const weeks = await getWeeks();
  console.log(`Processed ${weeks.length} contribution weeks.`);
  const svg = buildSvg(weeks);
  const outPath = path.resolve(OUTPUT);
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, svg, "utf8");
  console.log(`Successfully generated Jet Heatmap at ${outPath}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
