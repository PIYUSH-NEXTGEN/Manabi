import { AskManabi } from '@/components/home/AskManabi';
import { BuildInPublic } from '@/components/home/BuildInPublic';
import { FeaturedProblems } from '@/components/home/FeaturedProblems';
import { FinalCta } from '@/components/home/FinalCta';
import { Hero } from '@/components/home/Hero';
import { MarqueeTape } from '@/components/home/MarqueeTape';
import { useFacets } from '@/hooks/useFacets';
import { useProblems } from '@/hooks/useProblems';

export function HomePage() {
  const facets = useFacets();
  const problems = useProblems({ sort: 'newest', limit: 3 });

  return (
    <main>
      <Hero />
      <MarqueeTape query={facets} />
      <FeaturedProblems query={problems} />
      <BuildInPublic />
      <AskManabi />
      <FinalCta />
    </main>
  );
}
