/* bd bass */
#define BPM 140.0
const float PI = acos(-1.0);
const float TAU = PI * 2.0;


float timeToBeat(float t) {return t / 60.0 * BPM;}
float beatToTime(float b) {return b / BPM * 60.0;}


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






vec2 mainSound(float time) {
  float soundMixer;
  float beat = timeToBeat(time);
  float tempo = sine((mod(beat, 4.0) >= 1.0 ? 440.0 : 880.0) * time) * exp(-1e2 * fract(beat));
  
  float bass = square(220.0 * time) * 0.1 + sin(time) * 0.7;
  
  float kickTime = beatToTime(mod(beat,1.0));
  float vib = 0.2 * sine((mod(beat, 4.0) <= 2.0 ? 0.0:beat) * 8.0);
  float freq440 = 440.0;
  float fm = 0.1 * sine(freq440 * time * 2.0);
  float wave = sine(freq440 * time);
  
  
  float sidechain = smoothstep(0.0, 0.5, kickTime);
  
  soundMixer += 0.5 * (kick(kickTime));
  soundMixer += bass * sidechain;
  if (abs(soundMixer) > 1.0) soundMixer /= abs(soundMixer);
  
  //return vec2(kick(kickTime), bass * sidechain);
  return vec2(0.9 * soundMixer);
}
