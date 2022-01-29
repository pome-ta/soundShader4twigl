const float BPM = 140.;
const float PI = acos(-1.0);
const float TAU = PI * 2.0;


/*
float saw(float phase) {
    return 2.0 * fract(phase) - 1.0;
}

float square(float phase) {
    return fract(phase) < 0.5 ? -1.0 : 1.0;
}

float triangle(float phase) {
    return 1.0 - 4.0 * abs(fract(phase) - 0.5);
}



float sine(float freq, float time) {
  return sin(freq * TAU * time);
}


float metronom4b4(float bpm, float time) {
  float click = sin(mod(bpm, 4.0) >= 1.0 ? 440.0:880.0*TAU* time);
  float envelope = exp(-1e2 * fract(bpm));
  return click * envelope;
  
}
*/
float timeToBeat(float time) {
  return time / 60.0 * BPM;
}

float sine(float freq, float time) {
  return sin(freq * TAU * time);
}


vec2 mainSound(float time) {
  float beat = timeToBeat(time);
  
  //float tempo = metronom4b4(beat, time);
  float tempo = sine(mod(beat, 4.0) >= 1.0 ? 440.0:880.0, time) * exp(-1e2 * fract(beat));
  
  //float wave = triangle(440.0 * time);
  return vec2(tempo);
}
