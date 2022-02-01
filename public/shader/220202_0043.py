#define BPM 82.0
const float PI = acos(-1.0);
const float TAU = PI * 2.0;

/* GLSL */
// 2D Random
float _rnd(in vec2 st) {
  return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453123);
}


/* sound common */
float timeToBeat(float t) {return t / 60.0 * BPM;}
float beatToTime(float b) {return b / BPM * 60.0;}

float saw(float phase) {return 2.0 * fract(phase) - 1.0;}
float square(float phase) {return fract(phase) < 0.5 ? -1.0 : 1.0;}
float triangle(float phase) {return 1.0 - 4.0 * abs(fract(phase) - 0.5);}
float sine(float phase) {return sin(TAU * phase );}


float random(float time) {
  float rnd_x = sine(123.4 * time);
  float rnd_y = sine(567.8 * time);
  return _rnd(vec2(rnd_x, rnd_y)) - 0.5;
}



float kick(float time) {
  float amp = exp(-0.75 * time);
  float phase = 32.0 * time - 24.0 * exp(-1.25 * time);
  return amp * sine( phase );
}

float snare(float time){
  float s_amp = exp(-32.0 * time);
  float s_phase = 64.0 * time - 32.0 * exp(-8.0 * time);
  
  float n_amp = exp(-48.0 * time);
  float tic = n_amp * random(time * 1e2);
  float rnd = 2.0 * sine(123.4 * time) -1.0;
  float noize = tic * sin(random(rnd));
  
  return s_amp * sine(s_phase + noize);
}

float hihat(float time) {
  float amp = exp(-128.0 * time);
  
  float tic = amp * random(time);
  float rnd = 2.0 * saw(123.4 * time) -1.0;
  float vib = 0.5 * sine(time * .75);
  return tic * sin(random(rnd));
}

/*
vec2 hihat(float time) {
  float amp = exp(-128.0 * time);
  float tic = amp * random(time * 1e2);
  float rnd_x = 2.0 * sine(123.4 * time) -1.0;
  float rnd_y = 2.0 * sine(567.8 * time) -1.0;
  return vec2(tic * sin(random(rnd_x)), tic * random(rnd_y));
}
*/


vec2 mainSound(float time) {
  float beat = timeToBeat(time);
  float tempo = sine((mod(beat, 4.0) >= 1.0 ? 440.0 : 880.0) * time) * exp(-1e2 * fract(beat));
  
  float kikTiming = mod(beat, 8.0);
  float kickTime = beatToTime(kikTiming);
  float bd = kick(kickTime);
  
  float snareTimig = mod(beat - 1.0, 4.0);
  float snareTime = beatToTime(snareTimig);
  float sn = snare(snareTime);
  
  float hihTiming = mod(beat - 0.5, 2.0) >= 1.0? mod(beat - 0.5, 0.125):0.0;
  float hihatTime = beatToTime(hihTiming);
  float hh = hihat(hihatTime);
  
  
  float chainTime = beatToTime(mod(beat, 1.0));
  float kickchain = smoothstep(0.0, 0.75, chainTime);
  
  float bass_tone = mod(beat, 8.0) >= 7.5 ? 97.999:110.0;
  float vib = 0.2 * sine(time * 0.5);
  float bass1 = saw(bass_tone * time + vib) * kickchain;
  float bass2 = sine(bass_tone * time) * kickchain;
  
  float bass = clamp(bass1 + bass2, -1.0, 1.0);
  

  //float mono_mix = clamp((1.28 * bd) + (0.8 * sn) + (0.3 * bass), -1.0, 1.0);
  float mono_mix = clamp((bd) + (sn) + (hh), -1.0, 1.0);
  
  
  return vec2(mono_mix, tempo);
}
