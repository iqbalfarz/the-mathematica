import type {SceneEntry} from '../types';
import {S0101Overlay} from './S0101';
import {S0102Overlay} from './S0102';
import {S0301Overlay} from './S0301';
import {S0302Overlay} from './S0302';

// Editorial overlays per scene (typography, labels, title cards). Scenes without
// an entry play their render as-is.
export const OVERLAYS: Record<string, React.FC<{scene: SceneEntry}>> = {
  s0101: S0101Overlay,
  s0102: S0102Overlay,
  s0301: S0301Overlay,
  s0302: S0302Overlay,
};
