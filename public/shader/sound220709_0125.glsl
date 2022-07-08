// memo: ワンショット

#define BPM 60.0
const float PI = acos(-1.0);
const float TAU = PI * 2.0;

/* sound common */
float timeToBeat(float t) {return t / 60.0 * BPM;}
float beatToTime(float b) {return b / BPM * 60.0;}

float sine(float phase) {
  return sin(TAU * phase);
}


float rand(vec2 st) {
  vec2 magic2 = vec2(12.9898, 78.233);
  float _rnd = sin(dot(st, magic2));
  return fract(_rnd * 43758.5453123);
}

float calcHertz(float scale) {
  return 440.0 * pow(2.0, scale / 12.0);
}

float bassDrum(float beat) {
  float t = mod(beat / 2.0, 1.0);// 3.0 * 8.0;
  float bd = sin(beatToTime(beat) * calcHertz(-4.0));
  return bd * max(0.0, 1.0 - fract(t) * 8.0);
}


float snereDrum(float beat) {
  float t = mod(beat / 2.0, 4.0) / 4.0 * 8.0;
  float sd = rand(vec2(beatToTime(beat) * 64.0, 0.0));
  return sd * max(0.0, 1.0 - t * 8.0);
}

float rect(float beat) {
  if (fract(beat / PI / 2.0) < 0.5) {
    return 1.0;  
  } else {
    return 0.0;
  }
}
float square(float phase) {
  return fract(phase) < 0.5 ? -1.0 : 1.0;
}
float triangle(float phase) {
  return 1.0 - 4.0 * abs(fract(phase) - 0.5);
}
float pulse(float phase, float duty) {
  return fract(phase) < abs(duty) ? -1.0 : 1.0;
}

vec2 mainSound(float time) {
  float bpm = timeToBeat(time);
  
  
  // float sound = 0.0;
  float freq = calcHertz(0.0);
  float fm = 0.07 * sine(time * freq * 7.0);
  // sound += triangle(time * freq + fm);
  float vib = fm * sine(time * 4.0);
  // float sound = triangle(time * freq + vib) * exp(- 2.0 * time);
  // float sound = triangle(time * freq + vib) * fract(-time / 4.0);
  // float sound = triangle(time * freq + vib) * fract(-time / 4.0) * exp(-time * 4.0);

  float sound = triangle(time * freq + vib) * exp(-time * 0.5) * fract(-time / 4.0);





  // sound += bassDrum(bpm) * 0.65;
  // sound += snereDrum(bpm) * 0.8;
  // sound += sine(calcHertz(0.0) * bpm);


  // if (abs(sound) > 1.0) sound /= abs(sound);
  // sound *= 0.8;
  
  return vec2(sound);
}

