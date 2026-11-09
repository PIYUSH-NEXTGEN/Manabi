/** Shared GitHub repo-URL rules used by the submit panel, the repo-analyzer
 * placeholder and the msw mock (which mirrors the backend's own checks). */
export const GITHUB_REPO_URL_PATTERN = /^https:\/\/github\.com\/[\w.-]+\/[\w.-]+$/;

/** Drop the optional .git suffix so `owner/repo.git` and `owner/repo` are the same repo. */
export function stripGitSuffix(repoUrl: string): string {
  return repoUrl.replace(/\.git$/, '');
}
