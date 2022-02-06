#define BPM 90.0
const float PI = acos(-1.0);
const float TAU = PI * 2.0;



/* sound common */
float timeToBeat(float t) {return t / 60.0 * BPM;}
float beatToTime(float b) {return b / BPM * 60.0;}

float sine(float phase) {
  return sin(TAU * phase);
}


float rhy(float time, float fade){
  return pow(fract(-time), 6.0 - fade * 3.0);
}
vec2 delay(float time, float dt){
  return exp(-2.0 * dt) * sin(TAU * 440.0 * beatToTime(time)) * 
    vec2(rhy(time - dt * 0.3, dt),
         rhy(time - dt * 0.5, dt));
}



vec2 mainSound(float time){
  float beat = timeToBeat(time);
  float tempo = sine((mod(beat, 4.0) >= 1.0 ? 440.0 : 880.0) * time) * exp(-1e2 * fract(beat));
  
  vec2 s;
  s += delay(beat, 0.0);
  s += delay(beat, 1.1);
  s += delay(beat, 1.9);
  s += delay(beat, 1.92);
  s += delay(beat, 1.95);
  
  return s;
}
