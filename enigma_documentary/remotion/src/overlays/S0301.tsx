import type {SceneEntry} from '../types';
import {TrackedLabels} from './Labels';

export const S0301Overlay: React.FC<{scene: SceneEntry}> = ({scene}) =>
  scene.labels ? <TrackedLabels data={scene.labels} /> : null;
