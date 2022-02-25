#define BPM 4.0
const float PI = acos(-1.0);
const float TAU = PI * 2.0;

/* sound common */
float timeToBeat(float t) {return t / 60.0 * BPM;}
float beatToTime(float b) {return b / BPM * 60.0;}

float sine(float phase) {
  return sin(TAU * phase);
}

float rand(vec2 co) {
  vec2 magic2 = vec2(12.9898, 78.233);
  float _rnd = sin(dot(co, magic2));
  return fract(_rnd * 43758.5453);
}

float calcHertz(float scale) {
  return 440.0 * pow(2.0, scale / 12.0);
}

float bassDrum(float time) {
  float t = mod(time, 1.0) / 3.0 * 8.0;
  //return sin(time * (440.0)) * max(0.0, 1.0 - fract(t) * 8.0);
  return tan(time * (4400.0)) * max(0.0, 1.0 - fract(t) * 16.0);
}

float snereDrum(float time) {
  float t = mod(time + 0.5, 1.0);
  return rand(vec2(time * 32.0, 0.0)) * max(0.0, 1.0 - t * 4.0);
}

float hiHat(float time) {
  float t = time * 16.0;
  if (mod(t, 16.0) > 3.0 && mod(t, 2.0) > 1.0) {
    return 0.0;
  }
  return rand(vec2(time * 32.0, 0.0)) * max(0.0, 1.0 - fract(t) * 4.0);
}


float rect(float time) {
  if (fract(time / PI / 2.0) < 0.5) {
    return 1.0;  
  } else {
    return 0.0;
  }
}

float strings(float time) {
  float t = mod(time * 4.0, 1.0);
  float sound = 0.0;
  if (mod(time, 8.0) < 4.0) {
    sound += rect(time * calcHertz(24.0));
    sound += rect(time * calcHertz(28.0));
    sound += rect(time * calcHertz(31.0));
    sound += rect(time * calcHertz(35.0));
  } else {
    sound += rect(time * calcHertz(23.0));
    sound += rect(time * calcHertz(26.0));
    sound += rect(time * calcHertz(30.0));
    sound += rect(time * calcHertz(33.0));
  }
  return sound * max(0.0, (1.0 - t * 2.0));
}

float bass(float time) {
  time = mod(time, 8.0);
  if (time < 2.0) {
    return rect(time * calcHertz(0.0));
  }
  if (time > 3.0 && time < 3.5) {
    return rect(time * calcHertz(0.0));
  }
  if (time < 4.0) {
    return rect(time * calcHertz(12.0));
  }
  if (time < 6.0) {
    return rect(time * calcHertz(11.0));
  }
  if (time < 8.0) {
    return rect(time * calcHertz(-1.0));
  }
  return 0.0;
}

vec2 mainSound(float time) {
  float bpm = timeToBeat(time);
  float tempo = sine((mod(bpm, 4.0) >= 1.0 ? 440.0 : 880.0) * time) * exp(-1e2 * fract(bpm));
  
  float sound = 0.0;
  sound += bassDrum(bpm) * 0.5;
  sound += snereDrum(bpm) * 0.5;
  sound += hiHat(bpm) * 0.5;
  sound += strings(bpm) * 0.2;
  sound += bass(bpm) * 0.2;
  sound += tempo;
  
  if (abs(sound) > 1.0) sound /= abs(sound);
  return vec2(sound);
}
