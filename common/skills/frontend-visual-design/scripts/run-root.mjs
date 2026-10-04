#!/usr/bin/env node

import { lstatSync, mkdirSync, realpathSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { isAbsolute, relative, resolve } from "node:path";

const SKILL_KEY = "frontend-visual-design";
const PORTABLE_SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*$/u;
const WINDOWS_RESERVED = /^(?:con|prn|aux|nul|com[1-9]|lpt[1-9])$/iu;
const RUN_ROOT = new RegExp(`^\\.local-state/visual-qa/${SKILL_KEY}/\\d{8}T\\d{6}Z-([a-z0-9]+(?:-[a-z0-9]+)*)$`, "u");

export function validateSlug(value) {
  if (typeof value !== "string" || value.length > 48 || !PORTABLE_SLUG.test(value) || WINDOWS_RESERVED.test(value)) {
    throw new Error("slug must be 1-48 lowercase ASCII letters or digits joined by single hyphens and must not be a Windows reserved name");
  }
  return value;
}

export function createRunRoot(slug, cwd = process.cwd(), now = new Date()) {
  const safeSlug = validateSlug(slug);
  const stamp = now.toISOString().replaceAll("-", "").replaceAll(":", "").replace(/\.\d{3}Z$/u, "Z");
  const root = `.local-state/visual-qa/${SKILL_KEY}/${stamp}-${safeSlug}`;
  const base = realpathSync(cwd);
  ensureDirectoryTree(base, root.split("/"));
  return root;
}

export function verifyRunFiles(root, files, cwd = process.cwd()) {
  const normalizedRoot = root.replaceAll("\\", "/");
  const match = normalizedRoot.match(RUN_ROOT);
  if (!match) {
    throw new Error(`run root must match .local-state/visual-qa/${SKILL_KEY}/YYYYMMDDTHHMMSSZ-<portable-slug>`);
  }
  validateSlug(match[1]);
  if (!Array.isArray(files) || files.length === 0) {
    throw new Error("at least one run file is required");
  }

  const base = realpathSync(cwd);
  const absoluteRoot = requireDirectoryTree(base, normalizedRoot.split("/"));
  for (const file of files) {
    if (typeof file !== "string" || file.length === 0 || isAbsolute(file)) {
      throw new Error("run filenames must be non-empty relative paths");
    }
    const candidate = resolve(absoluteRoot, file);
    const inside = relative(absoluteRoot, candidate);
    if (inside === "" || inside === ".." || inside.startsWith("../") || inside.startsWith("..\\") || isAbsolute(inside)) {
      throw new Error(`run file escapes its root: ${file}`);
    }
    requireNoSymlinkPath(absoluteRoot, inside);
    const metadata = lstatSync(candidate);
    if (!metadata.isFile() || metadata.size === 0) {
      throw new Error(`run file must be a non-empty regular file: ${file}`);
    }
  }
  return normalizedRoot;
}

function ensureDirectoryTree(base, segments) {
  let current = base;
  for (const [index, segment] of segments.entries()) {
    current = resolve(current, segment);
    try {
      const metadata = lstatSync(current);
      if (metadata.isSymbolicLink()) throw new Error(`run directory must not be a symlink: ${segment}`);
      if (!metadata.isDirectory()) throw new Error(`run path component must be a directory: ${segment}`);
      if (index === segments.length - 1) throw new Error(`run root already exists: ${current}`);
    } catch (error) {
      if (error?.code !== "ENOENT") throw error;
      try {
        mkdirSync(current);
      } catch (creationError) {
        if (creationError?.code !== "EEXIST") throw creationError;
        const metadata = lstatSync(current);
        if (metadata.isSymbolicLink()) throw new Error(`run directory must not be a symlink: ${segment}`);
        if (!metadata.isDirectory()) throw new Error(`run path component must be a directory: ${segment}`);
      }
    }
  }
  return current;
}

function requireDirectoryTree(base, segments) {
  let current = base;
  for (const segment of segments) {
    current = resolve(current, segment);
    const metadata = lstatSync(current);
    if (metadata.isSymbolicLink()) throw new Error(`run directory must not be a symlink: ${segment}`);
    if (!metadata.isDirectory()) throw new Error(`run path component must be a directory: ${segment}`);
  }
  return current;
}

function requireNoSymlinkPath(base, relativePath) {
  let current = base;
  for (const segment of relativePath.split(/[\\/]/u)) {
    current = resolve(current, segment);
    if (lstatSync(current).isSymbolicLink()) throw new Error(`run file path must not contain symlinks: ${relativePath}`);
  }
}

function main(argv) {
  const [command, value, ...files] = argv;
  if (command === "create" && value && files.length === 0) {
    process.stdout.write(`${createRunRoot(value)}\n`);
    return;
  }
  if (command === "verify" && value) {
    process.stdout.write(`${verifyRunFiles(value, files)}\n`);
    return;
  }
  throw new Error("usage: run-root.mjs create <slug> | verify <run-root> <file...>");
}

function isCliEntry(argvPath) {
  if (!argvPath) return false;
  try {
    return realpathSync(argvPath) === realpathSync(fileURLToPath(import.meta.url));
  } catch {
    return false;
  }
}

if (isCliEntry(process.argv[1])) {
  try {
    main(process.argv.slice(2));
  } catch (error) {
    process.stderr.write(`run-root: ${error instanceof Error ? error.message : String(error)}\n`);
    process.exitCode = 2;
  }
}
