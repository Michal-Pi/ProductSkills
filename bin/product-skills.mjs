#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { fileURLToPath, pathToFileURL } from "node:url";

const CLI_PATH = fileURLToPath(import.meta.url);
const PACKAGE_ROOT = path.resolve(path.dirname(CLI_PATH), "..");
const CANONICAL_REPO = "https://github.com/Michal-Pi/ProductSkills.git";
const MARKER_START = "<!-- PRODUCT_SKILLS_START -->";
const MARKER_END = "<!-- PRODUCT_SKILLS_END -->";
const SUPPORTED_RUNTIMES = new Set(["claude", "codex", "cursor", "gemini", "all"]);
const SUPPORTED_SCOPES = new Set(["user", "repo"]);
const SUPPORTED_ADAPTERS = new Set(["skills", "agents", "extension", "auto"]);
const REQUIRED_NODE_MAJOR = 20;

class InstallerError extends Error {
  constructor(message, code = 1) {
    super(message);
    this.name = "InstallerError";
    this.code = code;
  }
}

class Plan {
  constructor({ dryRun = false } = {}) {
    this.dryRun = dryRun;
    this.actions = [];
  }

  record(action, target, detail = "") {
    this.actions.push({ action, target, detail });
  }

  writeFile(target, content) {
    this.record("write", target);
    if (!this.dryRun) {
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.writeFileSync(target, content, "utf8");
    }
  }

  appendFile(target, content) {
    this.record("append", target);
    if (!this.dryRun) {
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.appendFileSync(target, content, "utf8");
    }
  }

  mkdir(target) {
    this.record("mkdir", target);
    if (!this.dryRun) {
      fs.mkdirSync(target, { recursive: true });
    }
  }

  backup(source, target) {
    this.record("backup", `${source} -> ${target}`);
    if (!this.dryRun) {
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.copyFileSync(source, target);
      pruneBackups(source, 5);
    }
  }

  remove(target) {
    this.record("remove", target);
    if (!this.dryRun) {
      fs.rmSync(target, { recursive: true, force: true });
    }
  }

  rmdirIfEmpty(target) {
    this.record("rmdir-if-empty", target);
    if (!this.dryRun && fs.existsSync(target) && fs.readdirSync(target).length === 0) {
      fs.rmdirSync(target);
    }
  }
}

export function parseArgs(argv) {
  const options = {
    runtime: undefined,
    scope: undefined,
    adapter: "auto",
    repo: undefined,
    packageStore: undefined,
    source: undefined,
    ref: undefined,
    force: false,
    replace: false,
    dryRun: false,
    json: false,
    trackPackageStore: false,
    removePackageStore: false,
    cleanBackups: false,
    trustSource: false,
  };
  const positionals = [];

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) {
      positionals.push(token);
      continue;
    }

    const [rawName, inlineValue] = token.slice(2).split("=", 2);
    const readValue = () => {
      if (inlineValue !== undefined) {
        return inlineValue;
      }
      index += 1;
      if (index >= argv.length || argv[index].startsWith("--")) {
        throw new InstallerError(`Missing value for --${rawName}`);
      }
      return argv[index];
    };

    switch (rawName) {
      case "runtime":
        options.runtime = readValue();
        break;
      case "scope":
        options.scope = readValue();
        break;
      case "adapter":
        options.adapter = readValue();
        break;
      case "repo":
        options.repo = readValue();
        break;
      case "package-store":
        options.packageStore = readValue();
        break;
      case "source":
        options.source = readValue();
        break;
      case "ref":
        options.ref = readValue();
        break;
      case "force":
        options.force = true;
        break;
      case "replace":
        options.replace = true;
        break;
      case "dry-run":
        options.dryRun = true;
        break;
      case "json":
        options.json = true;
        break;
      case "track-package-store":
        options.trackPackageStore = true;
        break;
      case "remove-package-store":
        options.removePackageStore = true;
        break;
      case "clean-backups":
        options.cleanBackups = true;
        break;
      case "trust-source":
        options.trustSource = true;
        break;
      case "global":
        options.scope = "user";
        break;
      case "project":
        options.scope = "repo";
        break;
      case "help":
        positionals.push("help");
        break;
      default:
        throw new InstallerError(`Unknown option --${rawName}`);
    }
  }

  const command = positionals[0] ?? "help";
  if (positionals.length > 1) {
    throw new InstallerError(`Unexpected argument: ${positionals.slice(1).join(" ")}`);
  }
  return { command, options };
}

export function renderTemplate(template, variables) {
  return template.replaceAll("{{PACKAGE_STORE}}", variables.packageStore)
    .replaceAll("{{INSTALL_SCOPE}}", variables.scope)
    .replaceAll("{{RUNTIME}}", variables.runtime)
    .replaceAll("{{VERSION}}", variables.version);
}

export function upsertMarkerBlock(existing, block, filePath) {
  const start = existing.indexOf(MARKER_START);
  const end = existing.indexOf(MARKER_END);
  const hasStart = start !== -1;
  const hasEnd = end !== -1;

  if (hasStart !== hasEnd || (hasStart && start > end)) {
    throw new InstallerError(
      `Malformed ProductSkills marker block in ${filePath}. Restore from backup or remove the partial ${MARKER_START}/${MARKER_END} block, then rerun install.`
    );
  }

  const normalizedBlock = block.trimEnd();
  if (!hasStart) {
    const separator = existing.trim().length === 0 ? "" : "\n\n";
    return `${existing.trimEnd()}${separator}${normalizedBlock}\n`;
  }

  const before = existing.slice(0, start).trimEnd();
  const after = existing.slice(end + MARKER_END.length).trimStart();
  return `${before}${before ? "\n\n" : ""}${normalizedBlock}${after ? `\n\n${after}` : "\n"}`;
}

function ensureSupportedNode() {
  const major = Number.parseInt(process.versions.node.split(".")[0], 10);
  if (Number.isNaN(major) || major < REQUIRED_NODE_MAJOR) {
    throw new InstallerError(
      `Unsupported Node.js version ${process.versions.node}. Install Node.js ${REQUIRED_NODE_MAJOR}.0.0 or newer, then rerun product-skills.`
    );
  }
}

function assertOptionValues(options) {
  if (options.runtime && !SUPPORTED_RUNTIMES.has(options.runtime)) {
    throw new InstallerError(`Invalid runtime '${options.runtime}'. Use claude, codex, cursor, gemini, or all.`);
  }
  if (options.scope && !SUPPORTED_SCOPES.has(options.scope)) {
    throw new InstallerError(`Invalid scope '${options.scope}'. Use user or repo.`);
  }
  if (options.adapter && !SUPPORTED_ADAPTERS.has(options.adapter)) {
    throw new InstallerError(`Invalid adapter '${options.adapter}'. Use skills, agents, extension, or auto.`);
  }
}

