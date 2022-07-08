// memo: note

#define BPM 60.0
const float PI = acos(-1.0);
const float TAU = PI * 2.0;

/* sound common */
float timeToBeat(float t) {return t / 60.0 * BPM;}
float beatToTime(float b) {return b / BPM * 60.0;}

float sine(float phase) {
  return sin(TAU * phase);
}

float calcHertz(float scale) {
  return 220.0 * pow(2.0, scale / 12.0);
}

float triangle(float phase) {
  return 1.0 - 4.0 * abs(fract(phase) - 0.5);
}

vec2 mainSound(float time) {
  float bpm = timeToBeat(time);

  float note;
  // C4
  note = 3.0;
  
  // D4
  note = 5.0;
  
  // E4
  note = 7.0;
  
  // F4
  note = 8.0;
  
  // G4
  note = 10.0;
  
  // A4
  note = 12.0;
  
  // B4
  note = 14.0;
  
  // C5
  note = 15.0;


  float freq = calcHertz(note);
  
  float fm = 0.07 * sine(time * freq * 7.0);
  float vib = fm * sine(time * 4.0);

  float sound = triangle(time * freq + vib) * exp(-time * 0.5) * fract(-time / 4.0);

  return vec2(sound);
}
