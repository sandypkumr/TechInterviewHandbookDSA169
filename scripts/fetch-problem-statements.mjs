#!/usr/bin/env node
/**
 * fetch-problem-statements.mjs
 *
 * Fetches problem statements from LeetCode's public GraphQL endpoint and
 * writes them into the MDX content files under site/src/content/problems/.
 *
 * NOTE: LeetCode problem content is copyright LeetCode LLC.
 * This script is intended for personal / educational use only.
 *
 * USAGE
 *   node scripts/fetch-problem-statements.mjs              # all problems
 *   node scripts/fetch-problem-statements.mjs --dry-run   # preview, no writes
 *   node scripts/fetch-problem-statements.mjs --slug two-sum          # one problem
 *   node scripts/fetch-problem-statements.mjs --force     # re-fetch existing
 *
 * Requires Node 18+ (uses built-in fetch). Node 22 is fine.
 */

import { readFile, writeFile, readdir } from 'fs/promises';
import { join, dirname }                from 'path';
import { fileURLToPath }               from 'url';

const ROOT         = dirname(fileURLToPath(import.meta.url));
const PROBLEMS_DIR = join(ROOT, '../site/src/content/problems');
const DELAY_MS     = 1500; // ms between requests — be polite to LeetCode

// ── CLI flags ─────────────────────────────────────────────────────────────
const argv      = process.argv.slice(2);
const DRY_RUN   = argv.includes('--dry-run');
const FORCE     = argv.includes('--force');
const DEBUG     = argv.includes('--debug');
const ONLY_SLUG = (() => { const i = argv.indexOf('--slug'); return i !== -1 ? argv[i + 1] : null; })();

const sleep = ms => new Promise(r => setTimeout(r, ms));

// ═══════════════════════════════════════════════════════════════════════════
// LeetCode GraphQL fetch
// ═══════════════════════════════════════════════════════════════════════════

