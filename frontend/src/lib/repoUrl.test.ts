import { describe, expect, it } from 'vitest';
import { GITHUB_REPO_URL_PATTERN, stripGitSuffix } from './repoUrl';

describe('GITHUB_REPO_URL_PATTERN', () => {
  it('accepts owner/name https URLs', () => {
    expect(GITHUB_REPO_URL_PATTERN.test('https://github.com/owner/name')).toBe(true);
  });

  it('accepts word, dot, dash and underscore in names', () => {
    expect(GITHUB_REPO_URL_PATTERN.test('https://github.com/octocat/triage_2.0')).toBe(true);
    expect(GITHUB_REPO_URL_PATTERN.test('https://github.com/demo-org/my-app.web')).toBe(true);
  });

  it('rejects http (insecure) hosts', () => {
    expect(GITHUB_REPO_URL_PATTERN.test('http://github.com/owner/name')).toBe(false);
  });

  it('rejects extra path segments, missing names, and other hosts', () => {
    expect(GITHUB_REPO_URL_PATTERN.test('https://github.com/owner/name/issues')).toBe(false);
    expect(GITHUB_REPO_URL_PATTERN.test('https://github.com/owner')).toBe(false);
    expect(GITHUB_REPO_URL_PATTERN.test('https://gitlab.com/owner/name')).toBe(false);
    expect(GITHUB_REPO_URL_PATTERN.test('https://github.com//name')).toBe(false);
  });

  it('rejects percent-encoding that changes the path when decoded', () => {
    expect(GITHUB_REPO_URL_PATTERN.test('https://github.com/a%2Fb/c')).toBe(false);
  });
});

describe('stripGitSuffix', () => {
  it('drops exactly one trailing .git', () => {
    expect(stripGitSuffix('https://github.com/owner/name.git')).toBe(
      'https://github.com/owner/name',
    );
  });

  it('leaves plain URLs untouched', () => {
    expect(stripGitSuffix('https://github.com/owner/name')).toBe(
      'https://github.com/owner/name',
    );
    expect(stripGitSuffix('https://github.com/owner/name.web')).toBe(
      'https://github.com/owner/name.web',
    );
  });
});
