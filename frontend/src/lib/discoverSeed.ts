const discoverSeeds = new Map<string, number>();

export function discoverSeedFor(
  locationKey: string,
  random: () => number = Math.random,
): number {
  const cached = discoverSeeds.get(locationKey);
  if (cached !== undefined) return cached;

  const seed = Math.floor(random() * 2_000_000_000) + 1;
  discoverSeeds.set(locationKey, seed);
  return seed;
}

export function clearDiscoverSeeds(): void {
  discoverSeeds.clear();
}
