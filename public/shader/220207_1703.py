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

vec2 mainSound(float time){
  vec2 o = vec2(0);
  //High & Harmonic
  //o += fm(time, 880.0, 1.0, 1.0) * exp(-time * 16.0);
  
  //Low & Harmonic
  o += fm(time, 110.0, 1.0, 1.0) * exp(-time * 16.0);
  
  //High Percussive
  //o += (hash12(time * 1e4) -0.5) * exp(-time * 16.0);

  //Low & Percussive
  //o += fm(time - 1.3 * exp(-time * 8.0), 15.0, 0.35, 0.71) * exp(-time * 16.0);
  
  return o;
}
