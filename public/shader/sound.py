vec2 mainSound(float time) {
  float pi = acos(-1.0);
  float pi2 = pi * 2.0;
  
  float tempo = abs(sin(time / 10.0));
  
  float wave44 = sin(pi2 * 440.0 * time);
  float env44 = wave44 * mod(-time * 0.5, 0.25);
  
  float wave88 = sin(pi2 * 880.0 * time);
  float env88 = wave88 * fract(time / -2.0);
  
  return vec2(env44, env88);
}
