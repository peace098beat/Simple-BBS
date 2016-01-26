/*
form無いでUPLOAD画像のプレビューを表示するスクリプト
*/
function preview(ele) {
    if (!ele.files.length) return;  // ファイル未選択

    var file = ele.files[0];
    if (!/^image\/(png|jpeg|gif)$/.test(file.type)) return;  // typeプロパティでMIMEタイプを参照

    var img = document.createElement('img');
    var fr = new FileReader();
    fr.onload = function() {
        img.src = fr.result;  // 読み込んだ画像データをsrcにセット
        document.getElementById('preview_field').appendChild(img);
    }
    fr.readAsDataURL(file);  // 画像読み込み

    // 画像名・MIMEタイプ・ファイルサイズ
    document.getElementById('preview_field').innerHTML =
//        'file name: ' + file.name + '<br />' +
//        'file type: ' + file.type + '<br />' +
        'file size: ' + file.size + '<br />';
}