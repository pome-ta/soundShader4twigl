#define BPM 140.0
const float PI = acos(-1.0);
const float TAU = PI * 2.0;



/* sound common */
float timeToBeat(float t) {return t / 60.0 * BPM;}
float beatToTime(float b) {return b / BPM * 60.0;}

float sine(float phase) {
  return sin(TAU * phase);
}

// https://raku-phys.hatenablog.com/entry/2020/04/19/002400

float fm(float time){
  return sin(1e3 * time + sin(300.0 * time));
}
float rhy(float time, float f){
  return pow(fract(mod(-time * 8.0, 8.0) / 3.0), 6.0 - 3.0 * f);
}
vec2 dfm(float tone, float time, float dt){
  return exp(-3.0 * dt) * fm(8.0 * tone) *
    vec2(rhy(time - 0.3 * dt, dt),
         rhy(time - 0.5 * dt, dt));
}


vec2 mainSound(float time){
  float beat = timeToBeat(time);
  float tempo = sine((mod(beat, 4.0) >= 1.0 ? 440.0 : 880.0) * time) * exp(-1e2 * fract(beat));
  
  vec2 t2 = vec2(tempo);
  
  vec2 s;
  // bd
  s += vec2(3.0 * sin(3e2 * time) * pow(fract(-beat), 4.0));
  
  // hh
  s += vec2(0.5 * sin(4e5 * time) * fract(-beat + 0.5));
  //s += vec2(0.5 * sin(4e5 * time));
  // * fract(-time * 2.0 + 0.5));
  
  s += dfm(time, beat / 2.0, 0.0);
  s += dfm(time, beat / 2.0, 0.5);
  s += dfm(time, beat / 2.0, 1.0);
  s += dfm(time, beat / 2.0, 2.0);
  
  //s += t2;
  
  return 0.3 * s;
}
