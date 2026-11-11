import { Outlet } from 'react-router-dom';
import { MotionConfig } from 'motion/react';
import { Nav } from './Nav';
import { Footer } from './Footer';
import { ChatWidget } from '@/components/chat/ChatWidget';

export function AppLayout() {
  return (
    <MotionConfig reducedMotion="user">
      <div className="flex min-h-screen flex-col bg-paper text-ink">
        <a
          href="#content"
          className="sr-only focus:not-sr-only focus:absolute focus:left-2 focus:top-2 focus:z-50 focus:border focus:border-ink focus:bg-accent focus:px-3 focus:py-2 focus:text-paper focus:font-mono focus:text-label focus:font-bold focus:uppercase focus:tracking-widest"
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
    </MotionConfig>
  );
}
