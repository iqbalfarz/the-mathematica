import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import type {SceneEntry} from '../types';

export const useSec = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return frame / fps;
};

export const beatStart = (scene: SceneEntry, id: string) => scene.beats.find((b) => b.id === id)?.start ?? 0;

/** 0 -> 1 fade over `dur` seconds starting at t0, back to 0 at t1 (if given). */
export const fade = (t: number, t0: number, dur = 0.4, t1?: number) => {
  const a = interpolate(t, [t0, t0 + dur], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  if (t1 === undefined) return a;
  return a * interpolate(t, [t1, t1 + dur], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
};
