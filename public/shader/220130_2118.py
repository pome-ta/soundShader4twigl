/* FM */

const float BPM = 140.0;
const float PI = acos(-1.0);
const float TAU = PI * 2.0;


float saw(float phase) {
    return 2.0 * fract(phase) - 1.0;
}

float square(float phase) {
    return fract(phase) < 0.5 ? -1.0 : 1.0;
}

float triangle(float phase) {
    return 1.0 - 4.0 * abs(fract(phase) - 0.5);
}

float sine(float phase) {
    return sin( TAU * phase );
}


float kick(float time) {
    float amp = exp( -5.0 * time );
    float phase = 50.0 * time
                - 10.0 * exp( -70.0 * time );
    return amp * sine( phase );
}

float timeToBeat(float time) {
  return time / 60.0 * BPM;
}



vec2 mainSound(float time) {
  float beat = timeToBeat(time);
  
  float tempo = sine((mod(beat, 4.0) >= 1.0 ? 440.0 : 880.0) * time) * exp(-1e2 * fract(beat));
  
  float vib = 0.2 * sine((mod(beat, 4.0) <= 2.0 ? 0.0:beat) * 8.0);
  float freq440 = 440.0;
  float fm = 0.1 * sine(freq440 * time * 7.0);
  float wave = sine(freq440 * time + fm);
  
  
  
  
  
  return vec2(tempo, wave);
}
