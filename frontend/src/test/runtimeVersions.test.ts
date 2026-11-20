import { readFileSync } from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';

const repoRoot = path.resolve(process.cwd(), '..');

function readRepoFile(relativePath: string): string {
  return readFileSync(path.join(repoRoot, relativePath), 'utf8');
}

describe('runtime version metadata', () => {
  it('keeps the pinned Node version consistent across local, CI, and Render', () => {
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
    expect(readRepoFile('render.yaml')).toMatch(
      new RegExp(`key: NODE_VERSION\\s+value: ${nodeVersion.replaceAll('.', '\\.')}`),
    );
  });
});
