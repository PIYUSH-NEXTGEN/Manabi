import { AskManabi } from '@/components/home/AskManabi';
import { BuildInPublic } from '@/components/home/BuildInPublic';
import { FinalCta } from '@/components/home/FinalCta';
import { Hero } from '@/components/home/Hero';

export function HomePage() {
  return (
    <main>
      <Hero />
      <BuildInPublic />
      <AskManabi />
      <FinalCta />
    </main>
  );
}
