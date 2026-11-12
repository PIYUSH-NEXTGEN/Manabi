import { AskManabi } from '@/components/home/AskManabi';
import { BuildInPublic } from '@/components/home/BuildInPublic';
import { Hero } from '@/components/home/Hero';
import { ProjectsSection } from '@/components/home/ProjectsSection';

export function HomePage() {
  return (
    <main>
      <Hero />
      <ProjectsSection />
      <BuildInPublic />
      <AskManabi />
    </main>
  );
}
