#define BPM 90.0

const float PI = acos(-1.0);
const float TAU = PI * 2.0;

/* sound common */
float timeToBeat(float t) {return t / 60.0 * BPM;}
float beatToTime(float b) {return b / BPM * 60.0;}


float sine(float phase) {
  return sin(TAU * phase);
}


float pitch(float p) {
  return pow(2.0, p / 12.0) * 440.0;
}


float saw(float phase) {
  float s = 0.0;
  for (int k=1; k<=8; k++) {
    s += (sin(TAU * float(k) * phase) / float(k));
  }
  return (1.0 / 2.0) - (1.0 / PI) * s - 0.5;
}


float drone(float time, float semitones[4]) {
  float s = 0.0;
  const int VOICES = 4;
  for (int i=0; i<4; i++) {
    float f = pitch(-12.0 + semitones[i]);
    const int UNISON = 4;
    for (int u=0; u<UNISON; u++) {
      float fu = float(u);
      float new_f = f + fu * tan(fu);
      s += saw(time * new_f) * (1.0 / float(UNISON)) * (1.0 / float(VOICES));
      //s *= fract(-timeToBeat(time) / 16.0);
    }
  }
  return s;
}


vec2 mainSound(float time){
  float bpm = timeToBeat(time);
  float tempo = sine((mod(bpm, 4.0) >= 1.0 ? 440.0 : 880.0) * time) * exp(-1e2 * fract(bpm));
  
  /*
  float s = 0.0;
  float semitones1[4];
  semitones1[0] = 0.0; semitones1[1] = 2.0;
  semitones1[2] = 7.0; semitones1[3] = 9.0;
  
  float semitones2[4];
  semitones2[0] = -2.0; semitones2[1] = 2.0;
  semitones2[2] = -7.0; semitones2[3] = 8.0;
  
  float bar = 8.0;
  float fadein = min(1.0, mod(bpm, bar));
  float semi1 = drone(time, semitones1) * fadein;
  float semi2 = drone(time, semitones2) * fadein;
  
  
  
  s = mod(bpm, bar * 2.0) < bar ? semi1:semi2;
  
  float f = sin(TAU * bpm * 8.0);
  float bs = sin(TAU * 64.0 * time + (s / 2.0) + f) * pow(fract(-bpm / 2.0), 1.25);
  
  //return vec2((s + bs) * 0.3);
  */
  float inout_fade1 = min(
    min(1.0, mod(bpm / 2.0, 4.0)),
    min(1.0, mod(-bpm / 2.0, 4.0))
  );
  float inout_fade2 = min(
    min(1.0, mod((bpm + 2.0) / 2.0, 4.0)),
    min(1.0, mod(-(bpm + 2.0) / 2.0, 4.0))
  );
  
  float stiming = sin(PI * bpm / 32.0);
  float ctiming = cos(PI * bpm / 32.0);
  
  float sin4 = sine(220.0 * time) * stiming;
  float saw4 = saw(220.0 * time) * ctiming;
  
  
  
  //float mix_out = (sin4 + tempo);
  float mix_out = (sin4 + saw4);
  //return vec2(mix_out, tempo);
  return vec2(mix_out);
}
