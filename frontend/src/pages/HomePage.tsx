import { AskManabi } from '@/components/home/AskManabi';
import { BuildInPublic } from '@/components/home/BuildInPublic';
import { FeaturedProblems } from '@/components/home/FeaturedProblems';
import { FinalCta } from '@/components/home/FinalCta';
import { Hero } from '@/components/home/Hero';
import { MarqueeTape } from '@/components/home/MarqueeTape';
import { MlTeaser } from '@/components/home/MlTeaser';
import { StatsStrip } from '@/components/home/StatsStrip';
import { useFacets } from '@/hooks/useFacets';
import { useProblems } from '@/hooks/useProblems';
import { useStats } from '@/hooks/useStats';

export function HomePage() {
  const stats = useStats();
  const facets = useFacets();
  const problems = useProblems({ sort: 'newest', limit: 3 });

  return (
    <main>
      <Hero />
      <MarqueeTape query={facets} />
      <StatsStrip query={stats} />
      <FeaturedProblems query={problems} />
      <MlTeaser />
      <BuildInPublic />
      <AskManabi />
      <FinalCta />
    </main>
  );
}
