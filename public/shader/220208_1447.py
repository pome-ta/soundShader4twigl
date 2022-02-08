#define BPM 128.0
const float PI = acos(-1.0);
const float TAU = PI * 2.0;



/* sound common */
float timeToBeat(float t) {return t / 60.0 * BPM;}
float beatToTime(float b) {return b / BPM * 60.0;}

float sine(float phase) {
  return sin(TAU * phase);
}

float fm(float t, float f, float i, float r){
  return sin(TAU * t * f + i * sin(TAU * t * f * r));
}
  
float pitch(float i){
  return pow(2.0, i / 12.0);
}



vec2 mainSound(float time) {
  float bpm = timeToBeat(time);
  float tempo = sine((mod(bpm, 4.0) >= 1.0 ? 440.0 : 880.0) * time) * exp(-1e2 * fract(bpm));
  
  float i = 3.0;
  
  float f = tan(TAU * bpm * 32.0);
  float w = sin((TAU * time * 110.0) + (f));
  
  
  return vec2(w * 0.5, tempo);
}
