import {useVideoConfig} from 'remotion';
import {C, FONT_MONO, vh} from '../theme';
import type {SceneEntry} from '../types';
import {beatStart, fade, useSec} from './common';

/** Lower-third strip: L → Y, L → H ... one entry per press, letters from the event stream. */
export const S0101Overlay: React.FC<{scene: SceneEntry}> = ({scene}) => {
  const t = useSec();
  const {height} = useVideoConfig();
  const presses = scene.events?.presses ?? [];
  const show = beatStart(scene, 'b4') + 1.8;
  return (
    <>
    <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: vh(height, 0.3),
      opacity: fade(t, scene.press_times[0] + 0.2, 0.3),
      background: 'linear-gradient(to top, rgba(8,7,6,0.85), rgba(8,7,6,0))'}} />
    <div style={{position: 'absolute', left: 0, right: 0, bottom: vh(height, 0.1), display: 'flex',
      justifyContent: 'center', gap: vh(height, 0.06), fontFamily: FONT_MONO, fontSize: vh(height, 0.05)}}>
      {presses.map((p, i) => {
        const at = Math.max(scene.press_times[i] + 0.3, i === 0 ? 0 : show);
        return (
          <div key={i} style={{opacity: fade(t, at, 0.3), color: C.paper}}>
            {p.key} <span style={{color: C.muted}}>→</span> <span style={{color: C.signal}}>{p.lamp}</span>
          </div>
        );
      })}
    </div>
    </>
  );
};
