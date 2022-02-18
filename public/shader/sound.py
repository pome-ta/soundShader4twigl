#define BPM 110.0
const float PI = acos(-1.0);
const float TAU = PI * 2.0;

/* sound common */
float timeToBeat(float t) {return t / 60.0 * BPM;}
float beatToTime(float b) {return b / BPM * 60.0;}


float sine(float phase) {
  return sin(TAU * phase);
}


float pitch(float p, float t) {
  return pow(2.0, p / 12.0) * t;
}

float saw(float phase) {
  float s = 0.0;
  for (int k=1; k<=8; k++) {
    s += (sin(TAU * float(k) * phase) / float(k));
  }
  return (1.0 / 2.0) - (1.0 / PI) * s - 0.5;
}

float square(float phase) {
  float s = 0.0;
  for (int k=1; k<8; k++) {
    s += sin(TAU * (2.0 * float(k) - 1.0) * phase) / (2.0 * float(k) - 1.0);
  }
  return (4.0 / PI) * s;
}

float kick_sine(float phase) {
  return sin(TAU * phase);
}



vec2 mainSound(float time){
  float bpm = timeToBeat(time);
  float tempo = sine((mod(bpm, 4.0) >= 1.0 ? 440.0 : 880.0) * time) * exp(-1e2 * fract(bpm));
  
  float s = kick_sine(pitch(0.0, 64.0) * time);
  s *= mod(-bpm, 1.0);
  
  return vec2(s);
}


