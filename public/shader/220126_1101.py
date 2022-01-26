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
  
  float w = sin(PI2 * 440.0 * time);
  
  
  float amp = exp(-100.0 * fract(beat));
  
  
  float w44 = sine(440.0, time) * exp(-10.0 * fract(beat));
  float w88 = sine(880.0, time) * exp(-1.0 * fract(beat));
  
  
  float freq = mod(beat, 4.0) <= 3.0 ? w44 : w88;
  
  return vec2(w44);
}
