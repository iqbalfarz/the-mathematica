import type {SceneEntry} from '../types';
import {StageCaption, TrackedLabels} from './Labels';

/** s0401: labels on the exploded rotor's parts. */
export const S0401Overlay: React.FC<{scene: SceneEntry}> = ({scene}) =>
  scene.labels ? <TrackedLabels data={scene.labels} /> : null;

/** s0402 / s0403: caption naming the wire / step, from the rotor_demo stream. */
export const S04CaptionOverlay: React.FC<{scene: SceneEntry}> = ({scene}) => (
  <StageCaption scene={scene} prefix={scene.id === 's0402' ? 'WIRE' : 'CURRENT'} />
);
