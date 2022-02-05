#define BPM 92.0
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
  
  float phz = 440.0;
  float nhz = -11.0;
  
  float pos_t = square(phz * beatToTime(beat));
  float neg_t = square(nhz * beatToTime(beat));
  float gate = mod(beat * 0.5, 4.0);
  float w =  gate < 1.0? pos_t:
             gate < 2.0? neg_t:
             gate < 3.0? pos_t - pos_t:
             gate < 4.0? pos_t - neg_t:
             0.0;

  return vec2(w, tempo);
}













