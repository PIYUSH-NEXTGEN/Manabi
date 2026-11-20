import { readFileSync } from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';

const repoRoot = path.resolve(process.cwd(), '..');

function readRepoFile(relativePath: string): string {
  return readFileSync(path.join(repoRoot, relativePath), 'utf8');
}

describe('runtime version metadata', () => {
  it('keeps the pinned Node version consistent across local and CI', () => {
    const nodeVersion = readRepoFile('.node-version').trim();
    const packageJson = JSON.parse(readRepoFile('frontend/package.json')) as {
      engines?: { node?: string; npm?: string };
    };

    expect(nodeVersion).toMatch(/^\d+\.\d+\.\d+$/);
    expect(packageJson.engines?.node).toBe(`>=${nodeVersion}`);
    expect(packageJson.engines?.npm).toBe('>=10');
    expect(readRepoFile('.github/workflows/ci.yml')).toContain(
      'node-version-file: .node-version',
    );
  });

  it('deploys Render as a Python-only service that does not build the frontend', () => {
    const renderYaml = readRepoFile('render.yaml');

    // Cloudflare Pages builds the frontend, so Render must not pin or install
    // Node for a bundle it never produces.
    expect(renderYaml).toMatch(/runtime: python/);
    expect(renderYaml).not.toContain('NODE_VERSION');
    expect(renderYaml).not.toContain('npm');
  });
});
