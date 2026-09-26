import {useVideoConfig} from 'remotion';
import {C, FONT_SANS, vh} from '../theme';
import type {SceneEntry} from '../types';
import {fade, useSec} from './common';

const ROMAN = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV',
  'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI', 'XXII', 'XXIII', 'XXIV'];

/** Small act label in the top-left for the first seconds of the first scene of each act. */
export const ActCard: React.FC<{scene: SceneEntry}> = ({scene}) => {
  const t = useSec();
  const {height} = useVideoConfig();
  const first = scene.id.endsWith('01');
  if (!first || scene.act === 1) return null;
  const o = fade(t, 0.3, 0.6, 4.0);
  return (
    <div style={{position: 'absolute', left: vh(height, 0.05), top: vh(height, 0.05), opacity: o,
      fontFamily: FONT_SANS, color: C.muted, fontSize: vh(height, 0.022), letterSpacing: '0.2em'}}>
      ACT {ROMAN[scene.act]} · {scene.act_title.toUpperCase()}
    </div>
  );
};
