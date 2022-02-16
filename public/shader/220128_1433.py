/* BDサウンドテスト */

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
  
  
  float kick_sound1 = sine(88., time);
  float kick_sound2 = sine(44.0, time);
  //float kicks = mix(kick_sound2, kick_sound1, 0.5);
  float kicks = kick_sound1 + kick_sound2;
  
  /*
  float kik1 = sine(44.0, time) * pow(fract(-beat), 8.0);
  float kik2 = sine(64.0, time) * smoothstep(0.7, 1.0, fract(-beat));
  float kicks = mix(kik1, kik2, 0.8);
  */
  
  
  
  float loop = mod(beat, 8.0) < 7.5 || mod(beat, 8.0) > 8.0 ? 1.0:0.5;
  float kick_env = fract(-beat / loop);
  float kick = kicks * kick_env;
  
  return vec2(tempo, kick);
}
