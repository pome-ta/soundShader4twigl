/* '__main__.py'を実行するやでー */

#define BPM 90.0  // ここでテンポの速度を決める
const float PI = acos(-1.0);
const float TAU = PI * 2.0;

/* common func */
float timeToBeat(float t) {return t / 60.0 * BPM;}
float beatToTime(float b) {return b / BPM * 60.0;}

float sine(float phase) {
  return sin(TAU * phase);
}

// 'time' => 1秒1拍
vec2 mainSound(float time) {
  float bpm = timeToBeat(time);  // BPM: 90 に
  
  vec2 sound = vec2(0.0);  // 最終出力用の'L(x)R(y)'
  
  /* '440.0Hz = A4(ラ)' を作る */
  // 'beatToTime(bpm)' は、'time' でも可('bpm' を1秒1拍に戻してる)
  float sine440 = sine(440.0 * beatToTime(bpm));
  
  // 'L'チャンネルに、音を突っ込む
  sound.x += sine440;
  
  
  /* メトロノームを作る */
  // 'mod(余剰計算)' で、4回に1回880Hz それ以外は、440Hz
  float metronome = sine(
    (
      mod(bpm, 4.0) >= 1.0 ? 440.0 : 880.0
    // 'mod' で決めたHz と'time' で'sine' 関数実行
    ) * time  // 'beatToTime(bpm)' でも可
  // bpm に合わせて音を減衰させる
    // 'fract' で、タイミングを決めるイメージ
  ) * exp(-1e2 * fract(bpm));
  
  
  // 'R'チャンネルに、メトロノームを突っ込む
  sound.y += metronome;
  
  return vec2(sound);
}

