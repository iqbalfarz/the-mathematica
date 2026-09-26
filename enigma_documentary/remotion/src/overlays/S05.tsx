import {useVideoConfig} from 'remotion';
import {C, FONT_MONO, vh} from '../theme';
import type {SceneEntry} from '../types';
import {StageCaption} from './Labels';
import {beatStart, fade, useSec} from './common';

type Hop = {stage: string; in_letter: string; out_letter: string};

/** s0501 / s0502: caption from the shot's labels.json (rotor letters, reflector pairs). */
export const S05CaptionOverlay: React.FC<{scene: SceneEntry}> = ({scene}) => (
  <StageCaption scene={scene} prefix={scene.id === 's0502' ? 'REFLECTOR' : 'CURRENT IN'} top={scene.id === 's0502'} />
);

/** s0503: the whole journey as one chain, built from the event stream, on the last beat. */
export const S0503Overlay: React.FC<{scene: SceneEntry}> = ({scene}) => {
  const t = useSec();
  const {height} = useVideoConfig();
  const press = scene.events?.presses?.[0] as unknown as {path: Hop[]} | undefined;
  const b5 = beatStart(scene, 'b5');
  if (!press) return <StageCaption scene={scene} />;
  const hop = (s: string) => press.path.find((h) => h.stage === s)!;
  const fwd = ['rotor_right_in', 'rotor_middle_in', 'rotor_left_in'].map(hop);
  const back = ['rotor_left_out', 'rotor_middle_out', 'rotor_right_out'].map(hop);
  const letters = [fwd[0].in_letter, ...fwd.map((h) => h.out_letter)];
  const ret = [back[0].in_letter, ...back.map((h) => h.out_letter)];
  const step = 0.35;
  const cell = (ch: string, i: number, color: string) => (
    <span key={i} style={{opacity: fade(t, b5 + 0.4 + i * step, 0.25), color}}>{ch}</span>
  );
  const arrow = (i: number) => (
    <span key={`a${i}`} style={{opacity: fade(t, b5 + 0.4 + i * step, 0.25), color: C.muted}}> → </span>
  );
  const parts: React.ReactElement[] = [];
  letters.forEach((ch, i) => {
    if (i) parts.push(arrow(i));
    parts.push(cell(ch, i, i === 0 ? C.paper : C.signal));
  });
  parts.push(<span key="turn" style={{opacity: fade(t, b5 + 0.4 + 4 * step, 0.25), color: C.brass}}> ⟲ </span>);
  ret.forEach((ch, i) => {
    if (i) parts.push(arrow(5 + i));
    parts.push(cell(ch, 5 + i, i === ret.length - 1 ? C.paper : C.signal));
  });
  return (
    <>
      {t < b5 ? <StageCaption scene={scene} /> : null}
      <div style={{position: 'absolute', left: 0, right: 0, bottom: vh(height, 0.1), textAlign: 'center',
        fontFamily: FONT_MONO, fontSize: vh(height, 0.05), opacity: fade(t, b5 + 0.2, 0.3),
        textShadow: '0 0 20px rgba(0,0,0,0.9)'}}>
        {parts}
      </div>
    </>
  );
};
