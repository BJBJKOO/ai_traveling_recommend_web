//버튼을 클릭하면
$("button.survay-btn").click(function () {
  var error = "";
  $("div.survays").each(function () {
    //해당설문이름 가져오기
    var survaysName =
      $(this)
        .find("span.survaysName")
        .text()
        .slice(0, $(this).find("span.survaysName").text().indexOf(".")) +
      "번 설문조사";
    //체크한 것들
    var checkBtn = $(this).find('input[type="radio"]:checked');
    //체크하지 않았으면
    if (!checkBtn.length) {
      //경고문저장
      error += survaysName + "를 선택하시기 바랍니다.\n";
    }
  });

  if (error) {
            alert(error);
  }
  else {
            document.getElementById('quest').submit();
  }
});


function hasClass(target, className) {
  if( (' ' + target.className + ' ').replace(/[\n\t]/g, ' ').indexOf(' ' + className + ' ') > -1 ) return true;
  return false;
}
function removeClass(target, className){
    var elClass = ' ' + target.className + ' ';
    while(elClass.indexOf(' ' + className + ' ') !== -1){
         elClass = elClass.replace(' ' + className + ' ', '');
    }
    target.className = elClass;
}
function addClass(target, className){
    target.className += ' ' + className;
}

if( hasClass( document.getElementsByTagName('html')[0], 'ie8' ) ) { // ie8 일 경우
    var radios = document.querySelectorAll('input[type="radio"]'),
        i,
        len = radios.length;
　
    for( i = 0; i < len; i++ ) {
        radios[i].attachEvent('onchange', function(e) {
            var siblingsChecked = this.parentNode.parentNode.querySelector('.checked'); // 이전 checked 버튼

            removeClass(siblingsChecked, 'checked'); // checked 삭제
            addClass(this, 'checked'); // checked 부여
        });
    }
}