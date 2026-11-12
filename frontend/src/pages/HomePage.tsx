import { BuildInPublic } from '@/components/home/BuildInPublic';
import { Hero } from '@/components/home/Hero';
import { ProjectsSection } from '@/components/home/ProjectsSection';
import { Sponsors } from '@/components/home/Sponsors';

export function HomePage() {
  return (
    <main>
      <Hero />
      <ProjectsSection />
      <BuildInPublic />
      <Sponsors />
    </main>
  );
}
