#define BPM 180.0
const float PI = acos(-1.0);
const float TAU = PI * 2.0;



/* sound common */
float timeToBeat(float t) {return t / 60.0 * BPM;}
float beatToTime(float b) {return b / BPM * 60.0;}

float fm(float t, float f, float i, float r){
  return sin(TAU * f * t + i * sin(TAU * f * t * r));
}

// 音程
float calf(float i){
  return pow(2.0 , i / 12.0);
}

float step_tone(float tone, float[8] line, float time) {
  float bpm = timeToBeat(time);
  float seq_time = mod(floor(bpm), 8.0);
  float seq_freq = tone * calf(line[int(seq_time)]);
  return fm(time, seq_freq, 0.5, 1.0) * fract(-bpm);
}


vec2 mainSound(float time){
  float bpm = timeToBeat(time);
  
  float seq;
  
  float[8] seq_line = float[](
    0.0, 2.0, 4.0, 5.0,
    7.0, 9.0, 11.0, 12.0
  );
  
  float cn = 13.75 * calf(3.0);
  float c0 = 27.5 * calf(3.0);
  float c1 = 55.0 * calf(3.0);
  float c2 = 110.0 * calf(3.0);
  float c3 = 220.0 * calf(3.0);
  float c4 = 440.0 * calf(3.0);
  float c5 = 880.0 * calf(3.0);
  float c6 = 1760.0 * calf(3.0);
  float c7 = 3520.0 * calf(3.0);
  
  seq += step_tone(cn, seq_line, time);
  seq += step_tone(c0, seq_line, time);
  seq += step_tone(c1, seq_line, time);
  seq += step_tone(c2, seq_line, time);
  seq += step_tone(c3, seq_line, time);
  seq += step_tone(c4, seq_line, time);
  seq += step_tone(c5, seq_line, time);
  seq += step_tone(c6, seq_line, time);
  seq += step_tone(c7, seq_line, time);
  
  
  return vec2(seq * 0.2);
}
