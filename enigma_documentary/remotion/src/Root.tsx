import {Composition, staticFile} from 'remotion';
import {Film} from './Film';
import type {Timeline} from './types';

const FALLBACK: Timeline = {
  profile: 'none', fps: 24, width: 1920, height: 1080, duration: 5, crf: 20, has_sfx: false, scenes: [],
};

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="EnigmaFilm"
      component={Film}
      defaultProps={{timeline: FALLBACK}}
      fps={24}
      width={1920}
      height={1080}
      durationInFrames={120}
      calculateMetadata={async () => {
        // Written by `python -m enigma_doc.stage` (make stage).
        const res = await fetch(staticFile('timeline.json'));
        const timeline = (await res.json()) as Timeline;
        const frames = timeline.scenes.reduce((n, s) => n + s.frames, 0);
        return {
          props: {timeline},
          fps: timeline.fps,
          width: timeline.width,
          height: timeline.height,
          durationInFrames: Math.max(1, frames),
        };
      }}
    />
  );
};
