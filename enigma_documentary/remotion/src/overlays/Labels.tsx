import {useCurrentFrame, useVideoConfig} from 'remotion';
import {C, FONT_MONO, FONT_SANS, vh} from '../theme';
import type {LabelData, SceneEntry} from '../types';
import {fade} from './common';

/** Draws labels that follow 3D parts, using tracks projected in Blender (blender/lib/labels.py). */
export const TrackedLabels: React.FC<{data: LabelData}> = ({data}) => {
  const frame = useCurrentFrame();
  const {width, height, fps} = useVideoConfig();
  const t = frame / fps;
  // Blender frame f (1-based) shows time (f-1)/fps; Remotion frame n shows n/fps.
  const bf = frame + 1;
  return (
    <>
      {data.labels.map((l, i) => {
        const p = l.track[bf - l.frame0];
        if (!p || t < l.t0 || t > l.t1 + 0.4) return null;
        const o = fade(t, l.t0, 0.35, l.t1);
        const x = p[0] * width;
        const y = p[1] * height;
        const lift = vh(height, 0.07);
        return (
          <div key={i} style={{position: 'absolute', left: 0, top: 0, width, height, opacity: o, pointerEvents: 'none'}}>
            <svg width={width} height={height} style={{position: 'absolute', left: 0, top: 0}}>
              <circle cx={x} cy={y} r={vh(height, 0.005)} fill={C.signal} />
              <line x1={x} y1={y} x2={x} y2={y - lift} stroke={C.paper} strokeWidth={Math.max(1, height / 700)} strokeOpacity={0.8} />
            </svg>
            <div style={{position: 'absolute', left: x, top: y - lift - vh(height, 0.045), transform: 'translateX(-50%)',
              fontFamily: FONT_SANS, fontWeight: 600, letterSpacing: '0.14em', fontSize: vh(height, 0.026), color: C.paper,
              background: 'rgba(14,13,11,0.72)', padding: `${vh(height, 0.006)}px ${vh(height, 0.012)}px`,
              borderRadius: vh(height, 0.004), whiteSpace: 'nowrap'}}>
              {l.text}
            </div>
          </div>
        );
      })}
    </>
  );
};

/** Lower-third caption that switches as the current reaches each part. */
export const StageCaption: React.FC<{scene: SceneEntry; prefix?: string; top?: boolean}> = ({
  scene,
  prefix = 'CURRENT IN',
  top = false,
}) => {
  const frame = useCurrentFrame();
  const {height, fps} = useVideoConfig();
  const t = frame / fps;
  const caps = scene.labels?.captions ?? [];
  let cur = -1;
  caps.forEach((c, i) => {
    if (t >= c.t) cur = i;
  });
  if (cur < 0) return null;
  const last = caps[caps.length - 1];
  const o = fade(t, caps[0].t, 0.3, last.t + 3.0);
  const c = caps[cur];
  return (
    <div style={{position: 'absolute', left: vh(height, 0.06), ...(top ? {top: vh(height, 0.07)} : {bottom: vh(height, 0.08)}), opacity: o,
      fontFamily: FONT_MONO, fontSize: vh(height, 0.034), color: C.paper, background: 'rgba(14,13,11,0.75)',
      padding: `${vh(height, 0.012)}px ${vh(height, 0.022)}px`, borderLeft: `${vh(height, 0.006)}px solid ${C.signal}`}}>
      <span style={{color: C.muted, fontSize: vh(height, 0.02), letterSpacing: '0.2em'}}>{prefix}&nbsp;&nbsp;</span>
      {c.text}
    </div>
  );
};
