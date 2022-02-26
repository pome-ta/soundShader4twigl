#define BPM 90.0
const float PI = acos(-1.0);
const float TAU = PI * 2.0;

/* sound common */
float timeToBeat(float t) {return t / 60.0 * BPM;}
float beatToTime(float b) {return b / BPM * 60.0;}

float sine(float phase) {
  return sin(TAU * phase);
}

float kick_sine(float phase) {
  return cos(TAU * phase);
}


float rand(vec2 st) {
  vec2 magic2 = vec2(12.9898, 78.233);
  float _rnd = sin(dot(st, magic2));
  return fract(_rnd * 43758.5453123);
}

float calcHertz(float scale) {
  return 440.0 * pow(2.0, scale / 12.0);
}

float bassDrum(float beat) {
  float t = mod(beat / 2.0, 1.0) / 3.0 * 8.0;
  float bd = sin(beatToTime(beat) * calcHertz(0.0));
  return bd * max(0.0, 1.0 - fract(t) * 8.0);
}


float kick(float time) {
    float amp = exp( -5.0 * time );
    float phase = 50.0 * time
                - 10.0 * exp( -70.0 * time );
    return amp * sine( phase );
}

vec2 mainSound(float time) {
  float bpm = timeToBeat(time);
  
  float tempo = sine((mod(bpm, 4.0) >= 1.0 ? 440.0 : 880.0) * time) * exp(-1e2 * fract(bpm));
  
  float sound = 0.0;
  float bd = 0.0;
  bd += kick_sine(beatToTime(bpm) * (640.0 - abs(sin(bpm * PI))));
  sound += bd * smoothstep(0.2, 1.0, fract(-bpm));
  
  
  //sound += tempo;
  
  
  if (abs(sound) > 1.0) sound /= abs(sound);
  
  return vec2(sound);
}


