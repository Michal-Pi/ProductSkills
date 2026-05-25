import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { parseArgs, upsertMarkerBlock } from "../bin/product-skills.mjs";

const REPO_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const CLI = path.join(REPO_ROOT, "bin", "product-skills.mjs");

function tempDir(name) {
  return fs.mkdtempSync(path.join(os.tmpdir(), `product-skills-${name}-`));
}

function makeRepo(name) {
  const repo = tempDir(name);
  fs.mkdirSync(path.join(repo, ".git"));
  return repo;
}

function runCli(args, { cwd = REPO_ROOT, home = tempDir("home") } = {}) {
  return spawnSync(process.execPath, [CLI, ...args], {
    cwd,
    env: {
      ...process.env,
      HOME: home,
    },
    encoding: "utf8",
  });
}

function runJson(args, options) {
  const result = runCli([...args, "--json"], options);
  assert.equal(result.status, 0, result.stderr || result.stdout);
  return JSON.parse(result.stdout);
}

test("parses scope aliases and adapter options", () => {
  const parsed = parseArgs(["install", "--runtime", "codex", "--global", "--adapter=agents"]);
  assert.equal(parsed.command, "install");
  assert.equal(parsed.options.runtime, "codex");
  assert.equal(parsed.options.scope, "user");
  assert.equal(parsed.options.adapter, "agents");

  const project = parseArgs(["status", "--project"]);
  assert.equal(project.options.scope, "repo");
});

