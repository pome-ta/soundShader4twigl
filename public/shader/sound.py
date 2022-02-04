#define BPM 90.0
const float PI = acos(-1.0);
const float TAU = PI * 2.0;



/* sound common */
float timeToBeat(float t) {return t / 60.0 * BPM;}
float beatToTime(float b) {return b / BPM * 60.0;}

float sine(float phase) {
  return sin(TAU * phase);
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

float cent(float dig) {
  return pow(2.0, dig / 12.0);
}



vec2 mainSound(float time) {
  float beat = timeToBeat(time);
  float tempo = sine((mod(beat, 4.0) >= 1.0 ? 440.0 : 880.0) * time) * exp(-1e2 * fract(beat));
  
  float baseHZ = 55.0;
  
  float gate = mod(beat * 2.0, 8.0);
  float tone = gate <= 1.0 ? baseHZ * cent(12.0):
                 gate <= 1.8 ? 0.0:
               gate <= 2.0 ? baseHZ * cent(12.0):
                 gate <= 2.8 ? 0.0:
               gate <= 3.0 ? baseHZ * cent(12.0):
               gate <= 4.0 ? baseHZ * cent(12.0):
               gate <= 5.0 ? baseHZ * cent(12.0):
               gate <= 6.0 ? baseHZ * cent(12.0):
                 gate <= 6.8 ? 0.0:
               gate <= 7.0 ? baseHZ * cent(7.0):
               gate < 8.0 ? 0.0: 0.0;
  
  float w = sine(tone * time);
  return vec2(w, tempo);
}













