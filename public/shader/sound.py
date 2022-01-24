vec2 mainSound(float time) {
  float pi = acos(-1.0);
  float pi2 = pi * 2.0;
  float sine_wave = sin(pi2 * 440.0 * time);
  float pitch5 = sin(pi2 * 440.0 * 1.5 * time);
  return vec2(0.4 * (sine_wave + pitch5));
}

