// [twigl.app](https://twigl.app/?ol=true&mode=3&source=gl_FragColor%3Dvec4(0)%3B&sound=true&soundsource=vec2%20s(float%20t,float%20n)%7B%0A%20%20float%20o%20%3D%201.059%3B%0A%20%20return%20vec2(sin(6.2831*440.*max(0.,t)*pow(o,n))*exp(-3.*t))*0.2%3B%0A%7D%0A%0Avec2%20mainSound(float%20time)%7B%0A%20%20float%20t%3Dtime%3B%0A%20%20return%20s(t-0.,3.)%2Bs(t-1.,5.)%2Bs(t-2.,7.)%3B%0A%7D)
// [https://twitter.com/ayano_tft/status/1546786874181980160?s=12&t=iIzCEjt5xT2arCDwEDBQ6Q](https://twitter.com/ayano_tft/status/1546786874181980160?s=12&t=iIzCEjt5xT2arCDwEDBQ6Q)


vec2 s(float t, float n){
  float o = 1.059;
  return vec2(sin(6.2831 * 440.0 * max(0.0, t) * pow(o, n)) * exp(-3.0 * t)) * 0.2;
}

vec2 mainSound(float time){
  float t = time;
  return s(t - 0.0, 3.0) + s(t - 1.0, 5.0) + s(t - 2.0, 7.0);
}

