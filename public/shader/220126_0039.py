/*vec2 mainSound(float time) {
  float pi = acos(-1.0);
  float pi2 = pi * 2.0;
  
  float tempo = abs(sin(time));
  
  float wave44 = sin(pi2 * 440.0 * time);
  //float env44 = wave44 * mod(-time * 0.5, 0.25);
  
  float env44 = wave44 * step(0.1, step(0.9,fract(-1.0 * time)));
  
  float wave88 = sin(pi2 * 880.0 * time);
  float env88 = wave88 * fract(time / -4.0);
  
  return vec2(env44, env88);
}*/

const float BPM = 90.0;

float timeToBeat(float time) {
  return time / 60.0 * BPM;
}

float sine(float freq, float time) {
  return sin(freq * 6.28318530718 * time);
}

// Shadertoyと同じmainSound関数
vec2 mainSound(float time) {
  float beat = timeToBeat(time);
  float freq = mod(beat, 4.0) >= 1.0 ? 440.0 : 880.0;
  float amp = exp(-6.0 * fract(beat));
  return vec2(sine(freq, time) * amp);
}
