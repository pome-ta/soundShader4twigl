#define BPM 128.0
const float PI = acos(-1.0);
const float TAU = PI * 2.0;




/* GLSL */
// 2D Random
float _rnd(in vec2 st) {
  return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453123);
}


/* sound common */
float timeToBeat(float t) {return t / 60.0 * BPM;}
float beatToTime(float b) {return b / BPM * 60.0;}


float saw(float phase) {return 2.0 * fract(phase) - 1.0;}
float square(float phase) {return fract(phase) < 0.5 ? -1.0 : 1.0;}
float triangle(float phase) {return 1.0 - 4.0 * abs(fract(phase) - 0.5);}
float sine(float phase) {return sin(TAU * phase );}


float random(float t) {
  float rnd_x = sine(123.4 * t);
  float rnd_y = sine(567.8 * t);
  return _rnd(vec2(rnd_x, rnd_y)) - 0.5;
}



float kick(float time) {
  float amp = exp(-24.0 * time);
  float phase = 48.0 * time - 4.8 * exp(-48.0 * time);
  return amp * sine( phase );
}



float hihat(float time) {
  float amp = exp(-48.0 * time);
  return amp * random(time * 1e6);
}


vec2 mainSound(float time) {
  float beat = timeToBeat(time);
  float tempo = sine((mod(beat, 4.0) >= 1.0 ? 440.0 : 880.0) * time) * exp(-1e2 * fract(beat));
  
  float kikTiming = mod(beat, 16.0) <= 15.0 ? mod(beat, 1.0) : mod(beat, 0.5);
  float kickTime = beatToTime(kikTiming);
  
  float bd = kick(kickTime);
  
  float hihTiming = mod(beat - 0.5, 1.0);
  float hihatTime = beatToTime(hihTiming);
  
  float hh = hihat(hihatTime);
  
  
  float a2 = 110.0;
  float a3 = 220.0;
  
  float w = sine(a3 * time);
  
  vec2 st = gl_FragCoord.xy;
  
  float wn1 = fract(sin(beat * 1e4) * 1e6) - 0.5;
  float wn2 = fract(sin(beat * 1e3) * 1e6) - 0.5;
  
  
  //float rnd = random(st);
  float nnn = random(time);
  
  
  //return vec2(tempo, bd);
  //return vec2(bd+ wav);
  //return vec2(clamp(nnn, -1.0, 1.0));
  //return vec2(bd, tempo);
  return vec2(bd + hh);
  //return vec2(fract(sin(time*1e3)*1e6)-.5);
}
