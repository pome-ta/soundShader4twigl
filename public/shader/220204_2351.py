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
  
  float a1 = 55.0;
  
  float g2 = a1 * cent(10.0);
  float a2 = 110.0;
  float b2 = a2 * cent(2.0);
  
  float d3 = a2 * cent(5.0);
  float g3 = a2 * cent(10.0);
  float a3 = 220.0;
  float b3 = a3 * cent(2.0);
  
  float d4 = a3 * cent(5.0);
  float a4 = 440.0;
  
  float a5 = 880.0;
  
  float gate = mod(beat * 1.0, 4.0);
  float gate_f = mod(gate, 1.0);
  float gate_i = ceil(gate);
  /*
  float tone = gate_i == 1.0 || gate_i == 3.0 ? a2:
                 //gate_f < 0.5 ? a3: g3:
               gate_i == 2.0 || gate_i == 4.0 ? g2:
                 //gate_f < 0.5 ? a3: g3:
               0.0;
   */
   float tone = gate < 1.0 ? a2:
                gate < 3.0 ? g2:
                0.0;
               
  
  float w = sine(tone * time) * smoothstep(0.0, 1.0, fract(beat));
  return vec2(w);
}













