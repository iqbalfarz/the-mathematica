// Mirrors manim_scenes/style.py and design/H_visual_design_system.md.
export const C = {
  bg: '#0E0D0B',
  paper: '#EDE6D6',
  muted: '#8A857C',
  brass: '#C8A04A',
  signal: '#FF9E38',
  correct: '#4CD97B',
  reject: '#F2403A',
  unknown: '#F5B942',
};

export const FONT_SANS = '"IBM Plex Sans", Inter, "DejaVu Sans", Arial, sans-serif';
export const FONT_MONO = '"IBM Plex Mono", "JetBrains Mono", "DejaVu Sans Mono", monospace';

// All sizes are fractions of the frame height, so every profile looks identical.
export const vh = (height: number, frac: number) => Math.round(height * frac);
