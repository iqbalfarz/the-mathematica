import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {ActCard} from './overlays/ActCard';
import {Slate} from './overlays/Slate';
import {OVERLAYS} from './overlays';
import type {SceneEntry} from './types';

const FrameSequence: React.FC<{dir: string; pad: number}> = ({dir, pad}) => {
  const frame = useCurrentFrame();
  const n = String(frame + 1).padStart(pad, '0');
  return <Img src={staticFile(`${dir}/frame_${n}.png`)} style={{width: '100%', height: '100%'}} />;
};

export const SceneView: React.FC<{scene: SceneEntry; hasSfx: boolean}> = ({scene, hasSfx}) => {
  const {fps} = useVideoConfig();
  const Overlay = OVERLAYS[scene.id];
  const m = scene.media;
  return (
    <AbsoluteFill>
      {m === null ? (
        <Slate scene={scene} />
      ) : m.type === 'frames' ? (
        <FrameSequence dir={m.dir} pad={m.pad} />
      ) : (
        <OffthreadVideo src={staticFile(m.src)} muted />
      )}
      {Overlay ? <Overlay scene={scene} /> : null}
      <ActCard scene={scene} />
      {scene.beats.map((b) =>
        b.wav ? (
          <Sequence key={b.id} from={Math.round(b.start * fps)} name={`voice ${b.id}`}>
            <Audio src={staticFile(`media/${b.wav}`)} />
          </Sequence>
        ) : null,
      )}
      {hasSfx &&
        scene.sfx.map((c, i) => (
          <Sequence key={`sfx-${i}`} from={Math.round(c.t * fps)} name={`sfx ${c.sfx}`}>
            <Audio src={staticFile(`media/sfx/${c.sfx}.wav`)} volume={c.sfx === 'hum' ? 0.5 : 0.8} />
          </Sequence>
        ))}
    </AbsoluteFill>
  );
};
