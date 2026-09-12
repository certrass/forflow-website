import {useLayoutEffect, useState} from 'react';

// Track real element geometry, including fitted and expanded product canvases.
export function useFilmPointer(root, selector, revision) {
  const [position, setPosition] = useState({x:0,y:0});
  useLayoutEffect(() => {
    const measure = () => {
      const stage = root.current?.querySelector('.story-stage');
      const target = stage?.querySelector(selector);
      if (!stage || !target) return;
      const canvas = stage.getBoundingClientRect();
      const bounds = target.getBoundingClientRect();
      const scale = canvas.width / stage.offsetWidth;
      if (!scale || !bounds.width) return;
      setPosition({x:(bounds.left+bounds.width/2-canvas.left)/scale,y:(bounds.top+bounds.height/2-canvas.top)/scale});
    };
    measure();
    const stage = root.current?.querySelector('.story-stage');
    stage?.addEventListener('scroll',measure,true);
    const observer = new ResizeObserver(measure);
    if (root.current) observer.observe(root.current);
    return () => { observer.disconnect(); stage?.removeEventListener('scroll',measure,true); };
  }, [root, selector, revision]);
  return position;
}