function expandHome(inputPath) {
  if (inputPath === "~") {
    return os.homedir();
  }
  if (inputPath.startsWith("~/")) {
    return path.join(os.homedir(), inputPath.slice(2));
  }
  return inputPath;
}

function resolvePath(inputPath, cwd = process.cwd()) {
  return path.resolve(cwd, expandHome(inputPath));
}

function findUp(start, predicate) {
  let current = path.resolve(start);
  while (true) {
    if (predicate(current)) {
      return current;
    }
    const parent = path.dirname(current);
    if (parent === current) {
      return null;
    }
    current = parent;
  }
}

function findGitRoot(start) {
  return findUp(start, (candidate) => fs.existsSync(path.join(candidate, ".git")));
}

function looksLikeProductSkillsRoot(candidate) {
  return fs.existsSync(path.join(candidate, "package.yaml"))
    && fs.existsSync(path.join(candidate, "registry.json"))
    && fs.existsSync(path.join(candidate, "skills", "workflow-product-operating-system", "SKILL.md"));
}

function findProductSkillsRoot(start) {
  return findUp(start, looksLikeProductSkillsRoot);
}

function parsePackageYamlVersion(packageYaml) {
  if (!fs.existsSync(packageYaml)) {
    return null;
  }
  const match = fs.readFileSync(packageYaml, "utf8").match(/^version:\s*([^\s#]+)/m);
  return match ? match[1].trim().replace(/^["']|["']$/g, "") : null;
}

function readJsonFile(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function readVersionSources(root) {
  const sources = {};
  const versionPath = path.join(root, "VERSION");
  if (fs.existsSync(versionPath)) {
    sources.VERSION = fs.readFileSync(versionPath, "utf8").trim();
  }
  const packageJsonPath = path.join(root, "package.json");
  if (fs.existsSync(packageJsonPath)) {
    sources["package.json"] = readJsonFile(packageJsonPath).version ?? null;
  }
  const codexPluginPath = path.join(root, ".codex-plugin", "plugin.json");
  if (fs.existsSync(codexPluginPath)) {
    sources[".codex-plugin/plugin.json"] = readJsonFile(codexPluginPath).version ?? null;
  }
  sources["package.yaml"] = parsePackageYamlVersion(path.join(root, "package.yaml"));
  const registryPath = path.join(root, "registry.json");
  if (fs.existsSync(registryPath)) {
    sources["registry.json"] = readJsonFile(registryPath).version ?? null;
  }
  return sources;
}

export function checkVersionConsistency(root = PACKAGE_ROOT) {
  const sources = readVersionSources(root);
  const present = Object.entries(sources).filter(([, value]) => typeof value === "string" && value.length > 0);
  const missing = Object.entries(sources).filter(([, value]) => !value).map(([name]) => name);
  const expected = sources.VERSION ?? present[0]?.[1] ?? null;
  const mismatches = expected
    ? present.filter(([, value]) => value !== expected).map(([name, value]) => ({ name, version: value, expected }))
    : [];
  return {
    ok: missing.length === 0 && mismatches.length === 0 && present.length >= 4,
    version: missing.length === 0 && mismatches.length === 0 ? expected : null,
    sources,
    mismatches,
    missing,
  };
}

function readVersion(root) {
  const versionPath = path.join(root, "VERSION");
  if (fs.existsSync(versionPath)) {
    return fs.readFileSync(versionPath, "utf8").trim();
  }
  return parsePackageYamlVersion(path.join(root, "package.yaml")) ?? "unknown";
}

function packageStoreDisplay(packageStore, scope, repoRoot) {
  if (scope === "repo" && repoRoot) {
    const relative = path.relative(repoRoot, packageStore);
    if (relative && !relative.startsWith("..") && !path.isAbsolute(relative)) {
      return relative.split(path.sep).join("/");
    }
  }
  return packageStore;
}

function resolveContext(options, cwd = process.cwd()) {
  assertOptionValues(options);
  const repoRoot = options.repo ? resolvePath(options.repo, cwd) : findGitRoot(cwd);
  const scope = options.scope ?? (repoRoot ? "repo" : "user");
  if (scope === "repo" && !repoRoot) {
    throw new InstallerError("Repo scope requested, but no git repository was found. Run inside a repo or pass --repo <path>.");
  }

  const packageStore = options.packageStore
    ? resolvePath(options.packageStore, cwd)
    : scope === "repo"
      ? path.join(repoRoot, ".product-skills")
      : path.join(os.homedir(), ".product-skills");

  return {
    repoRoot,
    scope,
    packageStore,
    runtime: options.runtime ?? "all",
    adapter: options.adapter ?? "auto",
  };
}

function runtimeList(runtime) {
  return runtime === "all" ? ["claude", "codex", "cursor", "gemini"] : [runtime];
}

function adapterTemplatePath(runtime, adapterKind) {
  if (runtime === "claude") {
    return path.join(PACKAGE_ROOT, "adapters", "claude", "SKILL.md");
  }
  if (runtime === "codex" && adapterKind === "agents") {
    return path.join(PACKAGE_ROOT, "adapters", "codex", "AGENTS.md");
  }
  if (runtime === "codex") {
    return path.join(PACKAGE_ROOT, "adapters", "codex", "SKILL.md");
  }
  if (runtime === "cursor") {
    return path.join(PACKAGE_ROOT, "adapters", "cursor", "product-operating-system.mdc");
  }
  if (runtime === "gemini") {
    if (adapterKind === "extension-manifest") {
      return path.join(PACKAGE_ROOT, "adapters", "gemini", "extension", "gemini-extension.json");
    }
    if (adapterKind === "extension-context") {
      return path.join(PACKAGE_ROOT, "adapters", "gemini", "extension", "GEMINI.md");
    }
    return path.join(PACKAGE_ROOT, "adapters", "gemini", "GEMINI.md");
  }
  throw new InstallerError(`Unsupported runtime '${runtime}'`);
}

function detectCursorUserRulesDir(home = os.homedir()) {
  const candidates = [];
  if (process.env.PRODUCT_SKILLS_CURSOR_USER_RULES_DIR) {
    candidates.push({
      path: resolvePath(process.env.PRODUCT_SKILLS_CURSOR_USER_RULES_DIR),
      source: "PRODUCT_SKILLS_CURSOR_USER_RULES_DIR",
    });
  }
  candidates.push({
    path: path.join(home, ".cursor", "rules"),
    source: "existing ~/.cursor/rules",
  });

  for (const candidate of candidates) {
    try {
      if (fs.statSync(candidate.path).isDirectory()) {
        return { supported: true, path: candidate.path, source: candidate.source };
      }
    } catch {
      // Keep probing; absence is the expected unsupported case.
    }
  }

  return {
    supported: false,
    reason: "Cursor user scope requires an existing supported global rules directory. Use --scope repo, or set PRODUCT_SKILLS_CURSOR_USER_RULES_DIR to a directory confirmed for your Cursor installation.",
  };
}

function resolveCodexAdapterMode(scope, adapter) {
  if (adapter === "agents") {
    return "agents";
  }
  if (adapter === "skills") {
    return "skills";
  }
  return scope === "repo" ? "agents" : "skills";
}

function adapterTargets(runtime, context) {
  const { scope, repoRoot, adapter } = context;
  if (runtime === "claude") {
    const base = scope === "repo" ? repoRoot : os.homedir();
    return [{
      runtime,
      kind: "dedicated",
      templateKind: "skills",
      path: path.join(base, ".claude", "skills", "product-operating-system", "SKILL.md"),
    }];
  }
  if (runtime === "codex") {
    const mode = resolveCodexAdapterMode(scope, adapter);
    if (mode === "agents") {
      return [{
        runtime,
        kind: "shared",
        templateKind: "agents",
        path: scope === "repo" ? path.join(repoRoot, "AGENTS.md") : path.join(os.homedir(), ".codex", "AGENTS.md"),
      }];
    }
    const base = scope === "repo" ? repoRoot : os.homedir();
    return [{
      runtime,
      kind: "dedicated",
      templateKind: "skills",
      path: path.join(base, ".codex", "skills", "product-operating-system", "SKILL.md"),
    }];
  }
  if (runtime === "cursor") {
    if (scope === "user") {
      const detection = detectCursorUserRulesDir();
      if (!detection.supported) {
        throw new InstallerError(detection.reason);
      }
      return [{
        runtime,
        kind: "dedicated",
        templateKind: "rules",
        path: path.join(detection.path, "product-operating-system.mdc"),
        compatibility: detection.source,
      }];
    }
    return [{
      runtime,
      kind: "dedicated",
      templateKind: "rules",
      path: path.join(repoRoot, ".cursor", "rules", "product-operating-system.mdc"),
    }];
  }
  if (runtime === "gemini") {
    if (adapter === "extension") {
      if (scope !== "user") {
        throw new InstallerError("Gemini extension adapter is supported only for user scope because current Gemini CLI extension discovery uses ~/.gemini/extensions. Use --adapter auto for repo-scope GEMINI.md.");
      }
      const extensionRoot = path.join(os.homedir(), ".gemini", "extensions", "product-skills");
      return [
        {
          runtime,
          kind: "dedicated",
          templateKind: "extension-manifest",
          path: path.join(extensionRoot, "gemini-extension.json"),
          compatibility: "Gemini CLI extensions v0.4.0",
        },
        {
          runtime,
          kind: "dedicated",
          templateKind: "extension-context",
          path: path.join(extensionRoot, "GEMINI.md"),
          compatibility: "Gemini CLI extensions v0.4.0",
        },
      ];
    }
    return [{
      runtime,
      kind: "shared",
      templateKind: "context",
      path: scope === "repo" ? path.join(repoRoot, "GEMINI.md") : path.join(os.homedir(), ".gemini", "GEMINI.md"),
    }];
  }
  throw new InstallerError(`Unsupported runtime '${runtime}'`);
}

function unsupportedAdapter(runtime, error) {
  return {
    runtime,
    adapter: "unsupported",
    path: "",
    supported: false,
    skipped: true,
    reason: error.message,
  };
}

function renderAdapter(target, context) {
  const template = fs.readFileSync(adapterTemplatePath(target.runtime, target.templateKind), "utf8");
  return renderTemplate(template, {
    packageStore: packageStoreDisplay(context.packageStore, context.scope, context.repoRoot),
    scope: context.scope,
    runtime: target.runtime,
    version: readVersion(context.packageStore),
  });
}

function isGeneratedDedicated(target, content) {
  if (target.path.endsWith("SKILL.md")) {
    return /^---[\s\S]*?^name:\s*product-operating-system\s*$/m.test(content);
  }
  if (target.path.endsWith(".mdc")) {
    return /^---[\s\S]*?^description:\s*.*Product Operating System workflow.*$/m.test(content);
  }
  if (target.path.endsWith("gemini-extension.json")) {
    try {
      const parsed = JSON.parse(content);
      return parsed.name === "product-skills" && parsed.contextFileName === "GEMINI.md";
    } catch {
      return false;
    }
  }
  return content.includes("Generated by ProductSkills");
}

function timestamp() {
  const date = new Date();
  const pad = (value) => String(value).padStart(2, "0");
  return `${date.getUTCFullYear()}${pad(date.getUTCMonth() + 1)}${pad(date.getUTCDate())}T${pad(date.getUTCHours())}${pad(date.getUTCMinutes())}${pad(date.getUTCSeconds())}${String(date.getUTCMilliseconds()).padStart(3, "0")}Z`;
}

function backupPath(filePath) {
  return `${filePath}.bak.${timestamp()}`;
}

function pruneBackups(filePath, keep) {
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    return;
  }
  const base = path.basename(filePath);
  const backups = fs.readdirSync(dir)
    .filter((entry) => entry.startsWith(`${base}.bak.`))
    .sort()
    .reverse();
  for (const oldBackup of backups.slice(keep)) {
    fs.rmSync(path.join(dir, oldBackup), { force: true });
  }
}

function writeDedicatedAdapter(plan, target, rendered, options) {
  if (!fs.existsSync(target.path)) {
    plan.writeFile(target.path, rendered);
    return;
  }

  const existing = fs.readFileSync(target.path, "utf8");
  if (isGeneratedDedicated(target, existing)) {
    plan.writeFile(target.path, rendered);
    return;
  }

  if (!options.force) {
    throw new InstallerError(
      `Adapter exists and is not ProductSkills-generated: ${target.path}. Rerun with --force to back it up and replace it.`
    );
  }

  plan.backup(target.path, backupPath(target.path));
  plan.writeFile(target.path, rendered);
}

function writeSharedAdapter(plan, target, rendered, options) {
  if (fs.existsSync(target.path)) {
    const existing = fs.readFileSync(target.path, "utf8");
    if (options.force && options.replace) {
      plan.backup(target.path, backupPath(target.path));
      plan.writeFile(target.path, rendered.trimEnd() + "\n");
      return;
    }
    let next;
    try {
      next = upsertMarkerBlock(existing, rendered, target.path);
    } catch (error) {
      plan.backup(target.path, backupPath(target.path));
      throw error;
    }
    plan.writeFile(target.path, next);
    return;
  }
  plan.writeFile(target.path, rendered.trimEnd() + "\n");
}

function removeMarkerBlock(existing, filePath) {
  const start = existing.indexOf(MARKER_START);
  const end = existing.indexOf(MARKER_END);
  const hasStart = start !== -1;
  const hasEnd = end !== -1;

  if (hasStart !== hasEnd || (hasStart && start > end)) {
    throw new InstallerError(
      `Malformed ProductSkills marker block in ${filePath}. Restore from backup or remove the partial ${MARKER_START}/${MARKER_END} block, then rerun uninstall.`
    );
  }
  if (!hasStart) {
    return existing;
  }

  const before = existing.slice(0, start).trimEnd();
  const after = existing.slice(end + MARKER_END.length).trimStart();
  if (before && after) {
    return `${before}\n\n${after}`;
  }
  if (before) {
    return `${before}\n`;
  }
  if (after) {
    return after.endsWith("\n") ? after : `${after}\n`;
  }
  return "";
}

function writeAdapters(plan, context, options) {
  const installed = [];
  for (const runtime of runtimeList(context.runtime)) {
    let targets;
    try {
      targets = adapterTargets(runtime, context);
    } catch (error) {
      if (context.runtime === "all") {
        installed.push(unsupportedAdapter(runtime, error));
        continue;
      }
      throw error;
    }
    for (const target of targets) {
      const rendered = renderAdapter(target, context);
      if (target.kind === "dedicated") {
        writeDedicatedAdapter(plan, target, rendered, options);
      } else {
        writeSharedAdapter(plan, target, rendered, options);
      }
      installed.push({
        runtime,
        adapter: target.templateKind,
        path: target.path,
        supported: true,
        skipped: false,
        compatibility: target.compatibility ?? null,
      });
    }
  }
  return installed;
}

function isUrl(source) {
  return /^[a-z]+:\/\//i.test(source) || source.startsWith("git@");
}

function run(command, args, { cwd = process.cwd(), stdio = "pipe", env = process.env } = {}) {
  const result = spawnSync(command, args, { cwd, stdio, env, encoding: "utf8" });
  if (result.error) {
    throw new InstallerError(`Failed to run ${command}: ${result.error.message}`);
  }
  return result;
}

function requireCommand(command, label) {
  let result;
  try {
    result = run(command, ["--version"]);
  } catch (error) {
    if (error instanceof InstallerError && error.message.includes("ENOENT")) {
      throw new InstallerError(`Missing ${label}. Install ${label}, then rerun product-skills.`);
    }
    throw error;
  }
  if (result.status !== 0) {
    throw new InstallerError(`Missing ${label}. Install ${label}, then rerun product-skills.`);
  }
}

function cloneSource(source, ref, tempRoot) {
  requireCommand("git", "git");
  const cloneTarget = path.join(tempRoot, "source");
  const args = ref
    ? ["clone", "--depth", "1", "--branch", ref, source, cloneTarget]
    : ["clone", "--depth", "1", source, cloneTarget];
  let result = run("git", args);
  if (result.status !== 0 && ref) {
    fs.rmSync(cloneTarget, { recursive: true, force: true });
    result = run("git", ["clone", "--no-checkout", "--depth", "1", source, cloneTarget]);
    if (result.status === 0) {
      const fetch = run("git", ["-C", cloneTarget, "fetch", "--depth", "1", "origin", ref]);
      const checkout = fetch.status === 0
        ? run("git", ["-C", cloneTarget, "checkout", "--detach", "FETCH_HEAD"])
        : fetch;
      result = checkout;
    }
  }
  if (result.status !== 0) {
    throw new InstallerError(
      `Git clone failed for ${source}. Check the source URL/path and ref, then rerun.\n${result.stderr || result.stdout}`
    );
  }
  return cloneTarget;
}

function shouldCopyPackagePath(sourceRoot, currentPath) {
  const rel = path.relative(sourceRoot, currentPath);
  if (!rel) {
    return true;
  }
  const normalized = rel.split(path.sep).join("/");
  const parts = normalized.split("/");
  if (parts.includes(".git") || parts.includes(".product-skills") || parts.includes("node_modules") || parts.includes("__pycache__")) {
    return false;
  }
  const base = path.basename(normalized);
  if (base === ".DS_Store" || base === ".env" || base.startsWith(".env.")) {
    return false;
  }
  if (normalized === "evals/results" || normalized.startsWith("evals/results/")) {
    return false;
  }
  const constructionDocs = new Set([
    "docs/PACKAGE_INSTALLER_SDD.md",
    "docs/PACKAGE_INSTALLER_AGENT_PROMPT.md",
    "docs/PACKAGE_INSTALLER_PHASE_3_4_AGENT_PROMPT.md",
    "docs/END_TO_END_IMPLEMENTATION_PLAN.md",
    "docs/IMPLEMENTATION_PLAN.md",
    "docs/NEXT_PHASE_AGENT_PROMPT.md",
    "docs/OPINIONATED_E2E_WORKFLOW_EXPANSION_PLAN.md",
    "docs/OPINIONATED_E2E_WORKFLOW_IMPLEMENTATION_DESIGN.md",
    "task_plan.md",
    "progress.md",
    "findings.md",
    "product-management-skills-package-design.md",
    "product-management-skills-package-final.md",
  ]);
  if (constructionDocs.has(normalized) || normalized.startsWith("docs/beta/") || normalized.startsWith("docs/reviews/")) {
    return false;
  }
  return true;
}

function listChecksumFiles(root) {
  const files = [];
  const stack = [root];
  while (stack.length > 0) {
    const current = stack.pop();
    for (const entry of fs.readdirSync(current, { withFileTypes: true })) {
      const entryPath = path.join(current, entry.name);
      if (!shouldCopyPackagePath(root, entryPath)) {
        continue;
      }
      if (entry.isDirectory()) {
        stack.push(entryPath);
      } else if (entry.isFile()) {
        files.push(entryPath);
      }
    }
  }
  return files.sort((left, right) => path.relative(root, left).localeCompare(path.relative(root, right)));
}

export function computeSnapshotChecksum(root = PACKAGE_ROOT) {
  const hash = crypto.createHash("sha256");
  const files = listChecksumFiles(root);
  for (const filePath of files) {
    const relative = path.relative(root, filePath).split(path.sep).join("/");
    const fileHash = crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex");
    hash.update(relative);
    hash.update("\0");
    hash.update(fileHash);
    hash.update("\n");
  }
  return {
    algorithm: "sha256",
    checksum: hash.digest("hex"),
    fileCount: files.length,
    files: files.map((filePath) => path.relative(root, filePath).split(path.sep).join("/")),
  };
}

function copyFiltered(sourceRoot, destinationRoot) {
  fs.cpSync(sourceRoot, destinationRoot, {
    recursive: true,
    dereference: false,
    filter: (sourcePath) => shouldCopyPackagePath(sourceRoot, sourcePath),
  });
}

function resolveInstallSource(options, cwd) {
  if (options.source) {
    return options.source;
  }
  const currentPackageRoot = findProductSkillsRoot(cwd);
  if (currentPackageRoot) {
    return currentPackageRoot;
  }
  if (looksLikeProductSkillsRoot(PACKAGE_ROOT)) {
    return PACKAGE_ROOT;
  }
  return CANONICAL_REPO;
}

function realpathIfExists(inputPath) {
  try {
    return fs.realpathSync(inputPath);
  } catch {
    return path.resolve(inputPath);
  }
}

function normalizedSource(source) {
  return String(source).replace(/\/$/, "").replace(/\.git$/, "");
}

function isTrustedInstallSource(source, sourceRoot, cwd) {
  if (isUrl(String(source))) {
    return normalizedSource(source) === normalizedSource(CANONICAL_REPO);
  }
  const trustedRoots = [PACKAGE_ROOT, findProductSkillsRoot(cwd)].filter(Boolean).map(realpathIfExists);
  return trustedRoots.includes(realpathIfExists(sourceRoot));
}

function stagePackageSource(source, ref, plan, options) {
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), "product-skills-install-"));
  plan.record("stage", tempRoot, "temporary package staging directory");
  try {
    const sourceRoot = isUrl(source)
      ? cloneSource(source, ref, tempRoot)
      : ref
        ? cloneSource(resolvePath(source), ref, tempRoot)
        : resolvePath(source);
    if (!looksLikeProductSkillsRoot(sourceRoot)) {
      throw new InstallerError(`Install source is not a ProductSkills package root: ${sourceRoot}`);
    }
    const staged = path.join(tempRoot, "staged");
    copyFiltered(sourceRoot, staged);
    return { tempRoot, staged, sourceRoot, trusted: isTrustedInstallSource(source, sourceRoot, process.cwd()) };
  } catch (error) {
    fs.rmSync(tempRoot, { recursive: true, force: true });
    throw error;
  }
}

function installPackageStore(plan, context, options) {
  const source = resolveInstallSource(options, process.cwd());
  if (plan.dryRun) {
    plan.record("resolve-source", String(source), options.ref ? `ref ${options.ref}` : "");
    plan.record("copy-package", context.packageStore, "dry run does not copy package files");
    return { source, sourceRoot: typeof source === "string" ? source : String(source) };
  }

  const stagedSource = stagePackageSource(source, options.ref, plan, options);
  try {
    if (!stagedSource.trusted && !options.allowUntrustedSource) {
      throw new InstallerError(
        `Refusing to execute validation scripts from untrusted source: ${source}. Use the canonical repository, run from the current ProductSkills checkout, or rerun with --trust-source if you trust this source.`
      );
    }
    plan.mkdir(path.dirname(context.packageStore));
    const nextStore = `${context.packageStore}.tmp.${process.pid}.${Date.now()}`;
    let previousStore = null;
    plan.record("copy-package", nextStore, `staged from ${stagedSource.sourceRoot}`);
    try {
      copyFiltered(stagedSource.staged, nextStore);
      if (options.preservePreviousStore && fs.existsSync(context.packageStore)) {
        previousStore = `${context.packageStore}.previous.${process.pid}.${Date.now()}`;
        plan.record("backup-store", `${context.packageStore} -> ${previousStore}`);
        fs.renameSync(context.packageStore, previousStore);
      } else {
        plan.remove(context.packageStore);
      }
      plan.record("move", `${nextStore} -> ${context.packageStore}`);
      fs.renameSync(nextStore, context.packageStore);
    } catch (error) {
      fs.rmSync(nextStore, { recursive: true, force: true });
      if (previousStore && !fs.existsSync(context.packageStore) && fs.existsSync(previousStore)) {
        fs.renameSync(previousStore, context.packageStore);
      }
      throw error;
    }
    writeInstallMetadata(context.packageStore, {
      source: isUrl(String(source)) ? String(source) : realpathIfExists(stagedSource.sourceRoot),
      sourceRoot: stagedSource.sourceRoot,
      trustedSource: stagedSource.trusted,
      ref: options.ref ?? null,
      adapter: options.adapter ?? null,
      installedAt: new Date().toISOString(),
    });
    return { source, sourceRoot: stagedSource.sourceRoot, previousStore };
  } finally {
    fs.rmSync(stagedSource.tempRoot, { recursive: true, force: true });
  }
}

function writeInstallMetadata(packageStore, metadata) {
  const metadataPath = path.join(packageStore, ".product-skills-install.json");
  fs.writeFileSync(metadataPath, `${JSON.stringify(metadata, null, 2)}\n`, "utf8");
}

function addRepoPackageStoreIgnore(plan, context, options) {
  if (context.scope !== "repo" || options.trackPackageStore) {
    return;
  }
  const relativeStore = path.relative(context.repoRoot, context.packageStore).split(path.sep).join("/");
  if (relativeStore !== ".product-skills") {
    return;
  }
  const gitignore = path.join(context.repoRoot, ".gitignore");
  const entry = ".product-skills/";
  const existing = fs.existsSync(gitignore) ? fs.readFileSync(gitignore, "utf8") : "";
  if (existing.split(/\r?\n/).includes(entry)) {
    return;
  }
  const prefix = existing.length > 0 && !existing.endsWith("\n") ? "\n" : "";
  plan.appendFile(gitignore, `${prefix}${entry}\n`);
}

function defaultUpdateSource(cwd) {
  const currentPackageRoot = findProductSkillsRoot(cwd);
  if (currentPackageRoot) {
    return currentPackageRoot;
  }
  if (looksLikeProductSkillsRoot(PACKAGE_ROOT)) {
    return PACKAGE_ROOT;
  }
  return CANONICAL_REPO;
}

function sourceExists(source) {
  return isUrl(String(source)) || fs.existsSync(resolvePath(String(source)));
}

function runPackageValidation(packageStore) {
  requireCommand("python3", "Python 3");
  const checks = [
    ["python3", [path.join(packageStore, "scripts", "check_package.py"), packageStore]],
    ["python3", [path.join(packageStore, "scripts", "run_trigger_evals.py"), packageStore]],
    ["python3", [path.join(packageStore, "scripts", "check_tool_safety.py"), packageStore]],
    ["python3", [path.join(packageStore, "scripts", "check_forward_tests.py"), packageStore]],
    ["python3", [
      "-m",
      "py_compile",
      path.join(packageStore, "scripts", "check_package.py"),
      path.join(packageStore, "scripts", "run_trigger_evals.py"),
      path.join(packageStore, "scripts", "grade_artifact.py"),
      path.join(packageStore, "scripts", "check_tool_safety.py"),
      path.join(packageStore, "scripts", "check_forward_tests.py"),
    ]],
  ];
  const results = [];
  for (const [command, args] of checks) {
    const result = run(command, args, { cwd: packageStore });
    const label = [command, ...args].join(" ");
    results.push({ command: label, status: result.status, stdout: result.stdout, stderr: result.stderr });
    if (result.status !== 0) {
      throw new InstallerError(`Package validation failed: ${label}\n${result.stdout}${result.stderr}`);
    }
  }
  return results;
}

function parseNpmPackDryRun(stdout) {
  try {
    const parsed = JSON.parse(stdout);
    const first = Array.isArray(parsed) ? parsed[0] : parsed;
    return {
      name: first.name,
      version: first.version,
      filename: first.filename,
      files: (first.files ?? []).map((file) => file.path).sort(),
      unpackedSize: first.unpackedSize,
    };
  } catch (error) {
    throw new InstallerError(`Could not parse npm pack --dry-run output: ${error.message}\n${stdout}`);
  }
}

function validatePackedFileList(root, files) {
  const disallowed = [
    /^\.env(?:\.|$)/,
    /^\.product-skills(?:\/|$)/,
    /(?:^|\/)__pycache__(?:\/|$)/,
    /^evals\/results(?:\/|$)/,
    /^docs\/PACKAGE_INSTALLER_/,
    /\.tgz$/,
  ];
  return files.filter((file) => {
    const wouldCopyToPackageStore = shouldCopyPackagePath(root, path.join(root, file));
    return !wouldCopyToPackageStore || disallowed.some((pattern) => pattern.test(file));
  });
}

function runDistributionValidation(root = PACKAGE_ROOT) {
  const version = checkVersionConsistency(root);
  if (!version.ok) {
    const reason = version.missing.length > 0
      ? `Missing version metadata: ${version.missing.join(", ")}`
      : `Version mismatch across release metadata: ${JSON.stringify(version.mismatches)}`;
    throw new InstallerError(`${reason}. Sources: ${JSON.stringify(version.sources)}`);
  }
  requireCommand("npm", "npm");
  const pack = run("npm", ["pack", "--dry-run", "--json", "--ignore-scripts"], {
    cwd: root,
    env: {
      ...process.env,
      npm_config_cache: path.join(os.tmpdir(), "product-skills-npm-cache"),
    },
  });
  if (pack.status !== 0) {
    throw new InstallerError(`npm pack --dry-run failed.\n${pack.stdout}${pack.stderr}`);
  }
  const packResult = parseNpmPackDryRun(pack.stdout);
  const disallowed = validatePackedFileList(root, packResult.files);
  if (disallowed.length > 0) {
    throw new InstallerError(`npm pack --dry-run included excluded files: ${disallowed.join(", ")}`);
  }
  return {
    version,
    pack: packResult,
    checksum: computeSnapshotChecksum(root),
  };
}

function cleanGeneratedValidationOutputs(root) {
  const evalResults = path.join(root, "evals", "results");
  fs.rmSync(evalResults, { recursive: true, force: true });
  const stack = [root];
  while (stack.length > 0) {
    const current = stack.pop();
    if (!fs.existsSync(current)) {
      continue;
    }
    for (const entry of fs.readdirSync(current, { withFileTypes: true })) {
      const entryPath = path.join(current, entry.name);
      if (!entry.isDirectory()) {
        continue;
      }
      if (entry.name === "__pycache__") {
        fs.rmSync(entryPath, { recursive: true, force: true });
      } else {
        stack.push(entryPath);
      }
    }
  }
}

function adapterExistsForRuntime(runtime, context) {
  try {
    return adapterTargets(runtime, context).map((target) => ({
      runtime,
      adapter: target.templateKind,
      path: target.path,
      exists: fs.existsSync(target.path),
      supported: true,
      skipped: false,
      compatibility: target.compatibility ?? null,
    }));
  } catch (error) {
    return [unsupportedAdapter(runtime, error)];
  }
}

function readInstallMetadata(packageStore) {
  const metadataPath = path.join(packageStore, ".product-skills-install.json");
  if (!fs.existsSync(metadataPath)) {
    return {};
  }
  try {
    return JSON.parse(fs.readFileSync(metadataPath, "utf8"));
  } catch {
    return {};
  }
}

function resolveInstalledContext(options) {
  const initialContext = resolveContext(options);
  const metadata = fs.existsSync(initialContext.packageStore) ? readInstallMetadata(initialContext.packageStore) : {};
  if (options.adapter === "auto" && SUPPORTED_ADAPTERS.has(metadata.adapter)) {
    const effectiveOptions = { ...options, adapter: metadata.adapter };
    return {
      context: resolveContext(effectiveOptions),
      options: effectiveOptions,
      metadata,
    };
  }
  return { context: initialContext, options, metadata };
}

async function installCommand(options) {
  const context = resolveContext(options);
  const plan = new Plan({ dryRun: options.dryRun });
  installPackageStore(plan, context, {
    ...options,
    adapter: context.adapter,
    allowUntrustedSource: options.trustSource || options.force,
  });
  addRepoPackageStoreIgnore(plan, context, options);

  let validation = [];
  if (!options.dryRun) {
    validation = runPackageValidation(context.packageStore);
    cleanGeneratedValidationOutputs(context.packageStore);
  } else {
    plan.record("validate", context.packageStore, "dry run skips validation because no package was copied");
  }

  const adapters = writeAdapters(plan, context, options);
  const result = {
    command: "install",
    scope: context.scope,
    runtime: context.runtime,
    packageStore: context.packageStore,
    adapters,
    validation: validation.map((item) => ({ command: item.command, status: item.status })),
    actions: plan.actions,
    dryRun: options.dryRun,
  };
  printResult(result, options);
}

async function updateCommand(options) {
  const resolved = resolveInstalledContext(options);
  const context = resolved.context;
  const effectiveOptions = resolved.options;
  if (!fs.existsSync(context.packageStore)) {
    throw new InstallerError(`Package store does not exist: ${context.packageStore}. Run product-skills install first.`);
  }
  if (!effectiveOptions.dryRun && !effectiveOptions.force) {
    throw new InstallerError("Update would replace the managed package store. Rerun with --force after reviewing status or use --dry-run first.");
  }

  const metadata = resolved.metadata;
  const previousVersion = readVersion(context.packageStore);
  const source = effectiveOptions.source
    ?? (metadata.source && sourceExists(metadata.source) ? metadata.source : defaultUpdateSource(process.cwd()));
  const ref = effectiveOptions.ref ?? metadata.ref ?? undefined;
  const plan = new Plan({ dryRun: effectiveOptions.dryRun });
  const updateOptions = {
    ...effectiveOptions,
    source,
    ref,
    adapter: context.adapter,
    allowUntrustedSource: effectiveOptions.trustSource,
    preservePreviousStore: true,
  };

  if (effectiveOptions.dryRun) {
    plan.record("detect-version", context.packageStore, `current ${previousVersion}`);
  }

  let installResult = null;
  let validation = [];
  try {
    installResult = installPackageStore(plan, context, updateOptions);
    addRepoPackageStoreIgnore(plan, context, updateOptions);

    if (!effectiveOptions.dryRun) {
      validation = runPackageValidation(context.packageStore);
      cleanGeneratedValidationOutputs(context.packageStore);
      if (installResult.previousStore) {
        plan.remove(installResult.previousStore);
      }
    } else {
      plan.record("validate", context.packageStore, "dry run skips validation because no package was copied");
    }
  } catch (error) {
    if (installResult?.previousStore && fs.existsSync(installResult.previousStore)) {
      fs.rmSync(context.packageStore, { recursive: true, force: true });
      fs.renameSync(installResult.previousStore, context.packageStore);
      plan.record("restore", `${installResult.previousStore} -> ${context.packageStore}`, "validation failed");
    }
    throw error;
  }

  const adapters = writeAdapters(plan, context, effectiveOptions);
  printResult({
    command: "update",
    scope: context.scope,
    runtime: context.runtime,
    packageStore: context.packageStore,
    previousVersion,
    version: effectiveOptions.dryRun ? previousVersion : readVersion(context.packageStore),
    source,
    ref: ref ?? null,
    adapters,
    validation: validation.map((item) => ({ command: item.command, status: item.status })),
    actions: plan.actions,
    dryRun: effectiveOptions.dryRun,
  }, effectiveOptions);
}

async function validateCommand(options) {
  const { context, options: effectiveOptions } = resolveInstalledContext(options);
  if (!fs.existsSync(context.packageStore)) {
    throw new InstallerError(`Package store does not exist: ${context.packageStore}. Run product-skills install first.`);
  }
  const validation = runPackageValidation(context.packageStore);
  cleanGeneratedValidationOutputs(context.packageStore);
  const adapters = runtimeList(context.runtime).flatMap((runtime) => adapterExistsForRuntime(runtime, context));
  const missing = adapters.filter((adapter) => !adapter.skipped && !adapter.exists);
  const unsupported = adapters.filter((adapter) => adapter.skipped);
  if (unsupported.length > 0 && context.runtime !== "all") {
    throw new InstallerError(unsupported.map((adapter) => adapter.reason).join("; "));
  }
  if (missing.length > 0) {
    throw new InstallerError(`Missing adapter(s): ${missing.map((item) => `${item.runtime}:${item.path || item.reason || item.error}`).join(", ")}`);
  }
  printResult({
    command: "validate",
    scope: context.scope,
    runtime: context.runtime,
    packageStore: context.packageStore,
    validation: validation.map((item) => ({ command: item.command, status: item.status })),
    adapters,
  }, effectiveOptions);
}

function cleanBackupsForFile(filePath, plan) {
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    return;
  }
  const base = path.basename(filePath);
  for (const entry of fs.readdirSync(dir)) {
    if (entry.startsWith(`${base}.bak.`)) {
      plan.remove(path.join(dir, entry));
    }
  }
}

function removeDedicatedAdapter(plan, target, options) {
  if (!fs.existsSync(target.path)) {
    plan.record("skip", target.path, "adapter missing");
    return { ...target, removed: false, reason: "missing" };
  }
  const existing = fs.readFileSync(target.path, "utf8");
  if (!isGeneratedDedicated(target, existing) && !options.force) {
    throw new InstallerError(`Adapter exists but is not ProductSkills-generated: ${target.path}. Rerun with --force to remove it.`);
  }
  plan.remove(target.path);
  if (target.templateKind === "extension-context") {
    plan.rmdirIfEmpty(path.dirname(target.path));
  }
  if (options.cleanBackups) {
    cleanBackupsForFile(target.path, plan);
  }
  return { ...target, removed: true };
}

function removeSharedAdapter(plan, target, options) {
  if (!fs.existsSync(target.path)) {
    plan.record("skip", target.path, "adapter missing");
    return { ...target, removed: false, reason: "missing" };
  }
  const existing = fs.readFileSync(target.path, "utf8");
  let next;
  try {
    next = removeMarkerBlock(existing, target.path);
  } catch (error) {
    plan.backup(target.path, backupPath(target.path));
    throw error;
  }
  if (next === existing) {
    plan.record("skip", target.path, "ProductSkills marker block missing");
    return { ...target, removed: false, reason: "marker-missing" };
  }
  plan.writeFile(target.path, next);
  if (options.cleanBackups) {
    cleanBackupsForFile(target.path, plan);
  }
  return { ...target, removed: true };
}

function removeAdapters(plan, context, options) {
  const removed = [];
  for (const runtime of runtimeList(context.runtime)) {
    let targets;
    try {
      targets = adapterTargets(runtime, context);
    } catch (error) {
      removed.push({
        runtime,
        adapter: "unsupported",
        path: "",
        removed: false,
        reason: error.message,
      });
      continue;
    }
    for (const target of targets) {
      const result = target.kind === "dedicated"
        ? removeDedicatedAdapter(plan, target, options)
        : removeSharedAdapter(plan, target, options);
      removed.push({
        runtime,
        adapter: target.templateKind,
        path: target.path,
        removed: result.removed,
        reason: result.reason,
      });
    }
  }
  return removed;
}

async function uninstallCommand(options) {
  const resolved = resolveInstalledContext(options);
  const context = resolved.context;
  const effectiveOptions = resolved.options;
  const plan = new Plan({ dryRun: effectiveOptions.dryRun });
  const adapters = removeAdapters(plan, context, effectiveOptions);

  if (effectiveOptions.removePackageStore) {
    plan.remove(context.packageStore);
  } else {
    plan.record("keep", context.packageStore, "package store preserved");
  }

  printResult({
    command: "uninstall",
    scope: context.scope,
    runtime: context.runtime,
    packageStore: context.packageStore,
    removePackageStore: effectiveOptions.removePackageStore,
    adapters,
    actions: plan.actions,
    dryRun: effectiveOptions.dryRun,
  }, effectiveOptions);
}

async function statusCommand(options) {
  const { context, options: effectiveOptions } = resolveInstalledContext(options);
  const exists = fs.existsSync(context.packageStore);
  const metadata = exists ? readInstallMetadata(context.packageStore) : {};
  let validationStatus = "missing";
  if (exists) {
    const result = run("python3", [path.join(context.packageStore, "scripts", "check_package.py"), context.packageStore], { cwd: context.packageStore });
    validationStatus = result.status === 0 ? "pass" : "fail";
  }
  const adapters = runtimeList(context.runtime).flatMap((runtime) => adapterExistsForRuntime(runtime, context));
  printResult({
    command: "status",
    scope: context.scope,
    runtime: context.runtime,
    packageStore: context.packageStore,
    packageStoreExists: exists,
    version: exists ? readVersion(context.packageStore) : null,
    ref: metadata.ref ?? null,
    source: metadata.source ?? null,
    validationStatus,
    adapters,
  }, effectiveOptions);
}

async function checksumCommand(options) {
  const root = options.packageStore ? resolvePath(options.packageStore) : PACKAGE_ROOT;
  if (!fs.existsSync(root) || !fs.statSync(root).isDirectory()) {
    throw new InstallerError(`Checksum target is not a directory: ${root}`);
  }
  printResult({
    command: "checksum",
    root,
    ...computeSnapshotChecksum(root),
  }, options);
}

async function distCheckCommand(options) {
  const root = options.source ? resolvePath(options.source) : PACKAGE_ROOT;
  if (!fs.existsSync(root) || !fs.statSync(root).isDirectory()) {
    throw new InstallerError(`Distribution check source is not a directory: ${root}`);
  }
  const result = runDistributionValidation(root);
  printResult({
    command: "dist-check",
    root,
    version: result.version,
    pack: result.pack,
    checksum: result.checksum,
  }, options);
}

function help() {
  return `Usage: product-skills <command> [options]

Commands:
  install    Install the ProductSkills package store and runtime adapters.
  update     Refresh the package store and regenerate selected adapters.
  uninstall  Remove selected runtime adapters and optionally the package store.
  validate   Validate the package store and selected runtime adapters.
  status     Show installed package and adapter status.
  checksum   Compute a deterministic package snapshot checksum.
  dist-check Validate release metadata and npm pack dry-run contents.

Options:
  --runtime claude|codex|cursor|gemini|all
  --scope user|repo
  --adapter skills|agents|extension|auto
  --repo <path>
  --package-store <path>
  --source <path-or-url>
  --ref <git-ref>
  --force
  --replace
  --dry-run
  --json
  --track-package-store
  --remove-package-store
  --clean-backups
  --trust-source
  --global      Alias for --scope user
  --project     Alias for --scope repo
`;
}

function printTextResult(result) {
  if (result.command === "install" || result.command === "update") {
    console.log(`${result.dryRun ? "DRY RUN " : ""}${result.command === "install" ? "Installed" : "Updated"} ProductSkills`);
    console.log(`- scope: ${result.scope}`);
    console.log(`- runtime: ${result.runtime}`);
    console.log(`- package store: ${result.packageStore}`);
    if (result.previousVersion) {
      console.log(`- version: ${result.previousVersion} -> ${result.version}`);
    }
    for (const adapter of result.adapters) {
      console.log(`- adapter: ${adapter.runtime} ${adapter.adapter} -> ${adapter.path}`);
    }
    if (result.validation.length > 0) {
      console.log("- validation: pass");
    }
    if (result.dryRun) {
      console.log("- dry-run actions:");
      for (const action of result.actions) {
        console.log(`  ${action.action}: ${action.target}${action.detail ? ` (${action.detail})` : ""}`);
      }
    }
    return;
  }
  if (result.command === "uninstall") {
    console.log(`${result.dryRun ? "DRY RUN " : ""}Uninstalled ProductSkills adapters`);
    console.log(`- scope: ${result.scope}`);
    console.log(`- runtime: ${result.runtime}`);
    console.log(`- package store: ${result.removePackageStore ? "removed" : "preserved"} ${result.packageStore}`);
    for (const adapter of result.adapters) {
      console.log(`- adapter: ${adapter.runtime} ${adapter.removed ? "removed" : "kept"} ${adapter.path}`);
    }
    if (result.dryRun) {
      console.log("- dry-run actions:");
      for (const action of result.actions) {
        console.log(`  ${action.action}: ${action.target}${action.detail ? ` (${action.detail})` : ""}`);
      }
    }
    return;
  }
  if (result.command === "validate") {
    console.log("ProductSkills validation passed");
    console.log(`- package store: ${result.packageStore}`);
    for (const adapter of result.adapters) {
      console.log(`- adapter: ${adapter.runtime} -> ${adapter.path}`);
    }
    return;
  }
  if (result.command === "status") {
    console.log("ProductSkills status");
    console.log(`- package store: ${result.packageStore}`);
    console.log(`- installed: ${result.packageStoreExists ? "yes" : "no"}`);
    console.log(`- version: ${result.version ?? "none"}`);
    console.log(`- source: ${result.source ?? "unknown"}`);
    console.log(`- ref: ${result.ref ?? "none"}`);
    console.log(`- validation: ${result.validationStatus}`);
    for (const adapter of result.adapters) {
      console.log(`- adapter: ${adapter.runtime} ${adapter.exists ? "present" : "missing"} ${adapter.path || adapter.reason || adapter.error}`);
    }
    return;
  }
  if (result.command === "checksum") {
    console.log(`ProductSkills checksum ${result.algorithm}:${result.checksum}`);
    console.log(`- root: ${result.root}`);
    console.log(`- files: ${result.fileCount}`);
    return;
  }
  if (result.command === "dist-check") {
    console.log("ProductSkills distribution check passed");
    console.log(`- root: ${result.root}`);
    console.log(`- version: ${result.version.version}`);
    console.log(`- npm pack files: ${result.pack.files.length}`);
    console.log(`- checksum: ${result.checksum.algorithm}:${result.checksum.checksum}`);
  }
}

function printResult(result, options) {
  if (options.json) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    printTextResult(result);
  }
}

async function main(argv = process.argv.slice(2)) {
  ensureSupportedNode();
  const { command, options } = parseArgs(argv);
  switch (command) {
    case "install":
      await installCommand(options);
      return 0;
    case "update":
      await updateCommand(options);
      return 0;
    case "uninstall":
      await uninstallCommand(options);
      return 0;
    case "validate":
      await validateCommand(options);
      return 0;
    case "status":
      await statusCommand(options);
      return 0;
    case "checksum":
      await checksumCommand(options);
      return 0;
    case "dist-check":
      await distCheckCommand(options);
      return 0;
    case "help":
      console.log(help());
      return 0;
    default:
      throw new InstallerError(`Unknown command '${command}'.\n${help()}`);
  }
}

const invokedPath = process.argv[1] ? realpathIfExists(process.argv[1]) : "";
const modulePath = realpathIfExists(CLI_PATH);

if (invokedPath && pathToFileURL(invokedPath).href === pathToFileURL(modulePath).href) {
  main().catch((error) => {
    const message = error instanceof InstallerError ? error.message : (error.stack || error.message);
    console.error(message);
    process.exit(error.code || 1);
  });
}
