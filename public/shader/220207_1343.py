// https://raku-phys.hatenablog.com/entry/2020/05/22/204117

#define pi2 6.2631
#define bpm 118.0

float fm(float t, float f, float i, float r){
  return sin(pi2 * f * t + i * sin(pi2 * f * t * r));
}
float calf(float i){
  return pow(2.0 , i / 12.0);
}
vec2 mainSound(float time){
  float tbpm = time * bpm / 60.0;
  float[8] seq_line = float[](
    0.0, 7.0, 5.0, 10.0,
    7.0, 3.0, 5.0, -2.0
  );
  float seq_time = mod(floor(tbpm), 8.0);
  float seq_freq = 440.0 * calf(seq_line[int(seq_time)]);
  float seq = fm(time,seq_freq, 0.5, 1.0) * fract(-tbpm);
  return vec2(seq * 0.5);
}
