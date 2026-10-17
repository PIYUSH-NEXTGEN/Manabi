import { describe, expect, it } from 'vitest';
import { markdownExcerpt } from './markdownExcerpt';

describe('markdownExcerpt', () => {
  it('strips markdown syntax and collapses whitespace', () => {
    const excerpt = markdownExcerpt(
      '## Monday morning\nYour **model** served [12k](http://x) requests.\n\n- one\n- two',
    );

    expect(excerpt).toBe('Monday morning Your model served 12k requests. one two');
  });

  it('truncates long scenarios with an ellipsis', () => {
    const long = 'word '.repeat(100);
    const excerpt = markdownExcerpt(long, 50);

    expect(excerpt.length).toBeLessThanOrEqual(51);
    expect(excerpt.endsWith('…')).toBe(true);
  });

  it('removes fenced code blocks', () => {
    const excerpt = markdownExcerpt('Before\n```python\nsecret = 1\n```\nAfter');
    expect(excerpt).toBe('Before After');
  });
});