async function fetchStatement(titleSlug) {
  const res = await fetch('https://leetcode.com/graphql', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'User-Agent':   'Mozilla/5.0 (compatible; educational-dsa-site)',
      'Referer':      `https://leetcode.com/problems/${titleSlug}/`,
    },
    body: JSON.stringify({
      operationName: 'questionContent',
      variables:     { titleSlug },
      query: `query questionContent($titleSlug: String!) {
  question(titleSlug: $titleSlug) { content isPaidOnly }
}`,
    }),
  });

  if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText}`);
  const json = await res.json();
  if (json.errors?.length) throw new Error(json.errors[0].message);
  return json.data?.question ?? null;
}

// ═══════════════════════════════════════════════════════════════════════════
// HTML → MDX conversion
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Decode HTML entities for content that will live INSIDE backtick code spans
 * or fenced code blocks. Inside those contexts <, > are safe literals.
 */
function decodeInCode(s) {
  return s
    .replace(/<sup[^>]*>([\s\S]*?)<\/sup>/gi, '^$1') // 10^4
    .replace(/<sub[^>]*>([\s\S]*?)<\/sub>/gi, '_$1')
    .replace(/<[^>]+>/g, '')                          // strip remaining tags
    .replace(/&lt;/g,   '<')
    .replace(/&gt;/g,   '>')
    .replace(/&amp;/g,  '&')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g,  "'")
    .replace(/&apos;/g, "'")
    .replace(/&nbsp;/g, ' ');
}

/**
 * Decode HTML entities for plain prose.
 * < must be escaped as \< so MDX does not try to parse it as JSX.
 */
function decodeInProse(s) {
  return s
    .replace(/&lt;/g,   '\\<')   // IMPORTANT: escape for MDX prose
    .replace(/&gt;/g,   '>')
    .replace(/&amp;/g,  '&')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g,  "'")
    .replace(/&apos;/g, "'")
    .replace(/&nbsp;/g, ' ')
    .replace(/&le;/g,   '≤')
    .replace(/&ge;/g,   '≥')
    .replace(/&times;/g,'×')
    .replace(/&#(\d+);/g, (_, c) => String.fromCharCode(+c));
}

function htmlToMdx(html) {
  let s = html;

  // ── 1. <pre> blocks → fenced code (examples / I-O blocks) ───────────────
  // Must run first before inline-tag conversion affects the pre contents.
  s = s.replace(/<pre>\s*([\s\S]*?)\s*<\/pre>/gi, (_, inner) => {
    const clean = decodeInCode(inner).trim();
    return `\n\n\`\`\`\n${clean}\n\`\`\`\n`;
  });

  // ── 2. <code> spans (decode inside, keep < literal) ──────────────────────
  s = s.replace(/<code[^>]*>([\s\S]*?)<\/code>/gi,
    (_, inner) => '`' + decodeInCode(inner) + '`');

  // ── 3. Superscript / subscript (prose context, outside code) ────────────
  s = s.replace(/<sup[^>]*>([\s\S]*?)<\/sup>/gi, '^$1^');
  s = s.replace(/<sub[^>]*>([\s\S]*?)<\/sub>/gi, '_$1_');

  // ── 4. Inline emphasis ────────────────────────────────────────────────────
  s = s.replace(/<strong[^>]*>([\s\S]*?)<\/strong>/gi, '**$1**');
  s = s.replace(/<b[^>]*>([\s\S]*?)<\/b>/gi,           '**$1**');
  s = s.replace(/<em[^>]*>([\s\S]*?)<\/em>/gi,         '_$1_');
  s = s.replace(/<i[^>]*>([\s\S]*?)<\/i>/gi,           '_$1_');

  // ── 5. Lists ──────────────────────────────────────────────────────────────
  // Collect only the <li> matches so inter-item whitespace nodes are discarded.
  s = s.replace(/<ul[^>]*>([\s\S]*?)<\/ul>/gi, (_, body) => {
    const items = [];
    const re = /<li[^>]*>([\s\S]*?)<\/li>/gi;
    let m;
    while ((m = re.exec(body)) !== null)
      items.push('- ' + m[1].replace(/<\/?[a-zA-Z][^>]*>/g, '').trim());
    return items.join('\n') + '\n\n';
  });

  s = s.replace(/<ol[^>]*>([\s\S]*?)<\/ol>/gi, (_, body) => {
    const items = [];
    let n = 0;
    const re = /<li[^>]*>([\s\S]*?)<\/li>/gi;
    let m;
    while ((m = re.exec(body)) !== null)
      items.push(`${++n}. ` + m[1].replace(/<\/?[a-zA-Z][^>]*>/g, '').trim());
    return items.join('\n') + '\n\n';
  });

  // ── 6. Paragraphs ─────────────────────────────────────────────────────────
  s = s.replace(/<p[^>]*>([\s\S]*?)<\/p>/gi, '$1\n\n');

  // ── 7. Horizontal rules / dividers ───────────────────────────────────────
  s = s.replace(/<hr\s*\/?>/gi, '\n\n---\n\n');

  // ── 8. Decode entities in the remaining prose ─────────────────────────────
  s = decodeInProse(s);

  // ── 9. Strip any remaining HTML tags ─────────────────────────────────────
  // Use <\/?[a-zA-Z] so the < in <= (inside code spans) is never matched.
  s = s.replace(/<\/?[a-zA-Z][^>]*>/g, '');

  // ── 10. Tidy whitespace ───────────────────────────────────────────────────
  s = s
    .replace(/\n{3,}/g, '\n\n')
    .replace(/ {2,}/g, ' ')
    .trim();

  return s;
}

// ═══════════════════════════════════════════════════════════════════════════
// MDX file patcher
// ═══════════════════════════════════════════════════════════════════════════

