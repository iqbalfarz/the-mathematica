import {interpolate, useVideoConfig} from 'remotion';
import {C, FONT_MONO, vh} from '../theme';
import type {SceneEntry} from '../types';
import {StageCaption, TrackedLabels} from './Labels';
import {fade, useSec} from './common';

// Mirrors blender/lib/api.py: rotors move between STEP_START and STEP_END of a press.
const STEP_START = 0.03;
const STEP_END = 0.1;

/** The three window letters, from the event stream. Each press flips them while the
 * rotors are being pushed; the letters that changed glow brass for a moment. */
const WindowReadout: React.FC<{scene: SceneEntry}> = ({scene}) => {
  const t = useSec();
  const {height} = useVideoConfig();
  const presses = scene.events?.presses ?? [];
  if (!presses.length) return null;
  const slow = scene.slow ?? 1;
  let shown = presses[0].positions_before;
  let prev = shown;
  let tFlip = -99;
  let tStart = -99;
  presses.forEach((p, i) => {
    const t0 = scene.press_times[i] + STEP_START * slow;
    const t1 = scene.press_times[i] + STEP_END * slow;
    if (t >= t0) {
      prev = p.positions_before;
      tStart = t0;
      tFlip = t1;
      shown = p.positions_after;
    }
  });
  const box = vh(height, 0.075);
  return (
    <div style={{position: 'absolute', right: vh(height, 0.06), top: vh(height, 0.06), opacity: fade(t, 0.3, 0.5),
      fontFamily: FONT_MONO, textAlign: 'center'}}>
      <div style={{color: C.muted, fontSize: vh(height, 0.018), letterSpacing: '0.25em', marginBottom: vh(height, 0.01)}}>
        WINDOWS
      </div>
      <div style={{display: 'flex', gap: vh(height, 0.012)}}>
        {shown.split('').map((ch, i) => {
          const changed = ch !== prev[i];
          // while the pawl pushes, the old letter slides up and the new one follows
          const k = changed ? interpolate(t, [tStart, tFlip], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 1;
          const glow = changed ? 1 - interpolate(t, [tFlip, tFlip + 2.5], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 0;
          return (
            <div key={i} style={{width: box, height: box, position: 'relative', overflow: 'hidden',
              background: 'rgba(14,13,11,0.8)', border: `2px solid ${glow > 0.01 ? C.brass : C.muted}`,
              boxShadow: glow > 0.01 ? `0 0 ${vh(height, 0.03) * glow}px ${C.brass}` : 'none'}}>
              {changed ? (
                <div style={{position: 'absolute', left: 0, right: 0, top: -k * box, lineHeight: `${box}px`,
                  fontSize: vh(height, 0.05), color: C.paper}}>{prev[i]}</div>
              ) : null}
              <div style={{position: 'absolute', left: 0, right: 0, top: (1 - k) * box, lineHeight: `${box}px`,
                fontSize: vh(height, 0.05), color: glow > 0.01 ? C.brass : C.paper}}>{ch}</div>
            </div>
          );
        })}
      </div>
      <div style={{color: C.muted, fontSize: vh(height, 0.016), letterSpacing: '0.2em', marginTop: vh(height, 0.008),
        display: 'flex', justifyContent: 'space-between'}}>
        <span>L</span><span>M</span><span>R</span>
      </div>
    </div>
  );
};

/** s0601-s0603: part labels, the window readout and the slow-motion tag. */
export const S06Overlay: React.FC<{scene: SceneEntry}> = ({scene}) => (
  <>
    {scene.labels ? <TrackedLabels data={scene.labels} /> : null}
    <WindowReadout scene={scene} />
    <StageCaption scene={scene} prefix="" />
  </>
);
