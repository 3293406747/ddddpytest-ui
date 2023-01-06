// 弹窗js 被alert.html引用
function myAlert(){
    alert("请点击确定按钮")
}
function myConfirm(){
    let element = document.getElementById("confirm");
    let result = confirm("请做出你的选择");
    if(result){
        element.innerHTML = "<span style='color: #651839;'> 你选择了确定 </span>";
    }else{
        element.innerHTML = "<span style='color: #651839;'> 你选择了取消 </span>";
    }
}
function myPrompt() {
    let name = prompt('请输入你的名字');
    let element = document.getElementById("prompt");
    if (name) {
        element.innerHTML = name;
    } else if (name === '') {
        element.innerHTML = "<span style='color: #651839;'> 姓名未输入 </span>";
    } else {
        element.innerHTML = "<span style='color: #651839;'> 点击了取消按钮 </span>";
    }
}