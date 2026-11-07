import { useLocation, useNavigationType } from 'react-router-dom';
import { useEffect } from 'react';

/** Scroll to the top of the page on client-side navigation. The initial page
 * load and back/forward navigation are left to the browser's own scroll
 * handling. */
export function ScrollToTop() {
  const location = useLocation();
  const navigationType = useNavigationType();

  useEffect(() => {
    if (navigationType === 'POP') return;
    if (window.scrollY === 0) return;
    window.scrollTo(0, 0);
  }, [location.pathname, navigationType]);

  return null;
}
