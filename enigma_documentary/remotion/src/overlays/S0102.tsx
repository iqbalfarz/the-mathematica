import {useVideoConfig} from 'remotion';
import {C, FONT_MONO, FONT_SANS, vh} from '../theme';
import type {SceneEntry} from '../types';
import {beatStart, fade, useSec} from './common';

export const S0102Overlay: React.FC<{scene: SceneEntry}> = ({scene}) => {
  const t = useSec();
  const {height} = useVideoConfig();
  const b2 = beatStart(scene, 'b2');
  const b3 = beatStart(scene, 'b3');
  const b4 = beatStart(scene, 'b4');
  return (
    <>
      <div style={{position: 'absolute', left: 0, right: 0, bottom: vh(height, 0.12), textAlign: 'center',
        fontFamily: FONT_MONO, color: C.paper, fontSize: vh(height, 0.03), letterSpacing: '0.25em',
        opacity: fade(t, b2 + 0.4, 0.4, b3 - 0.4)}}>
        26 KEYS · 26 LAMPS
      </div>
      <div style={{position: 'absolute', inset: 0, opacity: 0.85 * fade(t, b3, 0.6, b4 - 0.2),
        background: 'radial-gradient(ellipse at center, rgba(8,7,6,0.92) 0%, rgba(8,7,6,0.75) 45%, rgba(8,7,6,0.2) 100%)'}} />
      <div style={{position: 'absolute', left: '10%', right: '10%', top: '38%', textAlign: 'center',
        fontFamily: FONT_SANS, fontWeight: 600, color: C.paper, fontSize: vh(height, 0.06), lineHeight: 1.2,
        textShadow: '0 0 30px rgba(0,0,0,0.9)', opacity: fade(t, b3 + 0.2, 0.6, b4 - 0.2)}}>
        HOW CAN THE SAME KEY<br />HAVE A DIFFERENT ANSWER?
      </div>
    </>
  );
};
