#define BPM 90.0
const float PI = acos(-1.0);
const float TAU = PI * 2.0;

/* common func */
float timeToBeat(float t) {return t / 60.0 * BPM;}
float beatToTime(float b) {return b / BPM * 60.0;}

float sine(float phase) {
  return sin(TAU * phase);
}


vec2 mainSound(float time) {
  float bpm = timeToBeat(time);
  
  vec2 sound = vec2(0.0);
  
  float sine440 = sine(440.0 * beatToTime(bpm));
  sound.x += sine440;
  
  float metronome = sine((mod(bpm, 4.0) >= 1.0 ? 440.0 : 880.0) * time) * exp(-1e2 * fract(bpm));
  sound.y += metronome;
  
  return vec2(sound);
}

