#define BPM 90.0
const float PI = acos(-1.0);
const float TAU = PI * 2.0;



/* sound common */
float timeToBeat(float t) {return t / 60.0 * BPM;}
float beatToTime(float b) {return b / BPM * 60.0;}

float sine(float phase) {
  return sin(TAU * phase );
}
float saw(float phase) {
  return 2.0 * fract(phase) - 1.0;
}
float square(float phase) {
  return fract(phase) < 0.5 ? -1.0 : 1.0;
}
float triangle(float phase) {
  return 1.0 - 4.0 * abs(fract(phase) - 0.5);
}
float pulse(float phase, float duty) {
  return fract(phase) < abs(duty) ? -1.0 : 1.0;
}





float adsr(float t, float a, float d, float s, float r, float gt) {
  return max(0.0, min(1.0, t/max(1e-4, a)) - min((1.0 - s) ,max(0.0, t - a)*(1.0 - s)/max(1e-4, d)) - max(0.0, t - gt)*s/max(1e-4, r));
}





vec2 mainSound(float time) {
  float beat = timeToBeat(time);
  float tempo = sine((mod(beat, 4.0) >= 1.0 ? 440.0 : 880.0) * time) * exp(-1e2 * fract(beat));
  
  //float w = sine(440.0 * time) * pow(fract(-beat / 4.0), 8.0);
  float v = fract(beat);
  float w = sine(440.0 * time) + v;
  float s = sin(beat);
  
  return vec2(abs(s));
  //return vec2(tempo);
}













