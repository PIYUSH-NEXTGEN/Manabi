import { Outlet } from 'react-router-dom';
import { Nav } from './Nav';
import { Footer } from './Footer';
import { ChatWidget } from '@/components/chat/ChatWidget';

export function AppLayout() {
  return (
    <div className="flex min-h-screen flex-col bg-paper text-ink">
      <a
        href="#content"
        className="sr-only focus:not-sr-only focus:absolute focus:left-2 focus:top-2 focus:z-50 focus:border-[3px] focus:border-ink focus:bg-yellow focus:px-3 focus:py-2 focus:font-mono focus:text-xs focus:font-bold focus:uppercase focus:tracking-widest"
      >
        Skip to content
      </a>
      <Nav />
      <div className="flex-1" id="content">
        <Outlet />
      </div>
      <Footer />
      <ChatWidget />
    </div>
  );
}
