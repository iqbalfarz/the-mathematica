export type Beat = {
  id: string;
  start: number;
  dur: number;
  pause: number;
  text: string;
  sfx: string | null;
  wav: string | null;
};

export type Press = {
  index: number;
  key: string;
  lamp: string;
  positions_before: string;
  positions_after: string;
  double_step: boolean;
};

export type SceneEntry = {
  id: string;
  title: string;
  act: number;
  act_title: string;
  tool: 'blender' | 'manim';
  shot: string | null;
  music: string;
  film_start: number;
  duration: number;
  frames: number;
  beats: Beat[];
  sfx: {t: number; sfx: string}[];
  visuals: string[];
  media: null | {type: 'frames'; dir: string; pad: number} | {type: 'video'; src: string};
  events?: {presses: Press[]} | null;
  labels?: LabelData | null;
  press_times: number[];
  slow?: number;
  linger?: number;
};

export type LabelTrack = {text: string; t0: number; t1: number; frame0: number; track: ([number, number] | null)[]};
export type LabelData = {fps: number; labels: LabelTrack[]; captions: {t: number; text: string; until: number | null}[]};

export type Timeline = {
  profile: string;
  fps: number;
  width: number;
  height: number;
  duration: number;
  crf: number;
  has_sfx: boolean;
  scenes: SceneEntry[];
};
