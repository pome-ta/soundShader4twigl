/* メトロノーム */
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
