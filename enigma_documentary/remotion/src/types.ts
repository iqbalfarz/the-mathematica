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
  press_times: number[];
  sfx: {t: number; sfx: string}[];
  visuals: string[];
  media: null | {type: 'frames'; dir: string; pad: number} | {type: 'video'; src: string};
  events?: {presses: Press[]} | null;
};

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
