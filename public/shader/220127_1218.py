const float BPM = 140.;
const float PI = acos(-1.0);
const float TAU = PI * 2.0;

float timeToBeat(float time) {
  return time / 60.0 * BPM;
}

float sine(float freq, float time) {
  return sin(freq * TAU * time);
}

float tri(float freq, float time) {
  return -abs(1.0 - mod(freq * time * 2.0, 2.0));
}

vec2 mainSound(float time) {
  float beat = timeToBeat(time);
  
  float tempo = sine(mod(beat, 4.0) >= 1.0 ? 440.0:880.0, time) * exp(-1e2 * fract(beat));
  
  float w = sine(440.0, time) * step(0.1,step(fract(-beat), 0.1));
  
  
  float freq = 440.0;
  freq *= pow(1.06 * 1.06, floor(mod(beat, 8.0)));
  
  
  float tri1 = tri(freq, time) * sin(beat * PI);
  float tri2 = tri(freq * 1.5, time) * sin(time * PI);
  
  //return vec2(w,tempo);
  return vec2(tri1, tempo);
  
  
}
