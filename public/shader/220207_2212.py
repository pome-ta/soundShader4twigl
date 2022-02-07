#define BPM 140.0
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
  
float calf(float i){
  return pow(2.0, i / 12.0);
}

vec2 hash12(float t){
  vec3 p3 = fract(vec3(t) * vec3(0.101, 0.103, 0.979));
  p3 += dot(p3, p3.xzy + 33.33);
  return fract((p3.xx + p3.zy) * p3.xz);
}


float bass_step(float tone, float time) {
  return fm(time, tone, 1.0, 1.0) * exp(-time * 16.0);
}

vec2 mainSound(float time) {
  float bpm = timeToBeat(time);
  float tempo = sine((mod(bpm, 4.0) >= 1.0 ? 440.0 : 880.0) * time) * exp(-1e2 * fract(bpm));
  
  
  float[8] seq_line = float[](
    0.0, -2.0, 0.0, -2.0,
    0.0, -2.0, 0.0, -5.0
  );
  
  float seq_time = mod(floor(bpm), 8.0);
  float base_tone = 110.0;
  float seq_freq = base_tone * calf(seq_line[int(seq_time)]);
  
  float gate = mod(bpm * 1.0, 4.0);
  
  float bass;
  bass = gate < 1.0 ? sine(440.0 * time) * exp(-3.0 * fract(bpm)):
         gate < 2.0 ? 0.0:
         gate < 3.0 ? sine(220.0 * time) * exp(-3.0 * fract(bpm)):
         0.0;
  
  
  //float bass = fm(time, seq_freq, 1.0, 1.0) * exp(-time * 16.0);
  //float bass = fm(time, seq_freq, 1.0, 1.0) * fract(-bpm);
  //float bass = bass_step(seq_freq, time);
  

  
  float mono_mix = bass;
  
  return vec2(mono_mix, tempo);
}
