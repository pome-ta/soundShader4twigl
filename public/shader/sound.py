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

vec2 hash12(float t){
  vec3 p3 = fract(vec3(t) * vec3(0.101, 0.103, 0.979));
  p3 += dot(p3, p3.xzy + 33.33);
  return fract((p3.xx + p3.zy) * p3.xz);
}


float bass_step(float time, float tone) {
  return fm(time, tone, 1.0, 0.5) * exp(-fract(timeToBeat(time)) * 12.0);
}

vec2 mainSound(float time) {
  float bpm = timeToBeat(time);
  float tempo = sine((mod(bpm, 4.0) >= 1.0 ? 440.0 : 880.0) * time) * exp(-1e2 * fract(bpm));
  
  
  float g2 = 110.0 * pitch(-2.0);
  float a2 = 110.0 * pitch(0.0);
  float a3 = 220.0 * pitch(0.0);
  float b3 = 220.0 * pitch(2.0);
  float c4 = 220.0 * pitch(3.0);
  float d4 = 220.0 * pitch(5.0);
  float e4 = 440.0 * pitch(-5.0);
  float f4 = 440.0 * pitch(-4.0);
  float g4 = 440.0 * pitch(-2.0);
  float a4 = 440.0 * pitch(0.0);
  float b4 = 440.0 * pitch(2.0);
  float c5 = 440.0 * pitch(3.0);
  
  
  float gate = mod(bpm * 1.0, 8.0);
  /*
  float gate_i = ceil(gate);
  float gate_f = mod(gate, 1.0);
  float bass =
    //gate_i == 1.0 ? bass_step(time, c4):
    gate_i == 1.0 ? gate_f <= 0.5 ? bass_step(time, c4) : bass_step(time, c5) :
    gate_i == 2.0 ? bass_step(time, d4):
    gate_i == 3.0 ? bass_step(time, e4):
    gate_i == 4.0 ? bass_step(time, f4):
    gate_i == 5.0 ? bass_step(time, g4):
    gate_i == 6.0 ? bass_step(time, a4):
    gate_i == 7.0 ? bass_step(time, b4):
    gate_i == 8.0 ? bass_step(time, c5):
    0.0;
  */
  /*
  float bass =
    gate < 1.0 ? bass_step(time, c4):
    gate < 1.5 ? bass_step(time, d4):
    gate < 3.0 ? bass_step(time, e4):
    gate < 4.0 ? bass_step(time, f4):
    gate < 5.0 ? bass_step(time, g4):
    gate < 6.0 ? bass_step(time, a4):
    gate < 7.0 ? bass_step(time, b4):
    gate < 8.0 ? bass_step(time, c5):
    0.0;
  */
  float bass = bass_step(time*2.0, c4);
  
  
  
  //float bass = fm(time, seq_freq, 1.0, 1.0) * exp(-fract(bpm / 2.0) * 16.0);
  
  
  return vec2(bass);
}
