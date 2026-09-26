import {useVideoConfig} from 'remotion';
import {C, FONT_MONO, FONT_SANS, vh} from '../theme';
import type {SceneEntry} from '../types';
import {useSec} from './common';

/** Shown when a scene has not been rendered yet: an animatic card with the storyboard text. */
export const Slate: React.FC<{scene: SceneEntry}> = ({scene}) => {
  const t = useSec();
  const {height} = useVideoConfig();
  let i = 0;
  scene.beats.forEach((b, k) => {
    if (t >= b.start) i = k;
  });
  return (
    <div style={{position: 'absolute', inset: 0, background: '#15130F', color: C.paper, fontFamily: FONT_SANS,
      padding: vh(height, 0.08)}}>
      <div style={{fontFamily: FONT_MONO, color: C.unknown, fontSize: vh(height, 0.022)}}>
        NOT RENDERED YET · {scene.id} · {scene.tool.toUpperCase()}
      </div>
      <div style={{fontSize: vh(height, 0.05), marginTop: vh(height, 0.02)}}>{scene.title}</div>
      <div style={{fontSize: vh(height, 0.03), marginTop: vh(height, 0.05), color: C.muted, maxWidth: '75%'}}>
        {scene.visuals[i]}
      </div>
    </div>
  );
};