function patchFile(original, mdxStatement) {
  let out = original;

  // Update the three frontmatter boolean flags
  out = out
    .replace(/^hasProblemStatement:\s*(true|false)/m, 'hasProblemStatement: true')
    .replace(/^hasExamples:\s*(true|false)/m,         'hasExamples: true')
    .replace(/^hasConstraints:\s*(true|false)/m,      'hasConstraints: true');

  // Locate the ## Problem Statement section and replace it.
  // The section runs until the next ## heading (or end of file).
  const START_MARKER = '\n## Problem Statement';
  const startIdx = out.indexOf(START_MARKER);
  if (startIdx === -1) return out; // unexpected — leave file untouched

  // Find next ## heading after the start
  const nextH2 = out.indexOf('\n## ', startIdx + START_MARKER.length);
  const endIdx  = nextH2 !== -1 ? nextH2 : out.length;

  const newSection = `\n## Problem Statement\n\n${mdxStatement}\n`;
  return out.slice(0, startIdx) + newSection + out.slice(endIdx);
}

// ═══════════════════════════════════════════════════════════════════════════
// Main
// ═══════════════════════════════════════════════════════════════════════════

const stats = { ok: 0, skip: 0, premium: 0, fail: 0 };

const files = (await readdir(PROBLEMS_DIR))
  .filter(f => f.endsWith('.mdx'))
  .sort();

console.log(`Found ${files.length} problem files${DRY_RUN ? ' [DRY RUN]' : ''}\n`);

for (const file of files) {
  const filePath = join(PROBLEMS_DIR, file);
  const src      = await readFile(filePath, 'utf-8');

  // Extract the LeetCode title slug from the leetcodeUrl frontmatter field
  const urlMatch = src.match(
    /leetcodeUrl:\s*["']?https:\/\/leetcode\.com\/problems\/([^/"'\s\n]+)/
  );
  if (!urlMatch) {
    console.warn(`⚠  ${file} — no leetcodeUrl, skipping`);
    stats.skip++;
    continue;
  }
  const titleSlug = urlMatch[1].replace(/\/$/, '');

  // Apply --slug filter
  if (ONLY_SLUG && titleSlug !== ONLY_SLUG) continue;

  // Skip already-fetched unless --force
  if (!FORCE && /^hasProblemStatement:\s*true/m.test(src)) {
    process.stdout.write(`  ✓ ${titleSlug}\n`);
    stats.skip++;
    continue;
  }

  process.stdout.write(`→ ${titleSlug} … `);

  try {
    const question = await fetchStatement(titleSlug);

    if (!question) {
      console.log('not found');
      stats.fail++;
      continue;
    }
    if (question.isPaidOnly) {
      console.log('🔒 premium (skipped)');
      stats.premium++;
      continue;
    }
    if (!question.content) {
      console.log('empty content');
      stats.fail++;
      continue;
    }

    const mdxStatement = htmlToMdx(question.content);
    if (DEBUG) {
      console.log('\n── RAW HTML (first 2000 chars) ──');
      console.log(question.content.slice(0, 2000));
      console.log('\n── CONVERTED MDX ──');
      console.log(mdxStatement);
      console.log('─'.repeat(60));
    }
    const patched      = patchFile(src, mdxStatement);

    if (DRY_RUN) {
      console.log('[dry-run — preview below]');
      // Print the first 800 chars of the new Problem Statement section
      const previewStart = patched.indexOf('\n## Problem Statement');
      const previewEnd   = patched.indexOf('\n## ', previewStart + 22);
      console.log(patched.slice(previewStart, previewEnd !== -1 ? previewEnd : previewStart + 800));
      console.log('─'.repeat(60));
    } else {
      await writeFile(filePath, patched, 'utf-8');
      console.log('✅');
      stats.ok++;
    }
  } catch (err) {
    console.log(`✗  ${err.message}`);
    stats.fail++;
  }

  await sleep(DELAY_MS);
}

console.log(`
╔════════════════════════════════╗
  Updated  : ${String(stats.ok).padStart(3)}
  Skipped  : ${String(stats.skip).padStart(3)}
  Premium  : ${String(stats.premium).padStart(3)}
  Failed   : ${String(stats.fail).padStart(3)}
╚════════════════════════════════╝`);
