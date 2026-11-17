import { describe, expect, it } from 'vitest';
import { clearDiscoverSeeds, discoverSeedFor } from './discoverSeed';

describe('discoverSeedFor', () => {
  it('keeps the same seed for the same history entry', () => {
    const values = [0.1, 0.9];
    let calls = 0;

    const first = discoverSeedFor('same-entry', () => values[calls++]);
    const second = discoverSeedFor('same-entry', () => values[calls++]);

    expect(second).toBe(first);
    expect(calls).toBe(1);
  });

  it('creates a fresh seed for a different history entry', () => {
    const first = discoverSeedFor('entry-one', () => 0.1);
    const second = discoverSeedFor('entry-two', () => 0.9);

    expect(second).not.toBe(first);
  });

  it('recreates the seed after the board history is cleared', () => {
    const first = discoverSeedFor('cleared-entry', () => 0.1);
    clearDiscoverSeeds();
    const second = discoverSeedFor('cleared-entry', () => 0.9);

    expect(second).not.toBe(first);
  });
});
