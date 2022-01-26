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
  
  float freq = mod(beat, 4.0) <= 3.0 ? 440.0 : 0.0;
  float amp = exp(-8.0 * fract(beat));
  
  float w44 = sine(440.0, time) * exp(-8.0 * fract(beat));
  
  float w88 = sine(880.0, time) * exp(-1.0 * fract(beat));
  
  //float wave44 = mod(beat, 4.0) <= 3.0 ? w44 : 0.0;
  float wave;
  float preTime = 0.0;
  if (mod(beat, 4.0) <= 3.0) {
    preTime = time;
    wave = w44;
  } else {
    float negTime = time - preTime;
    wave += sine(880.0, negTime) * exp(-1.0 * fract(beat));
  }
  
  
  
  //float wave88 = mod(beat, 4.0) <= 3.0 ? w44 : 0.0;
  
  
  return vec2(wave);
}
