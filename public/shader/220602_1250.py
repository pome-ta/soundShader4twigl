// memo: ドローンと8ビートあわせたらひどくなったやつ
#define BPM 90.0

const float PI = acos(-1.0);
const float TAU = PI * 2.0;

/* sound common */
float timeToBeat(float t) {return t / 60.0 * BPM;}
float beatToTime(float b) {return b / BPM * 60.0;}

float rand(vec2 st) {
  vec2 magic2 = vec2(12.9898, 78.233);
  float _rnd = sin(dot(st, magic2));
  return fract(_rnd * 43758.5453123);
}

float pitch(float p) {
  return pow(2.0, p / 12.0) * 440.0;
}

float rect(float beat) {
  if (fract(beat / PI / 2.0) < 0.5) {
    return 1.0;  
  } else {
    return 0.0;
  }
}


float sine(float phase) {
  return sin(TAU * phase);
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


float drone(float time, float semitones[4]) {
  float s = 0.0;
  const int VOICES = 4;
  for (int i=0; i<4; i++) {
    float f = pitch(-12.0 + semitones[i]);
    const int UNISON = 4;
    for (int u=0; u<UNISON; u++) {
      float fu = float(u);
      float new_f = f + fu * tan(fu);
      s += square(time * new_f) * (1.0 / float(UNISON)) * (1.0 / float(VOICES));
    }
  }
  return s;
}


float strings(float beat) {
  float tb = beat / 2.0;
  float t = mod(tb * 4.0, 1.0);
  float sound = 0.0;
  if (mod(tb, 8.0) < 4.0) {
    sound += rect(beatToTime(beat) * pitch(24.0));
    sound += rect(beatToTime(beat) * pitch(26.0));
    sound += rect(beatToTime(beat) * pitch(31.0));
    sound += rect(beatToTime(beat) * pitch(33.0));
  } else {
    sound += rect(beatToTime(beat) * pitch(22.0));
    sound += rect(beatToTime(beat) * pitch(27.0));
    sound += rect(beatToTime(beat) * pitch(31.0));
    sound += rect(beatToTime(beat) * pitch(24.0));
  }
  return sound * max(0.0, (1.0 - t * 2.0));
}

float bass(float beat) {
  float t = mod(beat / 2.0, 8.0);
  if (t < 2.0) {
    return rect(beatToTime(beat) * pitch(-2.0));
  }
  if (t > 3.0 && t < 3.5) {
    return rect(beatToTime(beat) * pitch(-1.0));
  }
  if (t < 4.0) {
    return rect(beatToTime(beat) * pitch(11.0));
  }
  if (t < 6.0) {
    return rect(beatToTime(beat) * pitch(10.0));
  }
  if (t < 8.0) {
    return rect(beatToTime(beat) * pitch(-1.0));
  }
  return 0.0;
}


float bassDrum(float beat) {
  float t = mod(beat / 2.0, 1.0) / 3.0 * 8.0;
  float bd = sin(beatToTime(beat) * pitch(0.0));
  return bd * max(0.0, 1.0 - fract(t) * 8.0);
}


float snereDrum(float beat) {
  float t = mod((beat / 2.0) + 0.5, 1.0);
  float sd = rand(vec2(beatToTime(beat) * 32.0, 0.0));
  return sd * max(0.0, 1.0 - t * 4.0);
}

float hiHat(float beat) {
  // xxx:
  float t = beat / 2.0 * 16.0;
  if (mod(t, 16.0) > 3.0 && mod(t, 2.0) > 1.0) {
    return 0.0;
  }
  float hh = rand(vec2(beatToTime(beat) * 32.0, 0.0));
  return hh * max(0.0, 1.0 - fract(t) * 4.0);
}


vec2 mainSound(float time){
  float bpm = timeToBeat(time);
  float tempo = sine((mod(bpm, 4.0) >= 1.0 ? 440.0 : 880.0) * time) * exp(-1e2 * fract(bpm));
  
  
  float s = 0.0;
  float semitones1[4];
  semitones1[0] = 0.0; semitones1[1] = 2.0;
  semitones1[2] = 7.0; semitones1[3] = 9.0;
  
  float semitones2[4];
  semitones2[0] = -2.0; semitones2[1] = 3.0;
  semitones2[2] = 7.0; semitones2[3] = 12.0;
  
  
  float timing = PI * bpm / 64.0;
  float semi1 = drone(time, semitones1) * cos(timing);
  float semi2 = drone(time, semitones2) * sin(timing);
  
  float sound = 0.0;
  sound += bassDrum(bpm) * 0.6;
  sound += snereDrum(bpm) * 0.5;
  sound += hiHat(bpm) * 0.4;
  sound += strings(bpm) * 0.125;
  sound += bass(bpm) * 0.2;
  
  
  s = max(semi1, semi2);
  float f = sin(TAU * bpm * 8.0);
  float bs = sin(TAU * 64.0 * time + (s / 2.0) + f) * pow(fract(-bpm / 2.0), 1.25);
  
  return vec2((semi1 + semi2 + (bs * 0.8)) * 0.5 + sound);
  //float sq = square(time * 440.0);
  //return vec2(sq);
}

