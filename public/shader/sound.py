// memo: 440 sine wave

const float PI = acos(-1.0);
const float TAU = PI * 2.0;


vec2 mainSound(float time) {
  float sound = sin(TAU * 440.0 *time);
  
  return vec2(sound);
}