test("marker replacement is idempotent and detects malformed markers", () => {
  const block = [
    "<!-- PRODUCT_SKILLS_START -->",
    "# ProductSkills",
    "<!-- PRODUCT_SKILLS_END -->",
  ].join("\n");
  const first = upsertMarkerBlock("# Existing\n", block, "AGENTS.md");
  const second = upsertMarkerBlock(first, block, "AGENTS.md");
  assert.equal((second.match(/PRODUCT_SKILLS_START/g) ?? []).length, 1);
  const changed = upsertMarkerBlock(
    `before\n\n${block}\n\nafter\n`,
    [
      "<!-- PRODUCT_SKILLS_START -->",
      "# ProductSkills Changed",
      "<!-- PRODUCT_SKILLS_END -->",
    ].join("\n"),
    "AGENTS.md"
  );
  assert.match(changed, /^before/);
  assert.match(changed, /# ProductSkills Changed/);
  assert.match(changed, /after\n$/);
  assert.throws(
    () => upsertMarkerBlock("prefix\n<!-- PRODUCT_SKILLS_START -->\n", block, "AGENTS.md"),
    /Malformed ProductSkills marker block/
  );
});

test("linked product-skills bin invokes the CLI through a symlink", () => {
  const dir = tempDir("linked-bin");
  const linked = path.join(dir, "product-skills");
  fs.symlinkSync(CLI, linked);

  const result = spawnSync(process.execPath, [linked, "help"], {
    cwd: REPO_ROOT,
    encoding: "utf8",
  });

  assert.equal(result.status, 0, result.stderr || result.stdout);
  assert.match(result.stdout, /Usage: product-skills/);
});

test("dry-run install reports repo-scope Claude adapter writes", () => {
  const repo = makeRepo("claude-dry");
  const result = runJson([
    "install",
    "--runtime",
    "claude",
    "--scope",
    "repo",
    "--repo",
    repo,
    "--source",
    REPO_ROOT,
    "--dry-run",
  ]);

  assert.equal(result.dryRun, true);
  assert.equal(result.packageStore, path.join(repo, ".product-skills"));
  assert.ok(result.adapters.some((adapter) => adapter.path.endsWith(".claude/skills/product-operating-system/SKILL.md")));
  assert.equal(fs.existsSync(path.join(repo, ".product-skills")), false);
});

test("dry-run install reports repo-scope Cursor adapter writes", () => {
  const repo = makeRepo("cursor-dry");
  const result = runJson([
    "install",
    "--runtime",
    "cursor",
    "--scope",
    "repo",
    "--repo",
    repo,
    "--source",
    REPO_ROOT,
    "--dry-run",
  ]);

  assert.ok(result.adapters.some((adapter) => adapter.path.endsWith(".cursor/rules/product-operating-system.mdc")));
});

test("repo-scope Codex AGENTS install preserves marker block idempotently", () => {
  const repo = makeRepo("codex-install");
  fs.writeFileSync(path.join(repo, "AGENTS.md"), "# Repo Rules\n", "utf8");

  runJson([
    "install",
    "--runtime",
    "codex",
    "--adapter",
    "agents",
    "--scope",
    "repo",
    "--repo",
    repo,
    "--source",
    REPO_ROOT,
  ]);
  runJson([
    "install",
    "--runtime",
    "codex",
    "--adapter",
    "agents",
    "--scope",
    "repo",
    "--repo",
    repo,
    "--source",
    REPO_ROOT,
  ]);

  const agents = fs.readFileSync(path.join(repo, "AGENTS.md"), "utf8");
  assert.match(agents, /# Repo Rules/);
  assert.equal((agents.match(/PRODUCT_SKILLS_START/g) ?? []).length, 1);
  assert.equal(fs.readFileSync(path.join(repo, ".product-skills", "VERSION"), "utf8").trim(), "0.1.0");
  assert.equal(fs.existsSync(path.join(repo, ".product-skills", ".git")), false);
  assert.equal(fs.existsSync(path.join(repo, ".product-skills", "scripts", "__pycache__")), false);
  assert.equal(fs.existsSync(path.join(repo, ".product-skills", "docs", "PACKAGE_INSTALLER_SDD.md")), false);
  assert.equal(fs.existsSync(path.join(repo, ".product-skills", "docs", "OPINIONATED_E2E_WORKFLOW_EXPANSION_PLAN.md")), false);
  assert.match(fs.readFileSync(path.join(repo, ".gitignore"), "utf8"), /^\.product-skills\/$/m);

  const validate = runJson([
    "validate",
    "--runtime",
    "codex",
    "--adapter",
    "agents",
    "--scope",
    "repo",
    "--repo",
    repo,
  ]);
  assert.equal(validate.command, "validate");
  const status = runJson([
    "status",
    "--runtime",
    "codex",
    "--adapter",
    "agents",
    "--scope",
    "repo",
    "--repo",
    repo,
  ]);
  assert.equal(status.validationStatus, "pass");
});

test("repo-scope Gemini install preserves existing GEMINI.md content", () => {
  const repo = makeRepo("gemini-install");
  fs.writeFileSync(path.join(repo, "GEMINI.md"), "# Existing Gemini Rules\n\nKeep this.\n", "utf8");

  runJson([
    "install",
    "--runtime",
    "gemini",
    "--scope",
    "repo",
    "--repo",
    repo,
    "--source",
    REPO_ROOT,
  ]);

  const gemini = fs.readFileSync(path.join(repo, "GEMINI.md"), "utf8");
  assert.match(gemini, /# Existing Gemini Rules/);
  assert.match(gemini, /# ProductSkills/);
  assert.equal((gemini.match(/PRODUCT_SKILLS_START/g) ?? []).length, 1);
});

test("dry-run Gemini with existing GEMINI.md does not mutate the file", () => {
  const repo = makeRepo("gemini-dry");
  const geminiPath = path.join(repo, "GEMINI.md");
  fs.writeFileSync(geminiPath, "# Existing Gemini Rules\n", "utf8");
  const before = fs.readFileSync(geminiPath, "utf8");

  runJson([
    "install",
    "--runtime",
    "gemini",
    "--scope",
    "repo",
    "--repo",
    repo,
    "--source",
    REPO_ROOT,
    "--dry-run",
  ]);

  assert.equal(fs.readFileSync(geminiPath, "utf8"), before);
});

test("install refuses to execute validation scripts from an untrusted source without force", () => {
  const repo = makeRepo("untrusted-target");
  const source = tempDir("untrusted-source");
  fs.writeFileSync(path.join(source, "package.yaml"), "name: product-operating-system\nversion: 0.1.0\n", "utf8");
  fs.writeFileSync(path.join(source, "registry.json"), "{\"skills\":[]}\n", "utf8");
  fs.mkdirSync(path.join(source, "skills", "workflow-product-operating-system"), { recursive: true });
  fs.writeFileSync(path.join(source, "skills", "workflow-product-operating-system", "SKILL.md"), "---\nname: workflow-product-operating-system\ndescription: Test\n---\n", "utf8");

  const result = runCli([
    "install",
    "--runtime",
    "claude",
    "--scope",
    "repo",
    "--repo",
    repo,
    "--source",
    source,
  ]);

  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /Refusing to execute validation scripts from untrusted source/);
  assert.equal(fs.existsSync(path.join(repo, ".product-skills")), false);
});

test("self-install dry-run from the ProductSkills repo avoids package-store mutation", () => {
  const packageStore = path.join(tempDir("self-store"), ".product-skills");
  const result = runJson([
    "install",
    "--runtime",
    "claude",
    "--scope",
    "repo",
    "--package-store",
    packageStore,
    "--dry-run",
  ], { cwd: REPO_ROOT });

  assert.equal(result.dryRun, true);
  assert.ok(result.actions.some((action) => action.action === "copy-package"));
  assert.equal(fs.existsSync(packageStore), false);
});
