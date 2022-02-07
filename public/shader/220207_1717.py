#define BPM 90.0
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
    0.0, 7.0, 5.0, 10.0,
    7.0, 3.0, 5.0, -2.0
  );
  
  float seq_time = mod(floor(bpm), 8.0);
  float seq_freq = 440.0 * calf(seq_line[int(seq_time)]);
  
  //High & Harmonic
  float hh_s = fm(time, 880.0, 1.0, 1.0) * exp(-time * 16.0);
  
  //Low & Harmonic
  float lh_s = fm(time, seq_freq, 1.0, 1.0) * exp(-time * 16.0);
  
  //High Percussive
  vec2 hp_s = (hash12(time * 1e4) -0.5) * exp(-time * 16.0);

  //Low & Percussive
  float lp_s = fm(time - 1.3 * exp(-time * 8.0), 15.0, 0.35, 0.71) * exp(-time * 16.0);
  
  float mono_mix = lh_s;
  
  return vec2(mono_mix);
}
