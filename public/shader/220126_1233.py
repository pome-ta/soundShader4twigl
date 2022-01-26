const float BPM = 60.0;
const float PI = acos(-1.0);
const float PI2 = PI * 2.0;

float timeToBeat(float time) {
  return time / 60.0 * BPM;
}

float sine(float freq, float time) {
  return sin(freq * PI2 * time);
}


vec2 mainSound(float time) {
  float beat = timeToBeat(time);
  
  float w44 = sine(440.0, time) * exp(-8.0 * fract(beat));
  
  float wave88 = sine(880.0, time) * smoothstep(0.5, 1.0, fract(time / -4.0 - 0.25));
  
  float wave44 = mod(beat, 4.0) <= 3.0 ? w44 : 0.0;
  
  return vec2(0.4 * (wave44 + wave88));
}
