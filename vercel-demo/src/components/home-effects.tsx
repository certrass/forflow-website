"use client";

import { useEffect } from "react";

export function HomeEffects() {
  useEffect(() => {
    const root = document.querySelector<HTMLElement>(".ff-home-v4");
    if (!root) return;

    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const revealItems = Array.from(root.querySelectorAll<HTMLElement>("[data-reveal]"));

    if (reducedMotion || !("IntersectionObserver" in window)) {
      revealItems.forEach((item) => item.classList.add("is-visible"));
      return;
    }

    revealItems.forEach((item, index) => {
      item.style.setProperty("--reveal-delay", `${Math.min(index % 6, 5) * 70}ms`);
    });

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -12% 0px", threshold: 0.12 },
    );

    revealItems.forEach((item) => observer.observe(item));

    const heroPhoto = root.querySelector<HTMLElement>(".ff-hero-photo");
    const onPointerMove = (event: PointerEvent) => {
      if (!heroPhoto) return;
      const rect = heroPhoto.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width - 0.5;
      const y = (event.clientY - rect.top) / rect.height - 0.5;
      heroPhoto.style.setProperty("--hero-tilt-x", `${y * -4}deg`);
      heroPhoto.style.setProperty("--hero-tilt-y", `${x * 4}deg`);
    };
    const resetTilt = () => {
      heroPhoto?.style.setProperty("--hero-tilt-x", "0deg");
      heroPhoto?.style.setProperty("--hero-tilt-y", "0deg");
    };

    heroPhoto?.addEventListener("pointermove", onPointerMove);
    heroPhoto?.addEventListener("pointerleave", resetTilt);

    return () => {
      observer.disconnect();
      heroPhoto?.removeEventListener("pointermove", onPointerMove);
      heroPhoto?.removeEventListener("pointerleave", resetTilt);
    };
  }, []);

  return null;
}
