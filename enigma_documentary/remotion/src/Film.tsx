import {AbsoluteFill, Audio, Sequence, staticFile, useVideoConfig} from 'remotion';
import {SceneView} from './Scene';
import {C} from './theme';
import type {Timeline} from './types';

// Music beds are quiet and duck further while anyone is speaking.
const MUSIC_VOL = 0.22;
const MUSIC_DUCKED = 0.08;

export const Film: React.FC<{timeline: Timeline}> = ({timeline}) => {
  const {fps} = useVideoConfig();
  let at = 0;
  const placed = timeline.scenes.map((s) => {
    const from = at;
    at += s.frames;
    return {s, from};
  });

  // Group consecutive scenes of the same act into one music bed.
  const acts: {act: number; music: string; from: number; frames: number; speech: [number, number][]}[] = [];
  for (const {s, from} of placed) {
    const last = acts[acts.length - 1];
    const speech = s.beats.map((b) => [from + b.start * fps, from + (b.start + b.dur) * fps] as [number, number]);
    if (last && last.act === s.act) {
      last.frames += s.frames;
      last.speech.push(...speech);
    } else {
      acts.push({act: s.act, music: s.music, from, frames: s.frames, speech});
    }
  }

  return (
    <AbsoluteFill style={{backgroundColor: C.bg}}>
      {placed.map(({s, from}) => (
        <Sequence key={s.id} from={from} durationInFrames={s.frames} name={`${s.id} ${s.title}`}>
          <SceneView scene={s} hasSfx={timeline.has_sfx} />
        </Sequence>
      ))}
      {timeline.has_sfx &&
        acts.map((a) => (
          <Sequence key={`music-${a.act}`} from={a.from} durationInFrames={a.frames} name={`music act ${a.act}`}>
            <Audio
              src={staticFile(`media/sfx/music_${a.music}.wav`)}
              loop
              volume={(f) => {
                const g = a.from + f;
                const speaking = a.speech.some(([x, y]) => g >= x - 6 && g <= y + 6);
                const fadeIn = Math.min(1, f / (fps * 2));
                const fadeOut = Math.min(1, (a.frames - f) / (fps * 2));
                return (speaking ? MUSIC_DUCKED : MUSIC_VOL) * Math.min(fadeIn, fadeOut);
              }}
            />
          </Sequence>
        ))}
    </AbsoluteFill>
  );
};
