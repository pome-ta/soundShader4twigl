#define BPM 90.0
const float PI = acos(-1.0);
const float TAU = PI * 2.0;



/* sound common */
float timeToBeat(float t) {return t / 60.0 * BPM;}
float beatToTime(float b) {return b / BPM * 60.0;}

float sine(float phase) {
  return sin(TAU * phase);
}



vec2 mainSound(float time){
  float bpm = timeToBeat(time);
  float tempo = sine((mod(bpm, 4.0) >= 1.0 ? 440.0 : 880.0) * time) * exp(-1e2 * fract(bpm));
  
  float tone = 440.0;
  
  float bass_tone = sine(tone * fract(time));
  
  float s = bass_tone;
  
  return vec2(s);
}
