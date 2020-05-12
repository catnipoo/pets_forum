var vm = new Vue({
    el: '#reg',
    // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {
        host: '192.168.255.131:8000',
        error_name: false,
        error_password: false,
        error_password2: false,
        error_check_password: false,
        error_email:false,
        error_phone: false,
        error_name_message: '请输入5-20个字符的用户',
        error_password_message: '请输入8-20位的密码',
        error_password2_message: '两次输入的密码不一致',
        error_mobile_message: '请输入正确的手机号码',
        error_email_message: '请填写邮箱',
        username: '',
        password: '',
        password2: '',
        mobile: '',
        email: '',
    },
    methods: {
        // 检查用户名
        check_username: function () {
            var re = /^[a-zA-Z0-9_-]{5,20}$/;
            if (re.test(this.username)) {
                this.error_name = false;
            } else {
                this.error_name_message = '请输入5-20个字符的用户名';
                this.error_name = true;
            }

        //   前端校验完毕  才发送 判断是否重复的请求
            if (!this.error_name){
                //http://www.meiduo.site:8000/usernames/laowang/count/
                let url = this.host + '/usernames/' + this.username +'/count/'

                axios(url).then(response =>{
                //    接收后台返回的 count > 0
                    if (response.data.count > 0 ){

                          this.error_name_message = '用户名 重复了!';
                          this.error_name = true;

                    }

                }).catch( error => {

                    alert(error)
                })

            }

        },
        // 检查密码
        check_password: function () {
            var re = /^[0-9A-Za-z]{8,20}$/;
            if (re.test(this.password)) {
                this.error_password = false;
            } else {
                this.error_password = true;
                this.error_name_message = '请输入8-20密码';
            }
        },
        // 确认密码
        check_password2: function () {
            if (this.password != this.password2) {
                this.error_check_password = true;
                 this.error_name_message = '两次密码不一致';
            } else {
                this.error_check_password = false;
            }
        },
        // 检查手机号
        check_mobile: function () {
            var re = /^1[345789]\d{9}$/;
            if (re.test(this.mobile)) {
                this.error_phone = false;
            } else {
                this.error_mobile_message = '您输入的手机号格式不正确';
                this.error_phone = true;
            }

             //    发送 判断手机号是否重复 的 ajax 请求
             if (this.error_phone == false) {
                let url = '/mobiles/'+ this.mobile + '/count/';
                axios.get(url, {
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.count == 1) {
                            this.error_mobile_message = '手机号已存在';
                            this.error_phone = true;
                        } else {
                            this.error_phone = false;
                        }
                    })
                    .catch(error => {
                        console.log(error.response);
                    })
            }

        },
        //检查邮箱
        check_email: function () {
            var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
            if (re.test(this.email)) {
                this.error_email = false;
            } else {
                this.error_email_message = '邮箱格式不正确';
                this.error_email = true;
            }
        },
        // 表单提交
        on_submit(){
            this.check_username();
            this.check_password();
            this.check_password2();
            this.check_mobile();
            this.check_email();
            // this.check_sms_code();
            this.check_allow();

            if (this.error_name == true || this.error_password == true || this.error_check_password == true
                || this.error_phone == true || this.error_email == true) {
                // 不满足注册条件：禁用表单
                window.event.returnValue = false;
            }
        }
    }
});
// var vm2 = new Vue({
//     el: '#log',
//     // 修改Vue变量的读取语法，避免和django模板语法冲突
//     delimiters: ['[[', ']]'],
//     data: {
//         host,
//         f1_tab: 1, // 1F 标签页控制
//         f2_tab: 1, // 2F 标签页控制
//         f3_tab: 1, // 3F 标签页控制
//         cart_total_count: 0, // 购物车总数量
//         carts: [], // 购物车数据,
//         username:'',
//     },
//     mounted(){
//         // 获取购物车数据
//         this.get_carts();
//         this.username=getCookie('username');
//         console.log(this.username);
//     },
//     methods: {
//         // 获取购物车数据
//         get_carts(){
//             var url = this.host+'/carts/simple/';
//             axios.get(url, {
//                     responseType: 'json',
//                 })
//                 .then(response => {
//                     this.carts = response.data.cart_skus;
//                     this.cart_total_count = 0;
//                     for(var i=0;i<this.carts.length;i++){
//                         if (this.carts[i].name.length>25){
//                             this.carts[i].name = this.carts[i].name.substring(0, 25) + '...';
//                         }
//                         this.cart_total_count += this.carts[i].count;
//                     }
//                 })
//                 .catch(error => {
//                     console.log(error.response);
//                 })
//         }
//     }
// });


