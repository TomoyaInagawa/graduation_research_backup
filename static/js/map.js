//現在位置
var current_point = [35.0394, 135.7292];

//マーカー一覧保持用の連想配列
var markers = {};

// 地図本体
var map;

//マーカーを追加する処理
function addMarker(map, markers, id, lat, lng, name) {
  // idをキーとしてマーカー一覧にマーカーを追加
  markers[id] = L.marker([lat, lng], { draggable: true })
    .bindTooltip(name, { permanent: true }) // ツールチップで名称を表示
  markers[id].id = id;

  // 今回は使わないが下記形式で任意のデータを持たせることが可能
  markers[id].data = { x: "hoge", y: "fuga" };  // markers[id].data.xのように参照する

  // マップにマーカーを追加
  markers[id].addTo(map);
}

// 地図の初期化処理
function init() {
//地図を表示するdiv要素のidを設定
map = L.map('mapcontainer');

//地図の中心とズームレベルを指定
map.setView(current_point, 14);

//表示するタイルレイヤのURLとAttributionコントロールの記述を設定して、地図に追加する
L.tileLayer('https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png', {
  attribution: '© 国土地理院'
}).addTo(map);

//circleオブジェクトを作成して地図に追加
L.circle(current_point, { radius: 2000, color: "#FF5555", fill: false, weight: 3 }).addTo(map);

//現在位置のマーカーを地図に追加、ツールチップを表示
L.marker(current_point, { draggable: false })
  .bindTooltip("現在位置", { permanent: true })
  .addTo(map);
}
