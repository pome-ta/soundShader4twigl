vec2 mainSound(float time){
  float pi = acos(-1.0);
  return vec2(sin(pi * 2.0 * 440.0 * time));
}

