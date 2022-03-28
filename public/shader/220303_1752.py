// シェーダー空手のやつ
//# https://thebookofshaders.com/05/kynd.png

#define BPM 90.0
const float PI = acos(-1.0);
const float TAU = PI * 2.0;

/* sound common */
float timeToBeat(float t) {return t / 60.0 * BPM;}
float beatToTime(float b) {return b / BPM * 60.0;}

float sine(float phase) {
  return sin(TAU * phase);
}


float pitch(float scale) {
  return 440.0 * pow(2.0, scale / 12.0);
}



vec2 mainSound(float time) {
  float bpm = timeToBeat(time);
  float tempo = sine((mod(bpm, 4.0) >= 1.0 ? 440.0 : 880.0) * time) * exp(-1e2 * fract(bpm));
  
  float sound = 0.0;
  //#float tone = sin( 6.2831 * 440.0 * time );
  //#float env = fract(-bpm);
  float f = fract(bpm);
  float s = sin(PI * bpm / 2.0);
  
  float tone = 0.0;
  float env = 0.0;
  
  //tone = sine(beatToTime(bpm) * pitch(0.0));
  tone = sine(beatToTime(bpm) * 64.0);
  
  
  env = 1.0 - pow(abs(s), 0.5);
  //env = 1.0 - pow(abs(s), 1.0);
  //env = 1.0 - pow(abs(s), 3.5);
  
  //env = pow(cos(PI * s / 2.0), 0.5);
  //env = pow(cos(PI * s / 2.0), 1.0);
  //env = pow(cos(PI * s / 2.0), 3.5);
  
  //env = 1.0 - pow(abs(sin(PI * s / 2.0)), 0.5);
  //env = 1.0 - pow(abs(sin(PI * s / 2.0)), 1.0);
  //env = 1.0 - pow(abs(sin(PI * s / 2.0)), 3.5);
  
  //env = pow(min(cos(PI * s / 2.0), 1.0 - abs(s)), 0.5);
  //env = pow(min(cos(PI * s / 2.0), 1.0 - abs(s)), 1.0);
  //env = pow(min(cos(PI * s / 2.0), 1.0 - abs(s)), 3.5);
  
  //env = 1.0 - pow(max(0.0, abs(s) * 2.0 - 1.0), 0.5);
  //env = 1.0 - pow(max(0.0, abs(s) * 2.0 - 1.0), 1.0);
  //env = 1.0 - pow(max(0.0, abs(s) * 2.0 - 1.0), 3.5);
  
  
  float w = smoothstep(1.0, -1.0, tan(bpm * PI));
  env = sin(w * TAU);
  
  sound += tone * env;
  sound += tempo;
  
  
  //#if (abs(sound) > 1.0) sound /= abs(sound);
  return vec2(sound);
}


