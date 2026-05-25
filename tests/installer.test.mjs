import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import {
  checkVersionConsistency,
  computeSnapshotChecksum,
  parseArgs,
  upsertMarkerBlock,
} from "../bin/product-skills.mjs";

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

function copyPackageSource(name) {
  const source = tempDir(name);
  fs.cpSync(REPO_ROOT, source, {
    recursive: true,
    filter: (sourcePath) => !sourcePath.includes(`${path.sep}.git${path.sep}`),
  });
  return source;
}

function runCli(args, { cwd = REPO_ROOT, home = tempDir("home"), env = {} } = {}) {
  return spawnSync(process.execPath, [CLI, ...args], {
    cwd,
    env: {
      ...process.env,
      HOME: home,
      ...env,
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

  const uninstall = parseArgs(["uninstall", "--remove-package-store", "--clean-backups", "--trust-source"]);
  assert.equal(uninstall.options.removePackageStore, true);
  assert.equal(uninstall.options.cleanBackups, true);
  assert.equal(uninstall.options.trustSource, true);
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

test("install.sh dry-run delegates without filesystem mutation", () => {
  const repo = makeRepo("install-sh-dry");
  const result = spawnSync(path.join(REPO_ROOT, "install.sh"), [
    "--runtime",
    "claude",
    "--scope",
    "repo",
    "--repo",
    repo,
    "--source",
    REPO_ROOT,
    "--dry-run",
    "--json",
  ], {
    cwd: REPO_ROOT,
    env: {
      ...process.env,
      HOME: tempDir("install-sh-home"),
    },
    encoding: "utf8",
  });

  assert.equal(result.status, 0, result.stderr || result.stdout);
  const parsed = JSON.parse(result.stdout);
  assert.equal(parsed.command, "install");
  assert.equal(parsed.dryRun, true);
  assert.equal(fs.existsSync(path.join(repo, ".product-skills")), false);
  assert.equal(fs.existsSync(path.join(repo, ".claude")), false);
});

test("install.sh routes explicit checksum command", () => {
  const result = spawnSync(path.join(REPO_ROOT, "install.sh"), [
    "checksum",
    "--json",
  ], {
    cwd: REPO_ROOT,
    env: {
      ...process.env,
      HOME: tempDir("install-sh-checksum-home"),
    },
    encoding: "utf8",
  });

  assert.equal(result.status, 0, result.stderr || result.stdout);
  const parsed = JSON.parse(result.stdout);
  assert.equal(parsed.command, "checksum");
  assert.equal(parsed.algorithm, "sha256");
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

test("repo-scope Codex skills adapter validates", () => {
  const repo = makeRepo("codex-skills-install");

  runJson([
    "install",
    "--runtime",
    "codex",
    "--adapter",
    "skills",
    "--scope",
    "repo",
    "--repo",
    repo,
    "--source",
    REPO_ROOT,
  ]);

  const adapterPath = path.join(repo, ".codex", "skills", "product-operating-system", "SKILL.md");
  assert.match(fs.readFileSync(adapterPath, "utf8"), /Generated by ProductSkills/);

  const validate = runJson([
    "validate",
    "--runtime",
    "codex",
    "--adapter",
    "skills",
    "--scope",
    "repo",
    "--repo",
    repo,
  ]);
  assert.equal(validate.adapters[0].adapter, "skills");
  assert.equal(validate.adapters[0].exists, true);
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

test("user-scope Gemini install preserves existing GEMINI.md content", () => {
  const home = tempDir("gemini-user-home");
  const geminiPath = path.join(home, ".gemini", "GEMINI.md");
  fs.mkdirSync(path.dirname(geminiPath), { recursive: true });
  fs.writeFileSync(geminiPath, "# Existing User Gemini Rules\n", "utf8");

  runJson([
    "install",
    "--runtime",
    "gemini",
    "--scope",
    "user",
    "--source",
    REPO_ROOT,
  ], { home });

  const gemini = fs.readFileSync(geminiPath, "utf8");
  assert.match(gemini, /# Existing User Gemini Rules/);
  assert.match(gemini, /# ProductSkills/);
  assert.equal((gemini.match(/PRODUCT_SKILLS_START/g) ?? []).length, 1);
});

test("Cursor user-scope detection succeeds with a supported fixture", () => {
  const home = tempDir("cursor-user-home");
  const cursorRules = path.join(home, ".cursor", "rules");
  fs.mkdirSync(cursorRules, { recursive: true });

  const result = runJson([
    "install",
    "--runtime",
    "cursor",
    "--scope",
    "user",
    "--source",
    REPO_ROOT,
    "--dry-run",
  ], { home });

  assert.equal(result.adapters[0].runtime, "cursor");
  assert.equal(result.adapters[0].supported, true);
  assert.equal(result.adapters[0].path, path.join(cursorRules, "product-operating-system.mdc"));
});

test("Cursor user-scope env override succeeds with a supported fixture", () => {
  const home = tempDir("cursor-env-home");
  const cursorRules = tempDir("cursor-env-rules");

  const result = runJson([
    "install",
    "--runtime",
    "cursor",
    "--scope",
    "user",
    "--source",
    REPO_ROOT,
    "--dry-run",
  ], {
    home,
    env: {
      PRODUCT_SKILLS_CURSOR_USER_RULES_DIR: cursorRules,
    },
  });

  assert.equal(result.adapters[0].compatibility, "PRODUCT_SKILLS_CURSOR_USER_RULES_DIR");
  assert.equal(result.adapters[0].path, path.join(cursorRules, "product-operating-system.mdc"));
});

test("Cursor user-scope install writes detected rule file", () => {
  const home = tempDir("cursor-user-write-home");
  const cursorRules = path.join(home, ".cursor", "rules");
  fs.mkdirSync(cursorRules, { recursive: true });

  runJson([
    "install",
    "--runtime",
    "cursor",
    "--scope",
    "user",
    "--source",
    REPO_ROOT,
  ], { home });

  const adapterPath = path.join(cursorRules, "product-operating-system.mdc");
  assert.equal(fs.existsSync(adapterPath), true);
  assert.match(fs.readFileSync(adapterPath, "utf8"), /Generated by ProductSkills/);
});


test("Cursor user-scope detection fails gracefully when unsupported", () => {
  const home = tempDir("cursor-user-unsupported-home");
  const result = runCli([
    "install",
    "--runtime",
    "cursor",
    "--scope",
    "user",
    "--source",
    REPO_ROOT,
    "--dry-run",
  ], { home });

  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /Cursor user scope requires an existing supported global rules directory/);
});

test("update requires force for non-dry-run package replacement", () => {
  const repo = makeRepo("update-no-force");
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

  const result = runCli([
    "update",
    "--runtime",
    "codex",
    "--adapter",
    "agents",
    "--scope",
    "repo",
    "--repo",
    repo,
  ]);

  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /Rerun with --force/);
});

test("update refreshes package store and replaces only managed marker block", () => {
  const repo = makeRepo("update-force");
  const source = copyPackageSource("update-source");
  fs.writeFileSync(path.join(source, "VERSION"), "0.2.0\n", "utf8");
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
  const update = runJson([
    "update",
    "--runtime",
    "codex",
    "--adapter",
    "agents",
    "--scope",
    "repo",
    "--repo",
    repo,
    "--source",
    source,
    "--force",
    "--trust-source",
  ]);

  assert.equal(update.previousVersion, "0.1.0");
  assert.equal(update.version, "0.2.0");
  assert.equal(fs.readFileSync(path.join(repo, ".product-skills", "VERSION"), "utf8").trim(), "0.2.0");
  const agents = fs.readFileSync(path.join(repo, "AGENTS.md"), "utf8");
  assert.match(agents, /# Repo Rules/);
  assert.equal((agents.match(/PRODUCT_SKILLS_START/g) ?? []).length, 1);
});

test("update refuses untrusted source even when force confirms replacement", () => {
  const repo = makeRepo("update-untrusted");
  const source = copyPackageSource("update-untrusted-source");

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
  const result = runCli([
    "update",
    "--runtime",
    "codex",
    "--adapter",
    "agents",
    "--scope",
    "repo",
    "--repo",
    repo,
    "--source",
    source,
    "--force",
  ]);

  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /--trust-source/);
  assert.equal(fs.readFileSync(path.join(repo, ".product-skills", "VERSION"), "utf8").trim(), "0.1.0");
});

test("failed update restores previous package store", () => {
  const repo = makeRepo("update-rollback");
  const source = copyPackageSource("update-broken-source");
  fs.writeFileSync(path.join(source, "VERSION"), "0.3.0\n", "utf8");
  fs.writeFileSync(path.join(source, "registry.json"), "{ broken json\n", "utf8");

  runJson([
    "install",
    "--runtime",
    "claude",
    "--scope",
    "repo",
    "--repo",
    repo,
    "--source",
    REPO_ROOT,
  ]);

  const result = runCli([
    "update",
    "--runtime",
    "claude",
    "--scope",
    "repo",
    "--repo",
    repo,
    "--source",
    source,
    "--force",
    "--trust-source",
  ]);

  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /Package validation failed/);
  assert.equal(fs.readFileSync(path.join(repo, ".product-skills", "VERSION"), "utf8").trim(), "0.1.0");
  assert.equal(fs.existsSync(path.join(repo, ".product-skills", "registry.json")), true);
});

test("uninstall removes shared marker block and preserves package store by default", () => {
  const repo = makeRepo("uninstall-shared");
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
  const uninstall = runJson([
    "uninstall",
    "--runtime",
    "gemini",
    "--scope",
    "repo",
    "--repo",
    repo,
  ]);

  assert.equal(uninstall.removePackageStore, false);
  assert.equal(fs.existsSync(path.join(repo, ".product-skills")), true);
  const gemini = fs.readFileSync(path.join(repo, "GEMINI.md"), "utf8");
  assert.match(gemini, /# Existing Gemini Rules/);
  assert.doesNotMatch(gemini, /PRODUCT_SKILLS_START/);
});

test("uninstall removes generated adapters and package store when requested", () => {
  const repo = makeRepo("uninstall-store");
  runJson([
    "install",
    "--runtime",
    "claude",
    "--scope",
    "repo",
    "--repo",
    repo,
    "--source",
    REPO_ROOT,
  ]);
  const adapterPath = path.join(repo, ".claude", "skills", "product-operating-system", "SKILL.md");
  assert.equal(fs.existsSync(adapterPath), true);

  runJson([
    "uninstall",
    "--runtime",
    "claude",
    "--scope",
    "repo",
    "--repo",
    repo,
    "--remove-package-store",
  ]);

  assert.equal(fs.existsSync(adapterPath), false);
  assert.equal(fs.existsSync(path.join(repo, ".product-skills")), false);
});

test("uninstall refuses non-generated dedicated adapters unless forced", () => {
  const repo = makeRepo("uninstall-custom");
  const adapterPath = path.join(repo, ".claude", "skills", "product-operating-system", "SKILL.md");
  fs.mkdirSync(path.dirname(adapterPath), { recursive: true });
  fs.writeFileSync(adapterPath, "# Custom adapter\n", "utf8");

  const failed = runCli([
    "uninstall",
    "--runtime",
    "claude",
    "--scope",
    "repo",
    "--repo",
    repo,
  ]);
  assert.notEqual(failed.status, 0);
  assert.match(failed.stderr, /not ProductSkills-generated/);

  runJson([
    "uninstall",
    "--runtime",
    "claude",
    "--scope",
    "repo",
    "--repo",
    repo,
    "--force",
  ]);
  assert.equal(fs.existsSync(adapterPath), false);
});

test("user-scope uninstall all skips unsupported Cursor without aborting", () => {
  const home = tempDir("uninstall-user-home");
  const claudePath = path.join(home, ".claude", "skills", "product-operating-system", "SKILL.md");
  fs.mkdirSync(path.dirname(claudePath), { recursive: true });
  fs.writeFileSync(claudePath, [
    "---",
    "name: product-operating-system",
    "description: Test",
    "---",
    "",
  ].join("\n"), "utf8");

  const result = runJson([
    "uninstall",
    "--runtime",
    "all",
    "--scope",
    "user",
  ], { home });

  assert.equal(result.adapters.some((adapter) => adapter.runtime === "cursor" && adapter.reason.includes("Cursor user scope")), true);
  assert.equal(fs.existsSync(claudePath), false);
});

test("user-scope install all skips unsupported Cursor without aborting", () => {
  const home = tempDir("install-all-user-home");
  const result = runJson([
    "install",
    "--runtime",
    "all",
    "--scope",
    "user",
    "--source",
    REPO_ROOT,
    "--dry-run",
  ], { home });

  const cursor = result.adapters.find((adapter) => adapter.runtime === "cursor");
  assert.equal(cursor.skipped, true);
  assert.match(cursor.reason, /Cursor user scope requires/);
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

test("version consistency check passes and reports mismatches", () => {
  const ok = checkVersionConsistency(REPO_ROOT);
  assert.equal(ok.ok, true);
  assert.equal(ok.version, "0.1.0");

  const source = copyPackageSource("version-mismatch");
  const registry = JSON.parse(fs.readFileSync(path.join(source, "registry.json"), "utf8"));
  registry.version = "9.9.9";
  fs.writeFileSync(path.join(source, "registry.json"), `${JSON.stringify(registry, null, 2)}\n`, "utf8");

  const mismatch = checkVersionConsistency(source);
  assert.equal(mismatch.ok, false);
  assert.ok(mismatch.mismatches.some((item) => item.name === "registry.json" && item.version === "9.9.9"));
});

test("snapshot checksum generation is deterministic", () => {
  const first = computeSnapshotChecksum(REPO_ROOT);
  const second = computeSnapshotChecksum(REPO_ROOT);

  assert.equal(first.algorithm, "sha256");
  assert.equal(first.checksum, second.checksum);
  assert.equal(first.fileCount, second.fileCount);
});

test("snapshot checksum changes when a packaged file changes", () => {
  const source = copyPackageSource("checksum-sensitive");
  const first = computeSnapshotChecksum(source);
  fs.appendFileSync(path.join(source, "README.md"), "\nChecksum sensitivity fixture.\n", "utf8");
  const second = computeSnapshotChecksum(source);

  assert.notEqual(first.checksum, second.checksum);
});

test("distribution dry-run excludes construction and generated files", () => {
  const result = runJson(["dist-check"]);
  const packedFiles = result.pack.files;

  assert.equal(result.version.ok, true);
  assert.ok(packedFiles.includes("bin/product-skills.mjs"));
  assert.ok(packedFiles.includes("install.sh"));
  assert.ok(packedFiles.includes("docs/LOCAL_INSTALLATION.md"));
  assert.equal(packedFiles.some((file) => file.startsWith("docs/PACKAGE_INSTALLER_")), false);
  assert.equal(packedFiles.some((file) => file.startsWith(".product-skills/")), false);
  assert.equal(packedFiles.some((file) => file.includes("__pycache__")), false);
  assert.equal(packedFiles.some((file) => file.startsWith("evals/results/")), false);
});

test("distribution dry-run fails on version mismatch", () => {
  const source = copyPackageSource("dist-version-mismatch");
  const registry = JSON.parse(fs.readFileSync(path.join(source, "registry.json"), "utf8"));
  registry.version = "9.9.9";
  fs.writeFileSync(path.join(source, "registry.json"), `${JSON.stringify(registry, null, 2)}\n`, "utf8");

  const result = runCli(["dist-check", "--source", source]);

  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /Version mismatch across release metadata/);
  assert.match(result.stderr, /registry\.json/);
});
