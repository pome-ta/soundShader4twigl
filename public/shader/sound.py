const float BPM = 140.;
const float PI = acos(-1.0);
const float TAU = PI * 2.0;

float timeToBeat(float time) {
  return time / 60.0 * BPM;
}

float sine(float freq, float time) {
  return sin(freq * TAU * time);
}

vec2 mainSound(float time) {
  float beat = timeToBeat(time);
  
  float tempo = sine(mod(beat, 4.0) >= 1.0 ? 440.0:880.0, time) * exp(-1e2 * fract(beat));
  
  float wave_sound = sine(44., time);
  //float env = distance(fract(-tempo), fract(-beat));
  float env = smoothstep(1.0, 0.0, smoothstep(1.0, 0.5, fract(-beat)));
  
  
  float wave = wave_sound * env;
  
  
  float sound = tempo + wave;
  if (abs(sound) >= 0.3)  sound -= abs(sound);
  return vec2( 0.9 * sound);
}
