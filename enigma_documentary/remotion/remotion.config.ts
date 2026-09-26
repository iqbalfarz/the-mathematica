import {Config} from '@remotion/cli/config';

// Local rendering only. PNG sequences from Blender are read straight from public/media.
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(95);
Config.setOverwriteOutput(true);
Config.setPixelFormat('yuv420p');
Config.setCodec('h264');
