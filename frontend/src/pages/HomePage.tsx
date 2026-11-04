import { AskManabi } from '@/components/home/AskManabi';
import { BuildInPublic } from '@/components/home/BuildInPublic';
import { FeaturedProblems } from '@/components/home/FeaturedProblems';
import { FinalCta } from '@/components/home/FinalCta';
import { Hero } from '@/components/home/Hero';
import { useProblems } from '@/hooks/useProblems';

export function HomePage() {
  const problems = useProblems({ sort: 'newest', limit: 3 });

  return (
    <main>
      <Hero />
      <FeaturedProblems query={problems} />
      <BuildInPublic />
      <AskManabi />
      <FinalCta />
    </main>
  );
}
