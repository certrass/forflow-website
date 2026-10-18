import {useEffect, useRef, useState} from 'react';

// Discrete product states: CSS owns movement, React only advances at each hold.
// Preserve the remaining hold when a card leaves view or the tab is hidden.
export function useAmbientSequence(root, durations, enabled) {
  const [phase, setPhase] = useState(0);
  const [visible, setVisible] = useState(false);
  const [pageVisible, setPageVisible] = useState(!document.hidden);
  const [reduced, setReduced] = useState(() => matchMedia('(prefers-reduced-motion: reduce)').matches);
  const remaining = useRef(durations[0]);
  const selection = useRef(0);
  const running = enabled && visible && pageVisible && !reduced;
  useEffect(() => {
    const media = matchMedia('(prefers-reduced-motion: reduce)');
    const motion = () => setReduced(media.matches);
    const visibility = () => setPageVisible(!document.hidden);
    const observer = new IntersectionObserver(([entry]) => setVisible(entry.isIntersecting && entry.intersectionRatio >= .35), {threshold:[0,.35]});
    if (root.current) observer.observe(root.current);
    media.addEventListener('change', motion);
    document.addEventListener('visibilitychange', visibility);
    return () => {observer.disconnect();media.removeEventListener('change', motion);document.removeEventListener('visibilitychange', visibility);};
  }, [root]);
  useEffect(() => {
    if (reduced) {remaining.current = durations.at(-1);setPhase(durations.length - 1);}
  }, [reduced, durations]);
  useEffect(() => {
    if (!running) return;
    const started = performance.now();
    const currentSelection = selection.current;
    let advanced = false;
    const timer = setTimeout(() => {
      advanced = true;
      const next = (phase + 1) % durations.length;
      remaining.current = durations[next];
      setPhase(next);
    }, remaining.current);
    return () => {clearTimeout(timer);if (!advanced && selection.current === currentSelection) remaining.current = Math.max(0, remaining.current - (performance.now() - started));};
  }, [phase, running, durations]);
  const select = next => {selection.current += 1;remaining.current = durations[next];setPhase(next);};
  return {phase, running, reduced, select};
}
