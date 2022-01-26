const float BPM = 118.;
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
  
  //float tempo = sine(mod(beat, 4.0) >= 1.0 ? 440.0:880.0, time) * exp(-1e2 * fract(beat));
  
  float whiteNoise = fract(sin(time * 1e3) * 1e6) - 0.5;
  float hih = whiteNoise * smoothstep(0.96, 1.0, fract(-beat * 1.0 + 0.5));
  
  float kik1 = sine(44.0, time) * pow(fract(-beat), 8.0);
  float kik2 = sine(64.0, time) * smoothstep(0.7, 1.0, fract(-beat));
  float kik = mix(kik1, kik2, 0.8);
  
  float sn = (sine(880.0, time) + 1.02 * sine(330.0, time)) * step(0.98, fract(-beat / 2.0 - 0.5));
  
  return vec2(0.64 * ((0.64 * hih) + (1.75 * kik) + (0.5 * sn)));
  
}
