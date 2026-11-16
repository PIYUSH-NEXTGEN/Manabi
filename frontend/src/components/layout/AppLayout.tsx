import { Outlet, useLocation } from 'react-router-dom';
import { MotionConfig } from 'motion/react';
import { Nav } from './Nav';
import { Footer } from './Footer';
import { ChatWidget } from '@/components/chat/ChatWidget';
import { Mascot } from '@/components/mascot';

export function AppLayout() {
  const { pathname } = useLocation();
  // The homepage hero runs edge to edge behind the navigation.
  const overlayNav = pathname === '/';

  return (
    <MotionConfig reducedMotion="user">
      <div className="flex min-h-screen flex-col bg-paper text-ink">
        <a
          href="#content"
          className="sr-only focus:not-sr-only focus:absolute focus:left-3 focus:top-3 focus:z-50 focus:rounded-full focus:bg-accent focus:px-4 focus:py-2.5 focus:text-[0.875rem] focus:font-semibold focus:text-white focus:shadow-lift"
        >
          Skip to content
        </a>
        <Nav overlay={overlayNav} />
        <div className="flex-1" id="content">
          <Outlet />
        </div>
        <div className="relative">
          <Footer />
          {pathname === '/' ? (
            <div
              aria-hidden
              className="pointer-events-none absolute inset-x-0 top-0 z-10 flex justify-end pr-[4%]"
            >
              <Mascot
                state="working"
                className="pointer-events-auto w-24 -translate-y-full -scale-x-100 sm:w-32 md:w-36"
              />
            </div>
          ) : null}
        </div>
        <ChatWidget />
      </div>
    </MotionConfig>
  );
}
