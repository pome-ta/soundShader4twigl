#define BPM 132.0
const float PI = acos(-1.0);
const float TAU = PI * 2.0;


float timeToBeat(float t) {return t / 60.0 * BPM;}
float beatToTime(float b) {return b / BPM * 60.0;}


float saw(float phase) {return 2.0 * fract(phase) - 1.0;}
float square(float phase) {return fract(phase) < 0.5 ? -1.0 : 1.0;}
float triangle(float phase) {return 1.0 - 4.0 * abs(fract(phase) - 0.5);}
float sine(float phase) {return sin(TAU * phase );}


float kick(float time) {
  float amp = exp(-24.0 * time);
  float phase = 48.0 * time - 4.8 * exp(-48.0 * time);
  return amp * sine( phase );
}




vec2 mainSound(float time) {
  float beat = timeToBeat(time);
  float tempo = sine((mod(beat, 4.0) >= 1.0 ? 440.0 : 880.0) * time) * exp(-1e2 * fract(beat));
  
  float kikTiming = mod(beat, 16.0) <= 15.0 ? mod(beat, 1.0) : mod(beat, 0.5);
  float kickTime = beatToTime(kikTiming);
  
  float bd = kick(kickTime);
  
  
  float a2 = 110.0;
  float a3 = 220.0;
  
  float w = sine(a3 * time);
  
  
  //return vec2(tempo, bd);
  //return vec2(bd+ wav);
  return vec2(bd, w);
}
