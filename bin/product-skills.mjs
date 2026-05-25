#!/usr/bin/env node

import { spawnSync } from "node:child_process";
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
const SUPPORTED_ADAPTERS = new Set(["skills", "agents", "auto"]);
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
    throw new InstallerError(`Invalid adapter '${options.adapter}'. Use skills, agents, or auto.`);
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
    return path.join(PACKAGE_ROOT, "adapters", "gemini", "GEMINI.md");
  }
  throw new InstallerError(`Unsupported runtime '${runtime}'`);
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
      throw new InstallerError("Cursor user scope is not supported yet. Use --scope repo for Cursor installs.");
    }
    return [{
      runtime,
      kind: "dedicated",
      templateKind: "rules",
      path: path.join(repoRoot, ".cursor", "rules", "product-operating-system.mdc"),
    }];
  }
  if (runtime === "gemini") {
    return [{
      runtime,
      kind: "shared",
      templateKind: "context",
      path: scope === "repo" ? path.join(repoRoot, "GEMINI.md") : path.join(os.homedir(), ".gemini", "GEMINI.md"),
    }];
  }
  throw new InstallerError(`Unsupported runtime '${runtime}'`);
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
  return content.includes("Generated by ProductSkills");
}

function timestamp() {
  const date = new Date();
  const pad = (value) => String(value).padStart(2, "0");
  return `${date.getUTCFullYear()}${pad(date.getUTCMonth() + 1)}${pad(date.getUTCDate())}T${pad(date.getUTCHours())}${pad(date.getUTCMinutes())}${pad(date.getUTCSeconds())}Z`;
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
    const next = upsertMarkerBlock(existing, rendered, target.path);
    plan.writeFile(target.path, next);
    return;
  }
  plan.writeFile(target.path, rendered.trimEnd() + "\n");
}

function writeAdapters(plan, context, options) {
  const installed = [];
  for (const runtime of runtimeList(context.runtime)) {
    const targets = adapterTargets(runtime, context);
    for (const target of targets) {
      const rendered = renderAdapter(target, context);
      if (target.kind === "dedicated") {
        writeDedicatedAdapter(plan, target, rendered, options);
      } else {
        writeSharedAdapter(plan, target, rendered, options);
      }
      installed.push({ runtime, adapter: target.templateKind, path: target.path });
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
    if (!stagedSource.trusted && !options.force) {
      throw new InstallerError(
        `Refusing to execute validation scripts from untrusted source: ${source}. Use the canonical repository, run from the current ProductSkills checkout, or rerun with --force if you trust this source.`
      );
    }
    plan.mkdir(path.dirname(context.packageStore));
    const nextStore = `${context.packageStore}.tmp.${process.pid}.${Date.now()}`;
    plan.record("copy-package", nextStore, `staged from ${stagedSource.sourceRoot}`);
    try {
      copyFiltered(stagedSource.staged, nextStore);
      plan.remove(context.packageStore);
      plan.record("move", `${nextStore} -> ${context.packageStore}`);
      fs.renameSync(nextStore, context.packageStore);
    } catch (error) {
      fs.rmSync(nextStore, { recursive: true, force: true });
      throw error;
    }
    writeInstallMetadata(context.packageStore, {
      source: String(source),
      sourceRoot: stagedSource.sourceRoot,
      trustedSource: stagedSource.trusted,
      ref: options.ref ?? null,
      installedAt: new Date().toISOString(),
    });
    return { source, sourceRoot: stagedSource.sourceRoot };
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
    }));
  } catch (error) {
    return [{
      runtime,
      adapter: "unsupported",
      path: "",
      exists: false,
      error: error.message,
    }];
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

async function installCommand(options) {
  const context = resolveContext(options);
  const plan = new Plan({ dryRun: options.dryRun });
  installPackageStore(plan, context, options);
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

async function validateCommand(options) {
  const context = resolveContext(options);
  if (!fs.existsSync(context.packageStore)) {
    throw new InstallerError(`Package store does not exist: ${context.packageStore}. Run product-skills install first.`);
  }
  const validation = runPackageValidation(context.packageStore);
  cleanGeneratedValidationOutputs(context.packageStore);
  const adapters = runtimeList(context.runtime).flatMap((runtime) => adapterExistsForRuntime(runtime, context));
  const missing = adapters.filter((adapter) => !adapter.exists);
  if (missing.length > 0) {
    throw new InstallerError(`Missing adapter(s): ${missing.map((item) => `${item.runtime}:${item.path || item.error}`).join(", ")}`);
  }
  printResult({
    command: "validate",
    scope: context.scope,
    runtime: context.runtime,
    packageStore: context.packageStore,
    validation: validation.map((item) => ({ command: item.command, status: item.status })),
    adapters,
  }, options);
}

async function statusCommand(options) {
  const context = resolveContext(options);
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
  }, options);
}

function help() {
  return `Usage: product-skills <command> [options]

Commands:
  install    Install the ProductSkills package store and runtime adapters.
  validate   Validate the package store and selected runtime adapters.
  status     Show installed package and adapter status.

Options:
  --runtime claude|codex|cursor|gemini|all
  --scope user|repo
  --adapter skills|agents|auto
  --repo <path>
  --package-store <path>
  --source <path-or-url>
  --ref <git-ref>
  --force
  --replace
  --dry-run
  --json
  --track-package-store
  --global      Alias for --scope user
  --project     Alias for --scope repo
`;
}

function printTextResult(result) {
  if (result.command === "install") {
    console.log(`${result.dryRun ? "DRY RUN " : ""}Installed ProductSkills`);
    console.log(`- scope: ${result.scope}`);
    console.log(`- runtime: ${result.runtime}`);
    console.log(`- package store: ${result.packageStore}`);
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
      console.log(`- adapter: ${adapter.runtime} ${adapter.exists ? "present" : "missing"} ${adapter.path || adapter.error}`);
    }
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
    case "validate":
      await validateCommand(options);
      return 0;
    case "status":
      await statusCommand(options);
      return 0;
    case "help":
      console.log(help());
      return 0;
    case "update":
    case "uninstall":
      throw new InstallerError(`${command} is deferred to a later installer phase.`);
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
