function bindCaptchaBtnClick(){
    // 自动去搜register html文件中 id为captcha-btn 的按钮
    $("#captcha-btn").on("click", function(event){
        // 生成captcha-btn替代物
        var $this = $(this);
        //获取email输入框的值
        var email = $("input[name='email']").val();
        if (!email) {
            alert('请先输入邮箱');
            return;
        }
    //    通过js发送网络请求，ajax，async javascript  and xml(json格式为主)
        $.ajax({
            //定位到user.py文件下的captcha route
            url:'/user/captcha',
            method : 'POST',
            // 发送请求的数据
            data:{
                'email':email
            },
            success:function (res){
                var code = res['code'];
                // 检验是否成功的输入邮箱号码
                if (code == 200){
                    //取消点击事件
                    $this.off("click");
                    //开始计时
                    var countDown = 60;
                    var timer=setInterval(function (){
                        // 倒计时关键，自减一
                        countDown -= 1;
                        if(countDown >0){
                             $this.text(countDown+'秒后重新发送');
                        }else {
                            $this.text('获取验证码');
                        //    重新执行函数，重新绑定点击事件
                            bindCaptchaBtnClick();
                            //清除定时器，否则会一直执行
                            clearInterval(timer);
                        }

                    },1000);
                    alert('验证码发送成功');

                }else {
                    alert(res['message']);
                }
            }
        })
    });
}

//等待网页文档所有元素，都加载完成之后在执行我们的获取验证码的按钮
$(function () {
    bindCaptchaBtnClick();
});